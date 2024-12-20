from flask import Flask, render_template, request, jsonify
import pymysql
import datetime
import subprocess
import requests

app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flask_user'
app.config['MYSQL_PASSWORD'] = 'MdpFlask'
app.config['MYSQL_DB'] = 'rover_db'

VIDEO_STREAM_URL = "http://10.34.100.140:8000/video_feed"  # URL du flux vidéo de la Raspberry Pi

# Connexion à la base de données
def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Routes de base
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/session_live')
def session_live():
    return render_template('session_live.html', video_stream_url=VIDEO_STREAM_URL)

@app.route('/control')
def control():
    return render_template('control.html', video_stream_url=VIDEO_STREAM_URL)

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/advanced_settings')
def advanced_settings():
    return render_template('advanced_settings.html')

@app.route('/session_details/<int:session_id>')
def session_details(session_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = '''SELECT session_date, session_time, temperature, humidity
                     FROM session_data WHERE id = %s'''
            cursor.execute(sql, (session_id,))
            session_data = cursor.fetchone()

        if session_data:
            return render_template('session_details.html', session_data=session_data)
        else:
            return "Session non trouvée. Veuillez vérifier l'ID de session.", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# API pour recevoir les données en live du rover
@app.route('/api/live_data', methods=['POST'])
def receive_live_data():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Ajouter les données dans la base de données
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            current_datetime = datetime.datetime.now()
            session_date = current_datetime.date()
            session_time = current_datetime.time()

            sql = '''INSERT INTO session_data (session_date, session_time, temperature, humidity)
                     VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql, (
                session_date,
                session_time,
                data.get('temperature'),
                data.get('humidity')
            ))
            connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"message": "Data received successfully"}), 200

# API pour envoyer des commandes au rover
@app.route('/api/control', methods=['POST'])
def control_rover():
    data = request.json
    if not data or 'action' not in data:
        return jsonify({"error": "Action not specified"}), 400
    
    action = data['action']
    print(f"Commande reçue : {action}")

    try:
        # Envoi de la commande à la Raspberry Pi
        response = requests.post(f'http://10.34.100.140:8000/api/control', json={'action': action})
        if response.status_code == 200:
            return jsonify({"message": f"Commande '{action}' envoyée au rover"}), 200
        else:
            return jsonify({"error": "Erreur lors de l'envoi de la commande au rover"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erreur de connexion : {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
