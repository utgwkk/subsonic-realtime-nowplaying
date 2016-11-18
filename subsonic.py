import requests

class SubsonicAPI:
    def __init__(self, user, token, salt, endpoint, _format='json'):
        self.user = user
        self.token = token
        self.salt = salt
        self.endpoint = endpoint
        self.format = _format

    def _build_url(self, mode):
        return '{}/rest/{}.view?u={}&t={}&s={}&f={}'.format(
            endpoint, user, token, salt, _format)

    def getNowPlaying(self):
        r = requests.get(_build_url('getNowPlaying'))
        r.raise_for_status()

        # TODO: implement
