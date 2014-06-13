import unittest

from mock import Mock
from werkzeug.contrib.cache import SimpleCache

import uber


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


class UberAppTestCase(unittest.TestCase):
    def __call__(self, *args, **kwargs):
        self.app = self.create_app()

        self.app_context = self.app.app_context()

        try:
            self.app_context.push()
            super(UberAppTestCase, self).__call__(*args, **kwargs)
        finally:
            self.app_context.pop()

    def create_app(self):
        raise NotImplementedError()

    def setUp(self):
        self.client = self.app.test_client()


if __name__ == '__main__':
    unittest.main()
