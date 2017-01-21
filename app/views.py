from app import app
from flask import jsonify, abort, request, make_response

@app.route('/api/submitreading', methods=['POST'])
def create_task():
    if not request.json or not 'temp' in request.json:
        return make_response(jsonify({'error': 'No temperature specified'}), 400)
    new_reading = {
        'temp': request.json['temp']
    }

    return jsonify({'reading': new_reading}), 201

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
