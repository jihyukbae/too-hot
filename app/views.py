from app import app

@app.route('/api/submitreading', methods=['POST'])
def create_task():
    if not request.json or not 'temp' in request.json:
        abort(400)
    new_reading = {
        'temp': request.json['temp']
    }

    return jsonify({'reading': new_reading}), 201

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
