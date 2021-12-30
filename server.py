import time

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

import pickle
import os

app = Flask(__name__, template_folder='.', static_folder='statics')


@app.route('/')
def tron():
    return render_template('tron.html')

socketio = SocketIO(app)

rooms = {}
game_replay = {}

_list = []


@socketio.on('connect', namespace='/game')
def test_connect():
    print('connected!')
    emit('my response', {'data': 'Connected'})


@socketio.on('join', namespace='/game')
def on_join(data):
    uuid = data['uuid']
    room = data['room']
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(
        {
            'uuid': uuid,
            'status': False
        }
    )
    print(str(uuid) + ' joined! ' + room)
    join_room(room)


@socketio.on('command', '/game')
def get_command(data):
    uuid = data['uuid']
    room = data['room']

    _obj = {
        'dir': data['dir'],
        'time': time.time()
    }
    print(_obj)
    game_replay[room][uuid].append(_obj)
    print('commandddddddddddddddddddddd!')
    emit('command', data, room=room)


@socketio.on('upload', '/game')
def store_data(data):
    uuid = data['uuid']
    room = data['room']
    name1 = data['name1']
    name2 = data['name2']
    replay = data['replay']

    _list.append(replay)

    # with open('replay_%s_%s.pkl' % (name1, name2), 'wb') as output:
    #     pickle.dump(replay, output, pickle.HIGHEST_PROTOCOL)

    emit('upload_completed', {}, room=room)


@socketio.on('download', '/game')
def download(data):
    uuid = data['uuid']
    room = data['room']
    name1 = data['name1']
    name2 = data['name2']

    replay = _list[-1]
    # with open('replay_%s_%s.pkl' % (name1, name2), 'rb') as input_file:
    #     replay = pickle.load(input_file)

    emit('download_completed', {'data': replay}, room=room)


@socketio.on('ready', '/game')
def start_game(data):
    uuid = data['uuid']
    room = data['room']
    print('ready for play!')

    game_replay[room] = {}
    for _obj in rooms[room]:
        if _obj['uuid'] == uuid:
            _obj['status'] = True

    flag = True if all(i['status'] for i in rooms[room]) else False
    flag = False if len(rooms[room]) < 2 else flag
    print("*" * 20)
    print(rooms)
    print("*" * 20)
    print(flag)
    print("*" * 20)

    if flag:
        data = []
        for idx, _obj in enumerate(rooms[room]):
            json = {'uuid': _obj['uuid'], 'point': idx}
            data.append(json)
            game_replay[room][_obj['uuid']] = []
        emit('start', {'data': data}, room=room)


@socketio.on('stop', '/game')
def stop_game(data):
    room = data['room']
    for _obj in rooms[room]:
        _obj['status'] = False
    emit('clear', {}, room=room)


@socketio.on('sdp', '/game')
def get_sdp(data):
    uuid = data['uuid']
    room = data['room']
    emit('sdp', data, room=room)


@socketio.on('ice', '/game')
def get_ice(data):
    uuid = data['uuid']
    room = data['room']
    emit('ice', data, room=room)


socketio.run(app, host='0.0.0.0', port=5000, debug=True, certfile='certs/cert.pem', keyfile='certs/key.pem')
