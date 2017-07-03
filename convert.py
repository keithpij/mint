'''
Datatype conversion Tools
'''
import datetime


class InvalidDateFormat(ValueError):
    '''Custom exception to be thrown when an invalid data format is passed to the to_date function.'''
    pass


def to_date(value, date_format='mm/dd/yyyy'):
    '''
    Convert a string to a date. Values that can be processed are:
        dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy
        mm/dd/yyyy, mm-dd-yyyy, mm.dd.yyyy
        yyyymmdd
    '''
    value = value.strip()
    value = value.replace('-', '/')
    value = value.replace('.', '/')

    # Return None if no value is present.
    if len(value) == 0:
        return None

    # Looking for a format of dd/mm/yyyy
    elif date_format == 'dd/mm/yyyy':
        pieces = value.split('/')
        day = int(pieces[0])
        month = int(pieces[1])
        year = int(pieces[2])
        return_date = datetime.date(year, month, day)
        return return_date

    # Looking for a format of mm/dd/yyyy
    elif date_format == 'mm/dd/yyyy':
        pieces = value.split('/')
        month = int(pieces[0])
        day = int(pieces[1])
        year = int(pieces[2])
        return_date = datetime.date(year, month, day)
        return return_date

    # Looking for a format of yyyymmdd
    elif date_format == 'yyyymmdd':
        year = int(value[0:4])
        month = int(value[4:6])
        day = int(value[6:8])
        return_date = datetime.date(year, month, day)
        return return_date

    # If we get this far then the passed in value is in an unknown format.
    else:
        raise InvalidDateFormat('Invalid date format ' + date_format + '.')


def to_int(value):
    i = 0
    try:
        i = int(value)
    except Exception:
        i = 0
    return i


def to_float(value):
    f = 0

    value = value.replace(',', '')

    if len(value) < 1:
        return 0

    if value[0] == '$':
        value = value[1:]

    try:
        f = float(value)
    except Exception:
        f = 0
    return f
