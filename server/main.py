import os
import time
import json
from subsonic import SubsonicAPI
from flask import Flask, Response, jsonify
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
app = Flask(__name__)
api = SubsonicAPI(user=os.environ.get('SUBSONIC_USER'),
                  token=os.environ.get('SUBSONIC_TOKEN'),
                  salt=os.environ.get('SUBSONIC_SALT'),
                  endpoint=os.environ.get('SUBSONIC_ENDPOINT'),
                  appname=os.environ.get('SUBSONIC_APPNAME'))


def getNowPlaying(api):
    try:
        data = api.getNowPlaying()['subsonic-response']['nowPlaying']['entry'][0]
    except Exception as e:
        return None
    else:
        return data


def do_stream():
    ping = api.ping()
    yield 'event: ping\n'

    old_data = getNowPlaying(api)
    if old_data is None:
        yield ': no new data\n\n'
        old_data = {'id': -1000}
    else:
        yield 'data: {}\n\n'.format(json.dumps(old_data))

    while True:
        new_data = getNowPlaying(api)
        if new_data is not None and new_data.get('id') != old_data['id']:
            old_data = new_data
            yield 'data: {}\n\n'.format(json.dumps(new_data))
        else:
            yield ': no new data\n\n'
        time.sleep(5)

@app.route('/')
def index():
    data = getNowPlaying(api)
    if data is None:
        return jsonify({'error': 'no data'})
    else:
        return jsonify(data)

@app.route('/stream')
def streaming():
    return Response(do_stream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), threaded=True)
