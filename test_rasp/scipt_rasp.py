import cv2
import requests
import json
import serial
import time
from flask import Flask, Response

app = Flask(__name__)

# Configuration pour le port série (OpenCR connecté au port série de la Raspberry Pi)
port = '/dev/ttyACM0'  # Modifier si nécessaire selon le port utilisé pour l'OpenCR
baudrate = 115200       # Vitesse de transmission, à ajuster en fonction de l'OpenCR
ser = serial.Serial(port, baudrate, timeout=1)

# Adresse IP du serveur Flask (remplace cette adresse par celle de ton serveur)
server_url = 'http://192.168.1.100:5000/api/live_data'

# Configuration de la caméra (utilise la caméra Raspberry Pi ou une caméra USB)
camera = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

@app.route('/video_feed')
def video_feed():
    """Route pour fournir le flux vidéo."""
    return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_video_feed():
    """Générateur pour le flux vidéo."""
    while True:
        success, frame = camera.read()
        if not success:
            print("Erreur lors de la lecture de la caméra.")
            break
        else:
            # Encodage en JPEG pour le flux vidéo
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Envoi de l'image sous forme de flux vidéo
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def send_data_to_server():
    """Envoie les données du capteur OpenCR au serveur Flask."""
    while True:
        try:
            # Lecture des données depuis le port série de l'OpenCR
            raw_data = ser.readline().decode('utf-8').strip()
            if raw_data:
                print(f"Données lues de l'OpenCR : {raw_data}")
                
                # Ici, on suppose que l'OpenCR envoie une ligne sous forme de texte
                # Exemples de données : "22.5, 60.0, 10.5, 5.3" (température, humidité, position_x, position_y)
                try:
                    temperature, humidity, position_x, position_y = map(float, raw_data.split(','))
                    
                    # Construire le dictionnaire JSON pour les données à envoyer au serveur
                    sensor_data = {
                        'temperature': temperature,
                        'humidity': humidity,
                    }

                    # Envoi des données vers le serveur Flask
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(server_url, json=sensor_data, headers=headers)

                    if response.status_code == 200:
                        print("Données envoyées avec succès au serveur Flask")
                    else:
                        print(f"Erreur lors de l'envoi des données : {response.status_code}")
                except ValueError:
                    print("Erreur de format des données reçues de l'OpenCR.")
            
            time.sleep(1)  # Attente de 1 seconde avant de lire à nouveau les données
        except Exception as e:
            print(f"Erreur dans la lecture des données ou l'envoi au serveur : {e}")
            break

if __name__ == '__main__':
    try:
        # Démarre le serveur Flask pour fournir le flux vidéo et écouter les requêtes API
        print("Démarrage du serveur Flask et du streaming vidéo...")
        # Lance le serveur Flask sur l'adresse IP locale et le port 8000
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("Arrêt de l'application...")
    finally:
        # Libération des ressources (caméra et port série)
        print("Fermeture de la caméra et du port série.")
        camera.release()
        ser.close()
