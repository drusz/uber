import unittest

from uber import app


class UberTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.app = app.test_client()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
