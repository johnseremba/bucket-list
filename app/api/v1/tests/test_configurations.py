from unittest import TestCase
from app import create_app


class TestDevelopmentConfig(TestCase):
    def test_app_is_development(self):
        app = create_app('development')
        self.assertFalse(app is None)
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql://localhost/bucketlist')


class TestTestingConfig(TestCase):
    def test_app_is_testing(self):
        app = create_app('testing')
        self.assertFalse(app is None)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql://localhost/bucketlist_test')


class TestStagingConfig(TestCase):
    def test_app_is_stagging(self):
        app = create_app('staging')
        self.assertFalse(app is None)
        self.assertTrue(app.config['DEBUG'] is False)


class TestProdConfig(TestCase):
    def test_app_is_prod(self):
        app = create_app('production')
        self.assertFalse(app is None)
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql://localhost/bucketlist_prod')
