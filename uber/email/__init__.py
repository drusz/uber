import random

from flask import current_app
from flask import json

import requests

from uber.email import cache
from uber.email.models import *


_all_services = {}


class BaseEmailService(object):
    """
    Simple base class that an email service implements.
    """
    name = None
    full_name = None

    def __init__(self):
        pass

    def send(self, from_email, to_email, subject, body):
        """
        Sends an email using this service. Subclass services must
        implement this method.

        :param from_email: the email to send from
        :param to_email: the email to send to
        :param subject: the email subject
        :param body: the email body
        :return: True if successful, False otherwise
        """
        raise NotImplementedError()


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


def get_service(service_name):
    return _all_services.get(service_name)


def send(from_email, to_email, subject, body):
    """
    Send an email using any available service. If there is a failure, sending
    will fallback to another email service. This will continue until there are
    no available services left to try.

    If a service is attempted and unsuccessful, it will be cached as unavailable
    for a brief period of time.

    :return: True if successful, False if all services have been marked as unavailable.
    """
    valid_services = cache.available_services(_all_services.keys())

    while valid_services:
        service_name = random.choice(valid_services)
        service = _all_services[service_name]

        try:
            result = service.send(from_email, to_email, subject, body)
        except requests.RequestException:
            current_app.logger.exception('Network error sending to email service %s' % service_name)
        except Exception:
            current_app.logger.exception('Exception sending to email service %s' % service_name)
        else:
            if result:
                current_app.logger.info('Successfully sent email using service %s' % service_name)
                result = EmailServiceResult(service_name=service_name,
                                            from_email=from_email,
                                            to_email=to_email,
                                            subject=subject,
                                            body=body,
                                            success=True)
                result.save()
                return True
            else:
                current_app.logger.info('Failed to send email using service %s' % service_name)

        valid_services.remove(service_name)
        cache.set_unavailable_service(service_name)

        result = EmailServiceResult(service_name=service_name,
                                    from_email=from_email,
                                    to_email=to_email,
                                    subject=subject,
                                    body=body,
                                    success=False)
        result.save()

    return False


def _add_service(service):
    if _all_services.get(service.name):
        raise Exception('Service %s already exists')

    _all_services[service.name] = service


for name, value in globals().items():
    if (isinstance(value, type) and issubclass(value, BaseEmailService)
            and value != BaseEmailService):
        service = value()
        _add_service(service)
