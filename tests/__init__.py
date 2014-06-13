import unittest

from mock import Mock
from werkzeug.contrib.cache import SimpleCache

import uber
from uber import create_app


class UberTestCase(unittest.TestCase):
    def __call__(self, *args, **kwargs):
        self.app = create_app(settings_override={
            'MONGODB_SETTINGS': {'DB': 'uber_test'},
            'TESTING': True,
            'WTF_CSRF_ENABLED': False
        })

        self.app_context = self.app.app_context()

        try:
            self.app_context.push()
            super(UberTestCase, self).__call__(*args, **kwargs)
        finally:
            self.app_context.pop()

    def setUp(self):
        self.client = self.app.test_client()

        self.cache = SimpleCache()

        self.orig_set = uber.cache.set
        self.orig_get_many = uber.cache.get_many

        uber.cache.set = Mock(wraps=self.cache.set)
        uber.cache.get_many = Mock(wraps=self.cache.get_many)

    def tearDown(self):
        self.cache.clear()

        uber.cache.set = self.orig_set
        uber.cache.get_many = self.orig_get_many


if __name__ == '__main__':
    unittest.main()
