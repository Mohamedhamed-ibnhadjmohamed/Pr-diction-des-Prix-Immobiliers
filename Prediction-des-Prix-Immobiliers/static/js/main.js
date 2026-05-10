// JavaScript principal pour l'application immobilière

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-rafraîchissement des notifications
    if (document.querySelector('.notification-badge')) {
        setInterval(updateNotifications, 30000); // Toutes les 30 secondes
    }

    // Confirmation pour les actions de suppression
    document.querySelectorAll('.btn-delete').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer ?')) {
                e.preventDefault();
            }
        });
    });

    // Gestion des favoris
    document.querySelectorAll('.favorite-btn').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            toggleFavorite(this);
        });
    });

    // Auto-complétion pour les villes
    const cityInput = document.querySelector('input[name="city"]');
    if (cityInput) {
        initializeCityAutocomplete(cityInput);
    }

    // Gestion de la recherche avancée
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        initializeAdvancedSearch(searchForm);
    }

    // Gestion des images uploadées
    const imageUpload = document.querySelector('input[type="file"][accept*="image"]');
    if (imageUpload) {
        initializeImageUpload(imageUpload);
    }
});

// Fonction pour mettre à jour les notifications
function updateNotifications() {
    fetch('/immobilier/notifications/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notification-badge');
            if (badge && data.count > 0) {
                badge.textContent = data.count;
                badge.style.display = 'inline';
            } else if (badge) {
                badge.style.display = 'none';
            }
        })
        .catch(error => console.error('Erreur lors de la mise à jour des notifications:', error));
}

// Fonction pour basculer les favoris
function toggleFavorite(button) {
    const propertyId = button.dataset.propertyId;
    const url = button.classList.contains('active') 
        ? `/immobilier/remove-favorites/${propertyId}/`
        : `/immobilier/add-favorites/${propertyId}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            button.classList.toggle('active');
            const icon = button.querySelector('i');
            icon.classList.toggle('fas');
            icon.classList.toggle('far');
            
            // Afficher une notification
            showNotification(data.message, data.status === 'success' ? 'success' : 'error');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showNotification('Une erreur est survenue', 'error');
    });
}

// Fonction pour initialiser l'auto-complétion des villes
function initializeCityAutocomplete(input) {
    let timeout;
    
    input.addEventListener('input', function() {
        clearTimeout(timeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            hideCitySuggestions();
            return;
        }
        
        timeout = setTimeout(() => {
            fetchCities(query);
        }, 300);
    });

    // Cacher les suggestions quand on clique ailleurs
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target)) {
            hideCitySuggestions();
        }
    });
}

function fetchCities(query) {
    fetch(`/immobilier/api/cities/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            showCitySuggestions(data.cities);
        })
        .catch(error => console.error('Erreur lors de la recherche de villes:', error));
}

function showCitySuggestions(cities) {
    hideCitySuggestions();
    
    if (cities.length === 0) return;
    
    const input = document.querySelector('input[name="city"]');
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'city-suggestions';
    suggestionsDiv.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #ddd;
        border-top: none;
        max-height: 200px;
        overflow-y: auto;
        z-index: 1000;
    `;
    
    cities.forEach(city => {
        const item = document.createElement('div');
        item.textContent = city;
        item.style.cssText = `
            padding: 8px 12px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
        `;
        
        item.addEventListener('click', function() {
            input.value = city;
            hideCitySuggestions();
        });
        
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f5f5f5';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'white';
        });
        
        suggestionsDiv.appendChild(item);
    });
    
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(suggestionsDiv);
}

function hideCitySuggestions() {
    const suggestions = document.querySelector('.city-suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

// Fonction pour initialiser la recherche avancée
function initializeAdvancedSearch(form) {
    const toggleButton = document.querySelector('.toggle-advanced-search');
    const advancedFields = document.querySelector('.advanced-search-fields');
    
    if (toggleButton && advancedFields) {
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            advancedFields.style.display = advancedFields.style.display === 'none' ? 'block' : 'none';
            this.textContent = advancedFields.style.display === 'none' ? 'Recherche avancée' : 'Recherche simple';
        });
    }
}

// Fonction pour initialiser l'upload d'images
function initializeImageUpload(input) {
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                showImagePreview(e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });
}

function showImagePreview(src) {
    const preview = document.querySelector('.image-preview');
    if (preview) {
        preview.innerHTML = `
            <img src="${src}" style="max-width: 200px; max-height: 200px; border-radius: 4px;">
            <button type="button" class="btn btn-sm btn-danger mt-2" onclick="removeImagePreview()">
                <i class="fas fa-trash"></i> Supprimer
            </button>
        `;
        preview.style.display = 'block';
    }
}

function removeImagePreview() {
    const preview = document.querySelector('.image-preview');
    const input = document.querySelector('input[type="file"][accept*="image"]');
    
    if (preview) {
        preview.style.display = 'none';
        preview.innerHTML = '';
    }
    
    if (input) {
        input.value = '';
    }
}

// Fonction utilitaire pour obtenir les cookies
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

// Fonction pour afficher des notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-suppression après 5 secondes
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Fonction pour confirmer les actions sensibles
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Fonction pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Fonction pour valider les formulaires
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Export des fonctions pour utilisation globale
window.immobilierApp = {
    toggleFavorite,
    showNotification,
    confirmAction,
    formatPrice,
    validateForm,
    getCookie
};
