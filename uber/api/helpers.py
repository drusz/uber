from uber import helpers


def email_type(val):
    if helpers.valid_email(val):
        return val
    else:
        raise ValueError('%s is not a valid email address' % val.encode('utf8'))


def string_type(name, min_length=None, max_length=None):
    if min_length is None:
        min_length = 1

    def validator(val):
        try:
            result = val.encode('utf8')
        except:
            raise ValueError('%s is not a valid string' % name)
        else:
            result_len = len(result)

            if result_len < min_length:
                raise ValueError('%s must be at least %d characters' % (name, min_length))

            if max_length and result_len > max_length:
                raise ValueError('%s must be at most %d characters' % (name, max_length))

            return result

    return validator