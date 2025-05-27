function initReactions(isAuthenticated, loginUrl) {
    isAuthenticated = (isAuthenticated === 'true');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Узнай id ContentType для EventPhoto через Django shell и подставь сюда
    const EVENT_PHOTO_TYPE_ID = 7; // <-- замени на свой id

    document.querySelectorAll('.reaction-btn').forEach(button => {
        button.addEventListener('click', async function() {
            if (!isAuthenticated) {
                window.location.href = loginUrl;
                return;
            }

            const type = this.dataset.type;
            const contentType = parseInt(this.dataset.contentType, 10);
            const objectId = parseInt(this.dataset.objectId, 10);
            
            // Для EventPhoto — отдельный URL
            if (contentType === EVENT_PHOTO_TYPE_ID) {
                let url = `/albums/photo/${objectId}/${type}/`;
                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    });
                    if (response.ok) {
                        const data = await response.json();
                        if (type === 'like') {
                            this.querySelector('.likes-count').textContent = data.likes;
                        } else {
                            this.querySelector('.dislikes-count').textContent = data.dislikes;
                        }
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            } else {
                // Для остальных — старый API
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
            }
        });
    });
} 