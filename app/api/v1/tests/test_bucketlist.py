from flask import json
from app.api.v1.tests.base import BaseTestCase


class TestCreateBucketlist(BaseTestCase):
    def test_no_authentication_token(self):
        with self.client:
            token = ''
            response = self.create_bucketlist(dict(
                name='Bucketlist1',
                description='Some description',
                interests='Some interests'
            ), token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid authentication token')

    def test_create(self):
        with self.client:
            token = self.get_auth_token()
            response = self.client.post(
                '/api/v1/bucketlists/',
                data=json.dumps(dict(
                    name="Bucketlist5",
                    description="Some Description",
                    interests="Some interest"
                )),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Bucketlist created successfully.')
