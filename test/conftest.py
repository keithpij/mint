'''
Fixtures to be used by unit tests.
'''
import datetime
import calendar
import pytest
import settings
import data


@pytest.fixture(scope='session')
def transactions():
    ''' Fixture that will return a list of transactions.'''
    print('Calling the transaction fixture.')
    trans = data.Transactions()
    yield trans
    trans = None


@pytest.fixture(scope='session')
def previous_month():
    '''
    Fixture that will return a tuple with two date values.
    The first value is the first day of the previous month.
    The second value is the last day of the previous month.
    '''
    # Get the current year and month.
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # Get previous month to make sure we have data.
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

    # Calculate the last day of the month.
    # calendar.monthrange returns a touple which is the day of the week of the first day of the
    # month and the number of days in the month.
    last_day = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, last_day)
    return (start_date, end_date)


@pytest.fixture(scope='session')
def current_month():
    '''
    Fixture that will return a tuple with two date values.
    The first value is the first day of the current month.
    The second value is the last day of the current month.
    '''
    # Get the current year and month.
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # Calculate the last day of the month.
    # calendar.monthrange returns a touple which is the day of the week of the first day of the
    # month and the number of days in the month.
    last_day = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, last_day)
    return (start_date, end_date)
