import datetime
import calendar
import pytest
import dataaccess
import reports
import settings
#from test_fixtures import transactions, previous_month, current_month


'''
@pytest.mark.usefixtures('transactions')
@pytest.mark.usefixtures('previous_month')
'''

def test_print_income(transactions, previous_month):
    ''' Test print_income function. '''
    # Get the current year and month.
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    start_date = previous_month[0]
    end_date = previous_month[1]

    credits = dataaccess.get_transactions_by_type(start_date, end_date, transactions, 'credit')
    reports.print_transactions('Credits', credits)
    reports.print_transaction_totals('Credits', credits)
    assert credits != None


def test_print_credits(transactions, previous_month):
    ''' Test the print_credits function. '''
    start_date = previous_month[0]
    end_date = previous_month[1]

    debits = dataaccess.get_transactions_by_type(start_date, end_date, transactions, 'debit')
    reports.print_transactions('Debits', debits)
    reports.print_transaction_totals('Debits', debits)
    assert debits != None


def test_print_categories(transactions):
    categories = dataaccess.get_categories(transactions)
    reports.print_categories(categories)
    assert categories != None


def test_print_category_totals(transactions):
    categories = dataaccess.get_categories(transactions)
    reports.print_category_totals(categories)
    assert categories != None


def test_print_accounts(transactions):
    accounts = dataaccess.get_accounts(transactions)
    reports.print_accounts(accounts)
    assert accounts != None


def test_print_category_comparison(transactions, previous_month, current_month):
    start_date = current_month[0]
    end_date = current_month[1]

    debits = dataaccess.get_transactions_by_type(start_date, end_date, transactions, 'debit')
    current_month = dataaccess.get_categories(debits)
    current_month_totals = dataaccess.get_category_totals(current_month)

    start_date = previous_month[0]
    end_date = previous_month[1]
    debits = dataaccess.get_transactions_by_type(start_date, end_date, transactions, 'debit')
    previous_month = dataaccess.get_categories(debits)
    previous_month_totals = dataaccess.get_category_totals(previous_month)

    reports.print_category_comparison(previous_month_totals, current_month_totals)

    