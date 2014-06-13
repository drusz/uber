import uber
from uber.email import cache

from tests import UberTestCase


class CacheTestCase(UberTestCase):
    def test_set_unavailable_service(self):
        key = cache._unavailable_service_key('test')

        cache.set_unavailable_service('test')

        uber.cache.set.assert_called_with(key, 1, timeout=cache.DEFAULT_UNAVAILABILITY_TIMEOUT)

    def test_get_all_available_services(self):
        result = cache.available_services(['test1', 'test2'])

        self.assertEqual(result, ['test1', 'test2'])

    def test_get_one_available_service(self):
        cache.set_unavailable_service('test1')

        result = cache.available_services(['test1', 'test2'])

        self.assertEqual(result, ['test2'])

    def test_preserve_order(self):
        cache.set_unavailable_service('test1')
        cache.set_unavailable_service('test4')

        result = cache.available_services(['test1', 'test2', 'test3', 'test4', 'test5', 'test6'])

        self.assertEqual(result, ['test2', 'test3', 'test5', 'test6'])

        cache.set_unavailable_service('test3')
        cache.set_unavailable_service('test6')

        result = cache.available_services(['test1', 'test2', 'test3', 'test4', 'test5', 'test6'])
        self.assertEqual(result, ['test2', 'test5'])

    def test_no_available_services(self):
        cache.set_unavailable_service('test1')
        cache.set_unavailable_service('test2')

        result = cache.available_services(['test1', 'test2'])

        self.assertEqual(result, [])
