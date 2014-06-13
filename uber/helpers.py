
def valid_email(val):
    return all(x in val for x in ['@', '.'])
