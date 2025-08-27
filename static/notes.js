// Fallback to using marked.js for markdown rendering (more reliable)
document.addEventListener('DOMContentLoaded', function () {
    const previews = document.querySelectorAll('[id^="preview_"]');

    previews.forEach(preview => {
        const content = preview.dataset.content || '';

        try {
            // Use marked.js to parse markdown
            const html = marked.parse(content);
            preview.innerHTML = `<div style="padding: 8px; font-size: 14px; line-height: 1.4;">${html}</div>`;
        } catch (error) {
            console.error('Error parsing markdown:', error);
            // Ultimate fallback to plain text
            preview.innerHTML = `<div style="padding: 8px; font-size: 14px;">${content}</div>`;
        }
    });
});


// add the filters
const publicFilter = document.getElementById('public');
const starredFilter = document.getElementById('starred');

publicFilter.addEventListener('change', () => {
    filterNotes();
});

starredFilter.addEventListener('change', () => {
    filterNotes();
});

function filterNotes() {
    const notes = document.querySelectorAll('.note');
    notes.forEach(note => {
        const isPublic = note.classList.contains('pub');
        const isStarred = note.classList.contains('fav');
        // [ 0 - pub] [ 0 - fav]
        // 
        const shouldShow = (!publicFilter.checked || isPublic) && (!starredFilter.checked || isStarred);
        note.style.display = shouldShow ? 'flex' : 'none';
    });
}


// Handle star checkbox clicks (prevent navigation when clicking star)`
document.addEventListener('click', async function (e) {
    var target = e.target.tagName === 'DIV' ? e.target : e.target.parentElement;
    console.log(target);
    if (target && target.classList.contains('favourite_btn')) {
        const noteId = target.getAttribute("note-id");
        e.preventDefault();
        await fetch('/api/fav/' + noteId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "star": !target.classList.contains('fav')
            })
        }).then(response => {
            if (response.ok) {
                response.json().then(data => {
                    if (data.success) {
                        if (data.star) {
                            if (!target.classList.contains('fav')) {
                                target.classList.add('fav')
                            }
                        } else {
                            if (target.classList.contains('fav')) {
                                target.classList.remove('fav')
                            }
                        }
                    }
                })
            } else {
                console.error('Error updating star status');
            }
        }).catch(error => {
            console.error('Error updating star status:', error);
        });

    }
    if (target && target.classList.contains("public_btn")) {
        const noteId = target.getAttribute("note-id");
        e.preventDefault();
        await fetch('/api/pub/' + noteId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "public": !target.classList.contains('pub')
            })
        }).then(response => {
            if (response.ok) {
                response.json().then(data => {
                    if (data.success) {
                        if (data.public) {
                            if (!target.classList.contains('pub')) {
                                target.classList.add('pub');
                            }
                        } else {
                            if (target.classList.contains('pub')) {
                                target.classList.remove('pub');
                            }
                        }
                    }
                })
            } else {
                console.error('Error updating public status');
            }
        }).catch(error => {
            console.error('Error updating public status:', error);
        });
    }
});