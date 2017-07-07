import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.my_app = True

    def test_true(self):
        self.assertTrue(self.my_app)
