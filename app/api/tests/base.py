from unittest import TestCase

from flask import json

from app import create_app, db


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self):
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                surname='Test',
                firstname='Tester',
                username='tester2',
                password='pass',
                email='test2@testing.com'
            )),
            content_type='application/json'
        )
