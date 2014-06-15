from mock import Mock

import json

import requests

from uber.email import constants
from uber.email.models import EmailStatus
from tests.api import ApiAppTestCase


class EmailStatusTestCase(ApiAppTestCase):
    def setUp(self):
        super(EmailStatusTestCase, self).setUp()

        fake_resp = requests.Response()
        fake_resp.status_code = 200

        self.orig_post = requests.post
        requests.post = Mock(return_value=fake_resp)

        self.email_status1 = EmailStatus()

    def tearDown(self):
        super(EmailStatusTestCase, self).tearDown()

        requests.post = self.orig_post

    def send_email(self, from_email, to_email, subject, body):
        return self.client.post('/1/email', data=dict(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            body=body
        ))

    def get_email_status(self, task_id):
        return self.client.get('/1/email_status/%s' % task_id)

    def test_email_task(self):
        rv = self.send_email('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        task_id = data['task_id']

        rv = self.get_email_status(task_id)
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        self.assertEqual(data.get('task_id'), task_id)
        self.assertEqual(data.get('status'), 'pending')

        email_status = EmailStatus.objects.get(task_id=task_id)
        email_status.status = constants.EMAIL_STATUS['success']
        email_status.save()

        rv = self.get_email_status(task_id)
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        self.assertEqual(data.get('task_id'), task_id)
        self.assertEqual(data.get('status'), 'success')

    def test_invalid_email_task(self):
        rv = self.get_email_status('invalid_task_id')
        self.assertEqual(rv.status_code, 404)