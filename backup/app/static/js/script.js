// // script.js - Basic enhancements for the blog

// // Password matching validation for registration form
// document.addEventListener('DOMContentLoaded', function() {
//     const registerForm = document.querySelector('form[action="/register"]');
//     if (registerForm) {
//         registerForm.addEventListener('submit', function(event) {
//             const password = document.querySelector('#password');
//             const password2 = document.querySelector('#password2');
//             if (password && password2 && password.value !== password2.value) {
//                 alert('Passwords do not match!');
//                 event.preventDefault(); // Prevent submit
//             }
//         });
//     }

//     // Smooth scrolling for anchor links (e.g., pagination)
//     document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//         anchor.addEventListener('click', function(e) {
//             e.preventDefault();
//             const target = document.querySelector(this.getAttribute('href'));
//             if (target) {
//                 target.scrollIntoView({ behavior: 'smooth' });
//             }
//         });
//     });
// });







// ajax

document.addEventListener('DOMContentLoaded', function() {
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
                        'X-Requested-With': 'XMLHttpRequest' // Indicate AJAX request
                    }
                });
                const result = await response.json();
                if (response.ok) {
                    if (result.approved) {
                        // Append comment to the DOM
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