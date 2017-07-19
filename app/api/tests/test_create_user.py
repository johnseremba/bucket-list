from flask import json
from app.api.tests.base import BaseTestCase


class TestCreateUser(BaseTestCase):
    def test_response_status(self):
        with self.client:
            response = self.create_user()
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_response_messages(self):
        with self.client:
            response = self.create_user()
            data = json.loads(response.data.decode())
            self.assertTrue(data is not None)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'User registered successfully.')

    def test_token_returned(self):
        with self.client:
            response = self.create_user()
            data = json.loads(response.data.decode())
            self.assertTrue(data['auth_token'])
