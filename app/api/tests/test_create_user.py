import unittest
from app import create_app

app = create_app('testing')


class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester().get('/homepage', content_type='html/text')
        self.assertEqual(response.status_code, 200)
