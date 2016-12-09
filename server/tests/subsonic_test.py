import unittest
import subsonic


class SubsonicTest(unittest.TestCase):
    def test_api_build_url(self):
        api = subsonic.SubsonicAPI(user='utgwkk', token='hogeooo', salt='oshio',
                                   endpoint='http://localhost/subsonic',
                                   appname='hoge')
        self.assertEqual('http://localhost/subsonic/rest/ping.view'
                         '?u=utgwkk&t=hogeooo&s=oshio&f=json&v=1.14.0&c=hoge',
                         api._build_url('ping'))

if __name__ == '__main__':
    unittest.main()
