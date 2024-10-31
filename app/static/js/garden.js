// Static/js/garden.js
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('garden-modal');
    const createBtn = document.getElementById('createGardenBtn');
    const closeBtn = document.getElementById('closeModal');
    const createGardenForm = document.getElementById('createGardenForm');

    // Show modal
    createBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    // Hide modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Handle form submission
    createGardenForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const gardenName = document.getElementById('gardenName').value;
        
        fetch('/create-garden', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrf_token')  // If you're using CSRF protection
            },
            body: JSON.stringify({
                name: gardenName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();  // Reload page to show new garden
            } else {
                alert('Error creating garden: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error creating garden');
        });
    });

    // Helper function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
