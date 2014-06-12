import unittest

from mock import Mock
from werkzeug.contrib.cache import SimpleCache

import uber
from uber import app
from uber import db


class UberTestCase(unittest.TestCase):
    def setUp(self):
        app.config['MONGODB_SETTINGS'] = {'DB': 'uber_test'}
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        db.init_app(app)

        self.app = app.test_client()

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
