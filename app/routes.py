from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse as url_parse
from datetime import datetime
from app import db
from app.models import User, Post, Category, Comment
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, ProfileForm, CategoryForm
import markdown
import bleach
from werkzeug.utils import secure_filename
import os
from flask import current_app  # Add this for accessing app config in routes
import uuid  # Move this from inside the if block to the top (or add if missing)

bp = Blueprint('main', __name__)

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'img'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt']
}

@bp.route('/')
@bp.route('/index', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user if current_user.is_authenticated else None, approved=current_user.is_authenticated)
        db.session.add(comment)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'approved': comment.approved,
                'body': comment.body,
                'author': comment.author.username if comment.author else 'Guest',
                'timestamp': comment.timestamp.strftime('%Y-%m-%d')
            })
        flash('Comment posted!' if comment.approved else 'Comment submitted for moderation.')
        return redirect(url_for('main.post', post_id=post.id))
    if request.method == 'POST' and not form.validate():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Invalid comment data'}), 400
    comments = post.comments.filter_by(approved=True).order_by(Comment.timestamp.asc())
    post_body_html = bleach.clean(
        markdown.markdown(post.body, extensions=['extra', 'codehilite']),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES
    )
    return render_template('post.html', post=post, form=form, comments=comments, post_body_html=post_body_html)

@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    form.category.choices = [(0, 'No Category')] + [(c.id, c.name) for c in Category.query.all()]
    if request.method == 'POST':
        print("Form submitted:", form.data, "Errors:", form.errors)  # Debug
    if form.validate_on_submit():
        category_id = form.category.data if form.category.data != 0 else None
        post = Post(title=form.title.data, body=form.body.data, author=current_user, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash('Post created!')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', form=form)

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Not authorized.')
        return redirect(url_for('main.index'))
    form = PostForm(obj=post)
    form.category.choices = [(0, 'No Category')] + [(c.id, c.name) for c in Category.query.all()]
    if request.method == 'POST':
        print("Form submitted:", form.data, "Errors:", form.errors)  # Debug
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category_id = form.category.data if form.category.data != 0 else None
        db.session.commit()
        flash('Post updated!')
        return redirect(url_for('main.post', post_id=post.id))
    return render_template('edit_post.html', form=form)

@bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Not authorized.')
        return redirect(url_for('main.index'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!')
    return redirect(url_for('main.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            # Make unique if needed
            unique_str = str(uuid.uuid4())[:8]
            filename = f"{unique_str}_{filename}"
            form.avatar.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.avatar = filename
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profile updated!')
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    # Render about_me as Markdown
    about_html = bleach.clean(
        markdown.markdown(current_user.about_me or '', extensions=['extra', 'codehilite']),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES
    ) if current_user.about_me else ''
    return render_template('profile.html', form=form, about_html=about_html)

@bp.route('/dashboard')
@login_required
def dashboard():
    posts = current_user.posts.all()
    comments_pending = Comment.query.filter_by(approved=False).all()
    return render_template('dashboard.html', posts=posts, comments_pending=comments_pending)

@bp.route('/approve_comment/<int:comment_id>', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.approved = True
    db.session.commit()
    flash('Comment approved!')
    return redirect(url_for('main.dashboard'))

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('main.index'))
    posts = Post.query.filter(Post.title.contains(query) | Post.body.contains(query)).order_by(Post.timestamp.desc()).all()
    return render_template('search.html', posts=posts, query=query)

@bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added!')
        return redirect(url_for('main.categories'))
    categories = Category.query.all()
    return render_template('categories.html', form=form, categories=categories)

@bp.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if Post.query.filter_by(category_id=category_id).first():
        flash('Cannot delete category with associated posts.')
        return redirect(url_for('main.categories'))
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted!')
    return redirect(url_for('main.categories'))


@bp.route('/category/<int:category_id>', methods=['GET'])
def category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    posts = category.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    next_url = url_for('main.category', category_id=category_id, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.category', category_id=category_id, page=posts.prev_num) if posts.has_prev else None
    return render_template('category.html', category=category, posts=posts.items, next_url=next_url, prev_url=prev_url)