import os
import time
import json
from subsonic import SubsonicAPI
from flask import Flask, Response
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
app = Flask(__name__)


def do_stream():
    api = SubsonicAPI(user=os.environ.get('SUBSONIC_USER'),
                      token=os.environ.get('SUBSONIC_TOKEN'),
                      salt=os.environ.get('SUBSONIC_SALT'),
                      endpoint=os.environ.get('SUBSONIC_ENDPOINT'),
                      appname=os.environ.get('SUBSONIC_APPNAME'))
    ping = api.ping()
    yield 'event: ping\n'
    yield 'data: {}\n\n'.format(json.dumps(ping))

    old_data = api.getNowPlaying()['subsonic-response']['nowPlaying']['entry'][0]
    yield 'data: {}\n\n'.format(json.dumps(old_data))
    while True:
        new_data = api.getNowPlaying()['subsonic-response']['nowPlaying']['entry'][0]
        if new_data['id'] != old_data['id']:
            old_data = new_data
            yield 'data: {}\n\n'.format(json.dumps(new_data))
        time.sleep(60)

@app.route('/stream')
def streaming():
    return Response(do_stream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)