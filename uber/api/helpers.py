from uber import helpers


def email_type(val):
    if helpers.valid_email(val):
        return val
    else:
        raise ValueError('%s is not a valid email address' % val.encode('utf8'))


def min_length_string(name, length=1):
    def validator(val):
        try:
            result = val.encode('utf8')
        except:
            raise ValueError('%s is not a valid string' % name)
        else:
            if len(result) < length:
                raise ValueError('%s must be at least %d characters' % (name, length))

            return result

    return validator