import cv2
import requests
import json
import serial
import time
from flask import Flask, Response, request, jsonify
import threading

app = Flask(__name__)

port = '/dev/ttyACM0'
baudrate = 115200       
ser = serial.Serial(port, baudrate, timeout=1)

# Adresse de l'API du serveur sur le PC
server_url = 'http://192.168.1.17:5000/api/live_data'

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
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Envoi de l'image sous forme de flux vidéo
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def send_data_to_server():
    """Envoie les données du capteur OpenCR au serveur Flask."""
    while True:
        try:
            raw_data = ser.readline().decode('utf-8').strip()
            if raw_data:
                print(f"Données lues de l'OpenCR : {raw_data}")
                try:
                    temperature, humidity = map(float, raw_data.split(','))
                    
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


@app.route('/api/control', methods=['POST'])
def control_rover():
    """Route pour recevoir des commandes de contrôle du rover."""
    data = request.json
    if not data or 'action' not in data:
        return jsonify({"error": "Action not specified"}), 400
    
    action = data['action']
    print(f"Commande reçue : {action}")

    commands = {
        "avancer": b"A\n",
        "reculer": b"R\n",
        "gauche": b"G\n",
        "droite": b"D\n",
        "avancer_gauche": b"AG\n",
        "avancer_droite": b"AD\n",
        "reculer_gauche": b"RG\n",
        "reculer_droite": b"RD\n",
        "prendre mesure": b"M\n"
    }

    if action in commands:
        try:
            # Envoyer la commande correspondante à l'OpenCR via le port série
            ser.write(commands[action])
            print(f"Commande '{action}' envoyée à l'OpenCR.")
            return jsonify({"message": f"Commande '{action}' exécutée"}), 200
        except Exception as e:
            print(f"Erreur lors de l'envoi de la commande à l'OpenCR : {e}")
            return jsonify({"error": f"Erreur de communication avec l'OpenCR : {str(e)}"}), 500
    else:
        print(f"Action non reconnue : {action}")
        return jsonify({"error": f"Action '{action}' non reconnue"}), 400


if __name__ == '__main__':
    try:
        # Démarre la lecture des données depuis l'OpenCR
        threading.Thread(target=send_data_to_server, daemon=True).start()
        
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("Arrêt de l'application...")
    finally:
        camera.release()
        ser.close()
