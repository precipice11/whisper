
let likeUrl = window.likeUrl;  // grab the global variable set in template


document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.editPost').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;
            const postContentDiv = document.querySelector(`.postContent[data-post-id="${postId}"]`);
            const originalText = postContentDiv.textContent.trim();

            // Replace content with textarea
            const textarea = document.createElement('textarea');
            textarea.value = originalText;
            textarea.rows = 4;
            textarea.style.width = "100%";

            // Create save button
            const saveButton = document.createElement('button');
            saveButton.textContent = "Save";
            saveButton.style.marginTop = "5px";

        // Clear old content and insert textarea + save button
            postContentDiv.innerHTML = "";
            postContentDiv.appendChild(textarea);
            postContentDiv.appendChild(saveButton);

            saveButton.addEventListener('click', () => {
            const newContent = textarea.value.trim();

            // Send updated content via fetch
            fetch(`/edit-post/${postId}/`, {
                method: "POST",
                headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ content: newContent })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                // Replace textarea with updated content
                postContentDiv.innerHTML = newContent;
                } else {
                alert("Error saving post");
                }
        });
        });
    });
    });

    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;

            fetch(likeUrl, {
                method: 'POST',
                headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    button.textContent = '❤️'; // If liked
                } else {
                    button.textContent = '🤍'; // If unliked
                }

                const likeCountSpan = button.nextElementSibling;
                likeCountSpan.textContent = data.total_likes;
            })
            .catch(error => console.log("Error:", error))
        })
    })


    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
    }

    document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('postContent');
    const postBtn = document.getElementById('postBtn');

    textarea.addEventListener('input', () => {
        const hasContent = textarea.value.trim().length > 0;

        postBtn.disabled = !hasContent;
        postBtn.classList.toggle('enabled', hasContent);
    });
    });

})



// CSRF token helper for fetch
