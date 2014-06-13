from mock import Mock

import requests

from tests.frontend import FrontendAppTestCase


class EmailerTestCase(FrontendAppTestCase):
    def setUp(self):
        super(EmailerTestCase, self).setUp()

        fake_resp = requests.Response()
        fake_resp.status_code = 200

        self.orig_post = requests.post
        requests.post = Mock(return_value=fake_resp)

    def tearDown(self):
        requests.post = self.orig_post

    def send_email(self, from_email, to_email, subject, body):
        return self.client.post('/', data=dict(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            body=body
        ))

    def test_valid_email_form(self):
        rv = self.send_email('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertIn('Email sent!', rv.data)

        requests.post.assert_called()

    def test_invalid_email_form(self):
        rv = self.send_email('', '', '', '')
        self.assertEqual(rv.data.count('This field is required.'), 4)

        rv = self.send_email('a@b.com', 'b@c.com', 'subject', '')
        self.assertIn('This field is required.', rv.data)

        rv = self.send_email('a@b.com', 'b@c.com', '', 'body')
        self.assertIn('This field is required.', rv.data)

        rv = self.send_email('a@b.com', 'bad_email', 'subject', 'body')
        self.assertIn('Invalid email address.', rv.data)

    def test_email_service_failure(self):
        requests.post.return_value = requests.Response()

        rv = self.send_email('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertIn('There was a problem sending your email! Please try again later.', rv.data)
