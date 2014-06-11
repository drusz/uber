from mock import Mock

import requests

from uber import emailer
from tests import UberTestCase


class FakeEmailService(emailer.BaseEmailService):
    name = 'fake'


class SecondFakeEmailService(emailer.BaseEmailService):
    name = 'fake2'


class EmailerTestCase(UberTestCase):
    def setUp(self):
        super(EmailerTestCase, self).setUp()

        self.fake_service = FakeEmailService()
        self.fake_service2 = SecondFakeEmailService()

        self.orig_services = emailer._all_services

        emailer._all_services = {}
        emailer._add_service(self.fake_service)

    def tearDown(self):
        emailer._all_services = self.orig_services

    def test_add_service(self):
        self.assertListEqual(sorted(emailer._all_services.values()),
                             sorted([self.fake_service]))

    def test_add_services(self):
        emailer._add_service(self.fake_service2)

        self.assertListEqual(sorted(emailer._all_services.values()),
                             sorted([self.fake_service, self.fake_service2]))

    def test_add_duplicate_service(self):
        with self.assertRaises(Exception):
            emailer._add_service(self.fake_service)

        with self.assertRaises(Exception):
            emailer._add_service(FakeEmailService())

    def test_service_send(self):
        self.fake_service.send = Mock()
        emailer.send('a@b.com', 'b@c.com', 'subject', 'body')

        self.fake_service.send.assert_called_with('a@b.com', 'b@c.com', 'subject', 'body')

    def test_service_error(self):
        self.fake_service.send = Mock()
        self.fake_service.send.side_effect = requests.ConnectionError('Could not connect')

        result = emailer.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

    def test_service_failure(self):
        self.fake_service.send = Mock()
        self.fake_service.send.return_value = False

        result = emailer.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

    def test_multi_service_failure(self):
        emailer._add_service(self.fake_service2)

        self.fake_service.send = Mock()
        self.fake_service.send.return_value = False

        self.fake_service2.send = Mock()
        self.fake_service2.send.return_value = False

        result = emailer.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

        self.fake_service.send.assert_called_with('a@b.com', 'b@c.com', 'subject', 'body')
        self.fake_service2.send.assert_called_with('a@b.com', 'b@c.com', 'subject', 'body')

    def test_service_success(self):
        emailer._add_service(self.fake_service2)

        self.fake_service.send = Mock()
        self.fake_service.send.return_value = False

        self.fake_service2.send = Mock()
        self.fake_service2.send.return_value = True

        # repeat 10 times to make sure the service failure isn't causing
        # the send to fail
        results = [emailer.send('a@b.com', 'b@c.com', 'subject', 'body') for x in xrange(10)]

        self.assertNotIn(False, results)

    def test_service_exception(self):
        emailer._add_service(self.fake_service2)

        # no send function, exception should be handled
        result = emailer.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

        self.fake_service.send = Mock()
        self.fake_service.send.side_effect = Exception('Oops')

        result = emailer.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)
