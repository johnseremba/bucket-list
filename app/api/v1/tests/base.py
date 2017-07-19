from unittest import TestCase
from flask import json
from app import create_app, db


class BaseTestCase(TestCase):
    USER_CREDENTIALS = dict(
        username='tester',
        password='pass'
    )

    USER_DETAILS = dict(
        surname='Test1',
        firstname='Tester1',
        username='tester1',
        password='pass',
        email='test1@testing.com'
    )

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.test_user = self.create_user(dict(
            surname='Test',
            firstname='Tester',
            username='tester',
            password='pass',
            email='test@gmail.com'
        ))

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self, data):
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

    def login_user(self, username, password):
        return self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username=username,
                password=password
            )),
            content_type='application/json'
        )

    def create_bucketlist(self, data, token):
        return self.client.post(
                '/api/v1/bucketlists/',
                data=json.dumps(data),
                headers=dict(
                    Authorization=token,
                    content_type='application/json'
                )
            )

    def get_auth_token(self):
        response = self.login_user(self.USER_CREDENTIALS['username'], self.USER_CREDENTIALS['password'])
        data = json.loads(response.data.decode())
        return data['auth_token']
