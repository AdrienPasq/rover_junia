// Fonction de mise à jour des données de session en direct
function updateLiveData() {
    const dataTable = document.querySelector('#live-data tbody');
    if (!dataTable) return; // Vérifie si la table existe avant d'ajouter des lignes

    const timestamp = new Date().toLocaleTimeString(); // Heure actuelle
    const temperature = (Math.random() * 50).toFixed(2); // Température simulée
    const humidity = (Math.random() * 100).toFixed(2); // Humidité simulée
    const positionX = (Math.random() * 100).toFixed(2); // Coordonnée X simulée
    const positionY = (Math.random() * 100).toFixed(2); // Coordonnée Y simulée

    // Création de la nouvelle ligne de données
    const newRow = `
        <tr>
            <td>${timestamp}</td>
            <td>(${positionX}, ${positionY})</td>
            <td>${temperature} °C</td>
            <td>${humidity} %</td>
        </tr>
    `;

    // Ajout de la nouvelle ligne à la table
    dataTable.innerHTML += newRow;
}

// Mise à jour des données en direct toutes les 2 secondes
setInterval(updateLiveData, 2000);

// Gestion du flux vidéo (placeholder pour le moment)
const videoStream = document.getElementById('video-stream');
if (videoStream) {
    videoStream.textContent = "Chargement du flux vidéo...";
}

console.log("Script de session live chargé.");
