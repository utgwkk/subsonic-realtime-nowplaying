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
                      salt=os.environ.get('SUBSONIC_SALT'))
    yield 'event: ping\n\n'

    old_data = {'updated_at': 0}
    while True:
        new_data = api.getNowPlaying()
        if new_data['updated_at'] != old_data['updated_at']:
            old_data = new_data
            yield 'data: {}\n\n'.format(json.dumps(new_data))
        time.sleep(1)

@app.route('/stream')
def streaming():
    return Response(do_stream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run()
