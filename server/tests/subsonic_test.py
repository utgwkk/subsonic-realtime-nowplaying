import unittest
import subsonic


class SubsonicTest(unittest.TestCase):
    def test_api_build_url(self):
        api = subsonic.SubsonicAPI(user='utgwkk', token='hogeooo', salt='oshio',
                                   endpoint='http://localhost/subsonic')
        self.assertEqual('http://localhost/subsonic/rest/ping.view'
                         '?u=utgwkk&t=hogeooo&s=oshio&f=json',
                         api._build_url('ping'))

if __name__ == '__main__':
    unittest.main()
