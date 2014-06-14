import random

from flask import current_app

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


def add_service(service):
    if _all_services.get(service.name):
        raise Exception('Service %s already exists')

    _all_services[service.name] = service
