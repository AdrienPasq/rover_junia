import serial
import time
import subprocess
import requests

# Configuration pour la communication série avec OpenCR
port = '/dev/ttyACM0'  # Vérifier le port sur lequel OpenCR est connecté
baudrate = 115200
ser = serial.Serial(port, baudrate, timeout=1)

# Fonction pour envoyer des commandes à l'OpenCR
def envoyer_commande_opencr(commande):
    try:
        ser.write(commande.encode('utf-8'))
        print(f"Commande envoyée à l'OpenCR: {commande}")
    except Exception as e:
        print(f"Erreur lors de l'envoi à OpenCR : {e}")

# Fonction pour récupérer les mesures du DHT11 (envoyées par l'OpenCR)
def prendre_mesure():
    print("Demande de prise de mesure")
    envoyer_commande_opencr("prendre_mesure")
    time.sleep(2)  # Attente de 2 secondes pour permettre à OpenCR de prendre la mesure
    
    # Lire les données de l'OpenCR
    raw_data = ser.readline().decode('utf-8').strip()
    if raw_data:
        try:
            temperature, humidity = map(float, raw_data.split(','))
            print(f"Température: {temperature}°C, Humidité: {humidity}%")
            return temperature, humidity
        except ValueError:
            print("Erreur dans les données reçues de l'OpenCR.")
    return None, None

# Fonctions pour les actions du rover (avancer, reculer, tourner)
def avancer():
    envoyer_commande_opencr("avancer")
    print("Rover avance")

def reculer():
    envoyer_commande_opencr("reculer")
    print("Rover recule")

def gauche():
    envoyer_commande_opencr("gauche")
    print("Rover tourne à gauche")

def droite():
    envoyer_commande_opencr("droite")
    print("Rover tourne à droite")

# Fonction principale pour gérer les commandes reçues
def main(action):
    if action == "avancer":
        avancer()
    elif action == "reculer":
        reculer()
    elif action == "gauche":
        gauche()
    elif action == "droite":
        droite()
    elif action == "prendre_mesure":
        temperature, humidity = prendre_mesure()
        if temperature is not None and humidity is not None:
            # Envoi des données mesurées (température, humidité) au serveur Flask
            requests.post("http://192.168.1.100:5000/api/mettre_a_jour_donnees", json={
                "temperature": temperature,
                "humidite": humidity
            })
    else:
        print("Action inconnue")

if __name__ == "__main__":
    # Exemple d'appel d'action depuis une commande
    action = "prendre_mesure"  # Exemple de test
    main(action)
