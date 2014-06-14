from mock import Mock

import json

import requests

from tests.api import ApiAppTestCase


class EmailerTestCase(ApiAppTestCase):
    def setUp(self):
        super(EmailerTestCase, self).setUp()

        fake_resp = requests.Response()
        fake_resp.status_code = 200

        self.orig_post = requests.post
        requests.post = Mock(return_value=fake_resp)

    def tearDown(self):
        requests.post = self.orig_post

    def send_email_json(self, from_email, to_email, subject, body):
        return self.client.post('/1/email', data=json.dumps(dict(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            body=body
        )), content_type='application/json')

    def send_email_form(self, from_email, to_email, subject, body):
        return self.client.post('/1/email', data=dict(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            body=body
        ))

    def test_valid_email_request_json(self):
        rv = self.send_email_json('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        self.assertEqual(data.get('err'), 0)
        self.assertIsInstance(data.get('task_id'), basestring)

        requests.post.assert_called()

    def test_valid_email_request_form(self):
        rv = self.send_email_form('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        self.assertEqual(data.get('err'), 0)
        self.assertIsInstance(data.get('task_id'), basestring)

        requests.post.assert_called()

    def test_invalid_email_request(self):
        rv = self.send_email_json('', '', '', '')
        self.assertEqual(rv.status_code, 400)

        rv = self.send_email_json('a@b.com', 'b@c.com', 'subject', '')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('body', rv.data)

        rv = self.send_email_json('a@b.com', 'b@c.com', '', 'body')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('subject', rv.data)

        rv = self.send_email_json('a@b.com', 'bad_email', 'subject', 'body')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('bad_email', rv.data)

        rv = self.send_email_json('bad_email', 'b@c.com', 'subject', 'body')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('bad_email', rv.data)
