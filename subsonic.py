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
            self.endpoint, mode, self.user, self.token, self.salt, self.format)

    def getNowPlaying(self):
        r = requests.get(self._build_url('getNowPlaying'))
        r.raise_for_status()

        # TODO: implement

    def ping(self):
        r = requests.get(self._build_url('ping'))
        r.raise_for_status()

        return r.json()
