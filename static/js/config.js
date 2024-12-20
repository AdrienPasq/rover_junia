// Sauvegarder les paramètres dans le stockage local
document.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    const speed = document.getElementById('speed').value;
    const interval = document.getElementById('interval').value;
    const resolution = document.getElementById('mapping-resolution').value;

    localStorage.setItem('speed', speed);
    localStorage.setItem('interval', interval);
    localStorage.setItem('resolution', resolution);

    showAlert('Configuration sauvegardée avec succès.', 'success');
    console.log('Configuration sauvegardée :', { speed, interval, resolution });
});

// Charger les paramètres au chargement
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('speed').value = localStorage.getItem('speed') || '';
    document.getElementById('interval').value = localStorage.getItem('interval') || '';
    document.getElementById('mapping-resolution').value = localStorage.getItem('resolution') || '';
});
console.log("Configuration JS chargé.");
