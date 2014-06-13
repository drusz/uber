from tests import UberAppTestCase

from uber.frontend import create_app


class FrontendAppTestCase(UberAppTestCase):
    def create_app(self):
        return create_app(settings_override={
            'MONGODB_SETTINGS': {'DB': 'uber_test'},
            'TESTING': True,
            'WTF_CSRF_ENABLED': False
        })
