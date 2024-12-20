import pymysql
import json

# Connexion à la base de données MySQL
connection = pymysql.connect(
    host='localhost',
    user='flask_user',
    password='MdpFlask',
    db='rover_db',
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM session_data")
        
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "date": row[1].strftime("%Y-%m-%d"),
                "time": row[2].strftime("%H:%M:%S"),
                "temperature": row[3],
                "humidity": row[4],
                "position_x": row[5],
                "position_y": row[6],
            })
        
        with open('session_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

finally:
    connection.close()
