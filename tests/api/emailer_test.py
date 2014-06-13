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

    def send_email(self, from_email, to_email, subject, body):
        return self.client.post('/email', data=json.dumps(dict(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            body=body
        )), content_type='application/json')

    def test_valid_email_request(self):
        rv = self.send_email('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        self.assertDictEqual(data, {'err': 0})

        requests.post.assert_called()

    def test_invalid_email_request(self):
        rv = self.send_email('', '', '', '')
        self.assertEqual(rv.status_code, 400)

        rv = self.send_email('a@b.com', 'b@c.com', 'subject', '')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('body', rv.data)

        rv = self.send_email('a@b.com', 'b@c.com', '', 'body')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('subject', rv.data)

        rv = self.send_email('a@b.com', 'bad_email', 'subject', 'body')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('bad_email', rv.data)

    def test_email_service_failure(self):
        requests.post.return_value = requests.Response()

        rv = self.send_email('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertIn('There was a problem sending your email! Please try again later.', rv.data)