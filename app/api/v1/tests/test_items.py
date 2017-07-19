from flask import json
from app.api.v1.tests.base import BaseTestCase


class TestBucketlistItems(BaseTestCase):
    def test_create_item(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            id = data['data']['id']

            response = self.client.post(
                '/api/v1/bucketlists/{}/items/'.format(id),
                data=json.dumps(self.ITEM_FIELDS),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Bucketlist item created successfully.')

    def test_wrong_bucketlist_id(self):
        with self.client:
            token = self.get_auth_token()
            id = 2

            response = self.client.post(
                '/api/v1/bucketlists/{}/items/'.format(id),
                data=json.dumps(self.ITEM_FIELDS),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Bucketlist does not exist.')

    def test_missing_params(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            id = data['data']['id']

            response = self.client.post(
                '/api/v1/bucketlists/{}/items/'.format(id),
                data=json.dumps({}),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Missing required parameters.')
