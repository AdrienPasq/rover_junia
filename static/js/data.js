// Simuler les données d'une session (pour tests)
const sessionData = [
    { date: '2024-12-15', name: 'Session 1', location: 'Champs A', lidar: '#', data: '#' },
    { date: '2024-12-16', name: 'Session 2', location: 'Champs B', lidar: '#', data: '#' },
];

// Charger les données dans le tableau
function loadSessionData() {
    const table = document.querySelector('#session-table tbody');
    sessionData.forEach(session => {
        const row = `
            <tr>
                <td>${session.date}</td>
                <td>${session.name}</td>
                <td>${session.location}</td>
                <td><a href="${session.lidar}">Carte</a></td>
                <td><a href="${session.data}">Données</a></td>
            </tr>`;
        table.innerHTML += row;
    });
}

// Charger les données au chargement de la page
document.addEventListener('DOMContentLoaded', loadSessionData);
console.log("Données JS chargé.");
