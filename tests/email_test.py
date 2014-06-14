from mock import Mock
import requests

from uber import email

from tests.frontend import UberAppTestCase


class FakeEmailService(email.BaseEmailService):
    name = 'fake'


class SecondFakeEmailService(email.BaseEmailService):
    name = 'fake2'


class EmailTestCase(UberAppTestCase):
    def setUp(self):
        super(EmailTestCase, self).setUp()

        self.fake_service = FakeEmailService()
        self.fake_service2 = SecondFakeEmailService()

        self.orig_services = email._all_services

        email._all_services = {}
        email.add_service(self.fake_service)

    def tearDown(self):
        super(EmailTestCase, self).tearDown()

        email._all_services = self.orig_services

    def testadd_service(self):
        self.assertListEqual(sorted(email._all_services.values()),
                             sorted([self.fake_service]))

    def testadd_services(self):
        email.add_service(self.fake_service2)

        self.assertListEqual(sorted(email._all_services.values()),
                             sorted([self.fake_service, self.fake_service2]))

    def test_add_duplicate_service(self):
        with self.assertRaises(Exception):
            email.add_service(self.fake_service)

        with self.assertRaises(Exception):
            email.add_service(FakeEmailService())

    def test_service_send(self):
        self.fake_service.send = Mock()
        email.send('a@b.com', 'b@c.com', 'subject', 'body')

        self.fake_service.send.assert_called_with('a@b.com', 'b@c.com', 'subject', 'body')

    def test_service_error(self):
        self.fake_service.send = Mock()
        self.fake_service.send.side_effect = requests.ConnectionError('Could not connect')

        result = email.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

    def test_service_failure(self):
        self.fake_service.send = Mock()
        self.fake_service.send.return_value = False

        result = email.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

    def test_multi_service_failure(self):
        email.add_service(self.fake_service2)

        self.fake_service.send = Mock()
        self.fake_service.send.return_value = False

        self.fake_service2.send = Mock()
        self.fake_service2.send.return_value = False

        result = email.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

        self.fake_service.send.assert_called_with('a@b.com', 'b@c.com', 'subject', 'body')
        self.fake_service2.send.assert_called_with('a@b.com', 'b@c.com', 'subject', 'body')

    def test_service_success(self):
        email.add_service(self.fake_service2)

        self.fake_service.send = Mock()
        self.fake_service.send.return_value = False

        self.fake_service2.send = Mock()
        self.fake_service2.send.return_value = True

        # repeat 10 times to make sure the service failure isn't causing
        # the send to fail
        results = [email.send('a@b.com', 'b@c.com', 'subject', 'body') for x in xrange(10)]

        self.assertNotIn(False, results)

    def test_service_exception(self):
        email.add_service(self.fake_service2)

        # no send function, exception should be handled
        result = email.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)

        self.fake_service.send = Mock()
        self.fake_service.send.side_effect = Exception('Oops')

        result = email.send('a@b.com', 'b@c.com', 'subject', 'body')
        self.assertFalse(result)
