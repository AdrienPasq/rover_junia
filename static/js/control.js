// Sélection des boutons de contrôle
const controlButtons = document.querySelectorAll('.control-btn');
const videoStream = document.getElementById('video-stream');

// Gestion des clics sur les boutons de contrôle
controlButtons.forEach(button => {
    button.addEventListener('click', () => {
        const action = button.dataset.action; // Récupération de l'action via l'attribut 'data-action'
        console.log(`Action : ${action}`);
        sendControlCommand(action);
        animateButton(button);
    });
});

// Fonction pour envoyer une commande au rover (via le serveur backend)
function sendControlCommand(action) {
    console.log(`Commande envoyée : ${action}`);
    
    // Envoie une requête POST à l'API backend
    fetch('/api/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => console.log(`Réponse du serveur : ${data.status}`))
    .catch(error => console.error('Erreur:', error));
}

// Placeholder pour indiquer que le flux vidéo est en cours de chargement
if (videoStream) {
    videoStream.textContent = "Chargement du flux vidéo...";
}

// Fonction pour ajouter une animation sur le bouton (au clic ou via le clavier)
function animateButton(button) {
    button.classList.add('active');
    setTimeout(() => {
        button.classList.remove('active');
    }, 100);
}

// Variables pour suivre les touches pressées
let pressedKeys = new Set();

// Gestion des commandes via clavier
document.addEventListener('keydown', (event) => {
    pressedKeys.add(event.code); // Ajouter la touche pressée à l'ensemble
    console.log('Touches pressées:', [...pressedKeys]);

    if (pressedKeys.has('ArrowUp') && pressedKeys.has('ArrowLeft')) {
        console.log('Commande : avancer_gauche');
        sendControlCommand('avancer_gauche');
        return;
    }
    else if (pressedKeys.has('ArrowUp') && pressedKeys.has('ArrowRight')) {
        console.log('Commande : avancer_droite');
        sendControlCommand('avancer_droite');
        return;
    }
    else if (pressedKeys.has('ArrowDown') && pressedKeys.has('ArrowLeft')) {
        console.log('Commande : reculer_gauche');
        sendControlCommand('reculer_gauche');
        return;
    }
    else if (pressedKeys.has('ArrowDown') && pressedKeys.has('ArrowRight')) {
        console.log('Commande : reculer_droite');
        sendControlCommand('reculer_droite');
        return;
    }

    else if (pressedKeys.has('ArrowUp')) {
        console.log('Commande : avancer');
        sendControlCommand('avancer');
    }
    else if (pressedKeys.has('ArrowDown')) {
        console.log('Commande : reculer');
        sendControlCommand('reculer');
    }
    else if (pressedKeys.has('ArrowLeft')) {
        console.log('Commande : gauche');
        sendControlCommand('gauche');
    }
    else if (pressedKeys.has('ArrowRight')) {
        console.log('Commande : droite');
        sendControlCommand('droite');
    }
    else if (pressedKeys.has('KeyF')) {
        console.log('Commande : prendre mesure');
        sendControlCommand('prendre mesure');
    }
});

// Gestion de la fin de la pression d'une touche
document.addEventListener('keyup', (event) => {
    pressedKeys.delete(event.code); // Supprimer la touche de l'ensemble quand elle est relâchée
});

// Indicateur que le fichier JavaScript a été chargé
console.log("Script de contrôle chargé.");
