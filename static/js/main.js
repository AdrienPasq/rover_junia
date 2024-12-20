// Activer la navigation active dans le menu
document.querySelectorAll('nav ul li a').forEach(link => {
    if (link.href === window.location.href) {
        link.classList.add('active');
    }
});

// Smooth scrolling pour les ancres internes
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Ajouter une fonction utilitaire pour les alertes
function showAlert(message, type = 'info') {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
    document.body.appendChild(alertBox);

    setTimeout(() => alertBox.remove(), 3000); // Disparaît après 3 secondes
}

// Exemple : appeler l'alerte (à tester)
console.log('Main.js chargé avec succès.');
