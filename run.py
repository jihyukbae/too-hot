


from app import app
from flask import jsonify, abort, request, make_response, send_from_directory, render_template
import sqlite3, time, datetime, json
from flask_socketio import SocketIO
import time
from dateutil.parser import parse
from datetime import datetime as dt
from datetime import date, timedelta


app.config['SECRET_KEY'] = 'secret!'

SICK_THRESHOLD = 36

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    temp_readings = get_all_readings_json_fmt()
    json_data = json.loads(temp_readings)['temps']

    num_readings_total = len(json_data)
    num_sick_total = 0
    num_readings_today = 0
    num_sick_today = 0

    # var nextWeek = Date.parse(new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7));

    previous_days_sick_totals = []
    for i in range(0,19):
        previous_days_sick_totals.append(0)

    for reading in json_data:
        timestamp = reading['timestamp']
        datetime_obj = parse(timestamp, fuzzy=True)

        if reading['temp'] > SICK_THRESHOLD and datetime_obj.date() == dt.today().date():
            num_sick_today += 1
            num_readings_today += 1
        if reading['temp'] > SICK_THRESHOLD:
            num_sick_total += 1

        for i in range(0,19):
            dayobj = dt.today() - timedelta(i+1)
            if reading['temp'] > SICK_THRESHOLD and datetime_obj.date() == dayobj.date():
                previous_days_sick_totals[i] += 1
    previous_days_sick_totals.reverse()
    return render_template('admin.html', readings=json_data, num_readings_today=num_readings_today, num_sick_today=num_sick_today,
                           num_readings_total=num_readings_total,num_sick_total=num_sick_total, previous_days_sick_totals=previous_days_sick_totals)

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
        currTime = dt.fromtimestamp(rawTime).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO temps (sensorID, timestamp, temp) VALUES (?, ?, ?)",(request.json['sensorID'], currTime, request.json['temp']))
        conn.commit()
        conn.close()
        reading_temp = request.json['temp']
        sick_status = None
        if reading_temp > SICK_THRESHOLD:
            sick_status = "true"
        else:
            sick_status = "false"

        socketio.emit('newtemp', {'temp': request.json['temp'],'sick':sick_status,'timestamp':currTime,'sensorID':request.json['sensorID']})
        return jsonify({'reading': new_reading}), 201
    elif request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        rows = cursor.fetchall()
        data = {"temps": []}
        for row in rows:
            print row
            data["temps"].append({'readingID': row[0], 'sensorID': row[1], 'timestamp': row[2], 'temp': row[3]})

        return jsonify(data), 200


    else:
        return jsonify({'status': 'error'}), 400

def get_all_readings_json_fmt():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from temps order by readingID DESC LIMIT 100")
    rows = cursor.fetchall()
    data = {"temps": []}
    for row in rows:
        print row
        data["temps"].append({'readingID': row[0], 'sensorID': row[1], 'timestamp': row[2], 'temp': row[3]})

    return json.dumps(data)

@app.route('/api/makenewdb', methods=['GET'])
def create_db():
    conn = sqlite3.connect('database.db')
    print "Opened database successfully"

    conn.execute('CREATE TABLE temps (readingID INTEGER PRIMARY KEY AUTOINCREMENT, sensorID INTEGER, timestamp TEXT, temp REAL)')
    print "Table created successfully"
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/api/makeemployeedb', methods=['GET'])
def create_employee_db():
    conn = sqlite3.connect('database_emp.db')
    conn.execute('CREATE TABLE emps (name TEXT, latitude REAL, longitude REAL)')
    conn.close()
    print "Employee Table created successfully"

    return jsonify({'status': 'success'})

@app.route('/api/emps', methods=['POST'])
def insert_employee():
    new_reading = {
        'name': request.json['name'],
        'latitude': request.json['latitude'],
        'longitude': request.json['longitude']
    }
    conn = sqlite3.connect('database_emp.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emps (name, latitude, longitude) VALUES (?, ?, ?)",(request.json['name'], request.json['latitude'], request.json['longitude']))
    conn.commit()
    conn.close()

    return jsonify({'reading': new_reading}), 201

socketio = SocketIO(app)
socketio.run(app)
