from tests import TEST_SETTINGS
from tests import UberAppTestCase

from uber.frontend import create_app


class FrontendAppTestCase(UberAppTestCase):
    def create_app(self):
        return create_app(settings_override=TEST_SETTINGS)
