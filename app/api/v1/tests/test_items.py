from flask import json
from app.api.v1.tests.base import BaseTestCase


class TestBucketlistItems(BaseTestCase):
    def test_create_item(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())
            id = data['data']['id']

            response = self.create_item(id, self.ITEM_FIELDS, token)
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'Bucketlist item created successfully.')

    def test_wrong_bucketlist_id(self):
        with self.client:
            token = self.get_auth_token()
            id = 2

            response = self.create_item(id, self.ITEM_FIELDS, token)
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'Bucketlist does not exist.')

    def test_missing_params(self):
        with self.client:
            token = self.get_auth_token()
            response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
            data = json.loads(response.data.decode())

            id = data['data']['id']
            response = self.create_item(id, {}, token)
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'Missing required parameters.')

    # def test_update_item(self):
    #     with self.client:
    #         token = self.get_auth_token()
    #         response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
    #         data = json.loads(response.data.decode())
    #         id = data['data']['id']
    #
    #         response = self.create_item(id, self.ITEM_FIELDS, token)
    #         data = json.loads(response.data.decode())
    #         item_id = data['id']
    #
    #         response = self.client.put(
    #             '/api/v1/bucketlists/{}/items/{}'.format(id, item_id),
    #             data=json.dumps(dict(
    #                 name='Item Name Updated',
    #                 description='Some Description updated',
    #                 status='complete'
    #             )),
    #             headers=dict(
    #                 content_type='application/json',
    #                 Authorization=token
    #             )
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(data['message'], 'Bucketlist item updated successfully.')
    #         self.assertEqual(data['data']['name'], 'Item Name Updated')
    #         self.assertEqual(data['data']['description'], 'Some Description updated')
    #         self.assertEqual(data['data']['status'], 'complete')
    #         self.assertEqual(data['data']['id'], item_id)

    def test_update_item_wrong_id(self):
        with self.client:
            token = self.get_auth_token()
            id = 2
            item_id = 2
            response = self.client.put(
                '/api/v1/bucketlists/{}/items/{}'.format(id, item_id),
                data=json.dumps(dict(
                    name='Item Name Updated',
                    description='Some Description updated',
                    status='complete'
                )),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['message'], 'Bucketlist item not found.')

    # def test_item_delete(self):
    #     with self.client:
    #         token = self.get_auth_token()
    #         response = self.create_bucketlist(dict(self.BUCKETLIST_FIELDS), token)
    #         data = json.loads(response.data.decode())
    #         id = data['data']['id']
    #
    #         response = self.create_item(id, self.ITEM_FIELDS, token)
    #         data = json.loads(response.data.decode())
    #         item_id = data['id']
    #
    #         response = self.client.delete(
    #             '/api/v1/bucketlists/{}/items/{}'.format(id, item_id),
    #             headers=dict(
    #                 content_type='application/json',
    #                 Authorization=token
    #             )
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 202)
    #         self.assertEqual(data['message'], 'Bucketlist item deleted successfully.')

    def test_item_delete_wrong_id(self):
        with self.client:
            token = self.get_auth_token()
            id = 2
            item_id = 2

            response = self.client.delete(
                '/api/v1/bucketlists/{}/items/{}'.format(id, item_id),
                headers=dict(
                    content_type='application/json',
                    Authorization=token
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['message'], 'Bucketlist item not found.')
