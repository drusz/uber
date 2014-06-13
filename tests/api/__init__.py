from tests import UberAppTestCase

from uber.api import create_app


class ApiAppTestCase(UberAppTestCase):
    def create_app(self):
        return create_app(settings_override={
            'MONGODB_SETTINGS': {'DB': 'uber_test'},
            'TESTING': True,
            'WTF_CSRF_ENABLED': False
        })
