import unittest

from flask.ext.mongoengine import MongoEngine
from mock import Mock
from werkzeug.contrib.cache import SimpleCache


import uber
from uber import factory
from uber.queue import celery


celery.conf.update({
    'CELERY_ALWAYS_EAGER': True
})

TEST_SETTINGS = {
    'DEBUG': False,
    'TESTING': True,
    'MONGODB_SETTINGS': {'DB': 'uber_test'},
    'WTF_CSRF_ENABLED': False
}


class UberTestCase(unittest.TestCase):
    def setUp(self):
        self.cache = SimpleCache()

        self.orig_set = uber.cache.set
        self.orig_get_many = uber.cache.get_many

        uber.cache.set = Mock(wraps=self.cache.set)
        uber.cache.get_many = Mock(wraps=self.cache.get_many)

    def tearDown(self):
        self.cache.clear()

        uber.cache.set = self.orig_set
        uber.cache.get_many = self.orig_get_many


class UberAppTestCase(UberTestCase):
    def __call__(self, *args, **kwargs):
        self.app = self.create_app()

        self.app_context = self.app.app_context()

        try:
            self.app_context.push()
            super(UberAppTestCase, self).__call__(*args, **kwargs)
        finally:
            self.app_context.pop()

    def setUp(self):
        super(UberAppTestCase, self).setUp()

        self.client = self.app.test_client()

    def create_app(self):
        return factory.create_app(__name__, settings_override=TEST_SETTINGS)


if __name__ == '__main__':
    unittest.main()
