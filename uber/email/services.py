from flask import current_app

from uber.email import BaseEmailService
from uber.email import add_service

import requests

import json


class MailgunEmailService(BaseEmailService):
    name = 'mailgun'
    full_name = 'Mailgun'
    _base_url = 'https://api.mailgun.net/v2'

    def send(self, from_email, to_email, subject, body):
        url = '%s/%s/messages' % (self._base_url, current_app.config['MAILGUN_DOMAIN'])
        data = {
            'from': from_email,
            'to': to_email,
            'subject': subject,
            'text': body
        }

        resp = requests.post(url, data=data,
                             auth=('api', current_app.config['MAILGUN_API_KEY']),
                             timeout=3)

        if resp.status_code == 200:
            return True
        else:
            current_app.logger.error(resp.text)
            return False


class MandrillEmailService(BaseEmailService):
    name = 'mandrill'
    full_name = 'Mandrill'
    _base_url = 'https://mandrillapp.com/api/1.0'

    def send(self, from_email, to_email, subject, body):
        url = '%s/messages/send.json' % self._base_url
        data = {
            'key': current_app.config['MANDRILL_API_KEY'],
            'message': {
                'from_email': from_email,
                'to': [{
                    'email': to_email
                }]
            },
            'subject': subject,
            'text': body
        }

        resp = requests.post(url, data=json.dumps(data),
                             headers={'Content-Type': 'application/json'},
                             timeout=3)

        if resp.status_code == 200:
            return True
        else:
            current_app.logger.error(resp.text)
            return False


for name, value in globals().items():
    if (isinstance(value, type) and issubclass(value, BaseEmailService)
            and value != BaseEmailService):
        service = value()
        add_service(service)
