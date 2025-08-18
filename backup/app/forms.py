# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
# from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
# from app.models import User

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')

# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('Username taken.')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('Email taken.')

# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     body = TextAreaField('Body', validators=[DataRequired()])
#     category = SelectField('Category', coerce=int)  # Populated dynamically
#     submit = SubmitField('Submit')

# class CommentForm(FlaskForm):
#     body = TextAreaField('Comment', validators=[DataRequired()])
#     submit = SubmitField('Post Comment')

# class ProfileForm(FlaskForm):
#     about_me = StringField('About Me', validators=[Length(min=0, max=140)])
#     submit = SubmitField('Update')









from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User, Category

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, choices=[(0, 'No Category')], validate_choice=False)
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class ProfileForm(FlaskForm):
    about_me = StringField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Update')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Add Category')

    def validate_name(self, name):
        if Category.query.filter_by(name=name.data).first():
            raise ValidationError('Category name already exists.')
