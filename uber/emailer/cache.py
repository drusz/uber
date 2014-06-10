from uber import cache


def _unavailable_service_key(service_name):
    return 'unavailable-service-%s' % service_name


def set_unavailable_service(service_name):
    cache.set(_unavailable_service_key(service_name), 1, timeout=60)


def available_services(service_names):
    """
    Filters out services that have been marked as unavailable
    :param service_names: the list of services to look up
    :return: a subset of `service_names` that have not been marked as
             unavailable
    """
    keys = map(_unavailable_service_key, service_names)
    result = cache.get_many(*keys)

    retval = []
    for i, service_name in enumerate(service_names):
        if result[i] is not 1:
            retval.append(service_name)

    return retval
