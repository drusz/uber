from tests import TEST_SETTINGS
from tests import UberAppTestCase

from uber.api import create_app


class ApiAppTestCase(UberAppTestCase):
    def create_app(self):
        return create_app(settings_override=TEST_SETTINGS)
