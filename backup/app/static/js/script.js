document.addEventListener('DOMContentLoaded', function() {
    // Initialize EasyMDE for create_post and edit_post forms
    const markdownEditor = document.getElementById('markdown-editor');
    if (markdownEditor) {
        const easyMDE = new EasyMDE({
            element: markdownEditor,
            spellChecker: false,
            status: false,
            forceSync: true,
            previewRender: function(plainText) {
                // Convert Markdown to HTML
                const html = this.markdown(plainText);
                // Create a temporary container for MathJax
                const container = document.createElement('div');
                container.innerHTML = html;
                // Trigger MathJax rendering
                if (typeof MathJax !== 'undefined') {
                    MathJax.typesetPromise([container]).then(() => {
                        // Ensure MathJax renders equations
                    });
                }
                return container.innerHTML;
            }
        });
        // Debug: Log EasyMDE value on change
        easyMDE.codemirror.on('change', () => {
            console.log('EasyMDE value:', easyMDE.value());
            markdownEditor.value = easyMDE.value();
        });
    }

    // Debug form submission
    const forms = document.querySelectorAll('#create-post-form, #edit-post-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log('Form submission triggered:', form.id);
            const formData = new FormData(form);
            console.log('Form data:', Object.fromEntries(formData));
            if (markdownEditor && easyMDE) {
                markdownEditor.value = easyMDE.value();
            }
        });
    });

    // Password matching validation for registration form
    const registerForm = document.querySelector('form[action="/register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            const password = document.querySelector('#password');
            const password2 = document.querySelector('#password2');
            if (password && password2 && password.value !== password2.value) {
                alert('Passwords do not match!');
                event.preventDefault();
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // AJAX for comment form submission
    const commentForm = document.querySelector('form[action^="/post/"]');
    if (commentForm) {
        commentForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(commentForm);
            try {
                const response = await fetch(commentForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                const result = await response.json();
                if (response.ok) {
                    if (result.approved) {
                        const commentsSection = document.querySelector('.comments-list') || document.createElement('div');
                        if (!commentsSection.classList.contains('comments-list')) {
                            commentsSection.classList.add('comments-list');
                            commentForm.before(commentsSection);
                        }
                        const newComment = document.createElement('div');
                        newComment.className = 'card mb-2';
                        newComment.innerHTML = `
                            <div class="card-body">
                                <p>${result.body}</p>
                                <p><small>By ${result.author || 'Guest'} on ${result.timestamp}</small></p>
                            </div>
                        `;
                        commentsSection.appendChild(newComment);
                        commentForm.reset();
                        alert('Comment posted!');
                    } else {
                        alert('Comment submitted for moderation.');
                        commentForm.reset();
                    }
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('AJAX error:', error);
                alert('Failed to post comment. Please try again.');
            }
        });
    }
});


// data upload
const form = document.getElementById("uploadForm");
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);

    try {
    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });
    const text = await response.text();
    document.getElementById("result").innerHTML = text;
    } catch (err) {
    document.getElementById("result").innerHTML = "Upload failed: " + err;
    }
});

