from flask import json
from app.api.v1.tests.base import BaseTestCase


class TestBucketlist(BaseTestCase):
    def test_no_authentication_token(self):
        with self.client:
            token = ''
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid authentication token')

    def test_create(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Bucketlist created successfully.')

    def test_missing_params(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist({}, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Missing required parameters.')

    def test_update_bucketlist(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            id = data['data']['id']

            response = self.client.put(
                '/api/v1/bucketlists/{}'.format(id),
                data=json.dumps(dict(
                    name='Bucketlist Updated',
                    description='Some Description updated',
                    interests='Some interests updated'
                )),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Bucketlist updated successfully.')

    def test_get_bucketlist(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            id = data['data']['id']

            response = self.client.get(
                '/api/v1/bucketlists/{}'.format(id),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Bucketlist(s) retrieved successfully.')

    def test_get_bucketlist_wrong_id(self):
        with self.client:
            token = self.get_auth_token()
            response = self.client.get(
                '/api/v1/bucketlists/{}'.format(23),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'No bucketlist(s) found.')

    def test_delete_bucketlist(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            id = data['data']['id']

            response = self.client.delete(
                '/api/v1/bucketlists/{}'.format(id),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Bucketlist deleted successfully.')

    def test_delete_bucketlist_wrong_id(self):
        with self.client:
            token = self.get_auth_token()
            id = 34

            response = self.client.delete(
                '/api/v1/bucketlists/{}'.format(id),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Bucketlist not found.')
