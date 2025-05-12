function initReactions(isAuthenticated, loginUrl) {
    isAuthenticated = (isAuthenticated === 'true');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    document.querySelectorAll('.reaction-btn').forEach(button => {
        button.addEventListener('click', async function() {
            if (!isAuthenticated) {
                window.location.href = loginUrl;
                return;
            }

            const type = this.dataset.type;
            const contentType = this.dataset.contentType;
            const objectId = this.dataset.objectId;
            
            try {
                const response = await fetch('/api/reactions/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        reaction_type: type,
                        content_type: contentType,
                        object_id: objectId
                    })
                });

                if (response.ok) {
                    const data = await response.json();

                    document.querySelectorAll(
                        `.reaction-btn[data-object-id="${data.object_id}"][data-content-type="${data.content_type}"]`
                    ).forEach(btn => {
                        const container = btn.closest('.reactions');
                        if (container) {
                    container.querySelector('.likes-count').textContent = data.likes;
                    container.querySelector('.dislikes-count').textContent = data.dislikes;
                        }
                    });
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
} 