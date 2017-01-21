from app import app
from flask import jsonify, abort, request, make_response, send_from_directory
import sqlite3, time, datetime


@app.route('/')
@app.route('/index')
def index():
    return "To be implemented"


@app.route('/static/admin')
def admin_index():
    return send_from_directory('static', "admin.html")

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/api/temps', methods=['POST', 'GET'])
def process_temps():
    if request.method == 'POST':
        if not request.json or not 'temp' in request.json:
            return make_response(jsonify({'error': 'No temperature specified'}), 400)
        new_reading = {
            'temp': request.json['temp'],
            'sensorID': request.json['sensorID']
        }

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        rawTime = time.time()
        currTime = datetime.datetime.fromtimestamp(rawTime).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO temps (sensorID, timestamp, temp) VALUES (?, ?, ?)",(request.json['sensorID'], currTime, request.json['temp']))
        conn.commit()
        conn.close()
        return jsonify({'reading': new_reading}), 201
    elif request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("select * from temps")
        rows = cursor.fetchall()
        data = {"temps": []}
        for row in rows:
            print row
            data["temps"].append({'readingID': row[0], 'sensorID': row[1], 'timestamp': row[2], 'temp': row[3]})


        return jsonify(data), 200


    else:
        return jsonify({'status': 'error'}), 400

@app.route('/api/makenewdb', methods=['GET'])
def create_db():
    conn = sqlite3.connect('database.db')
    print "Opened database successfully"

    conn.execute('CREATE TABLE temps (readingID INTEGER PRIMARY KEY AUTOINCREMENT, sensorID INTEGER, timestamp TEXT, temp REAL)')
    print "Table created successfully"
    conn.close()

    return jsonify({'status': 'success'})
