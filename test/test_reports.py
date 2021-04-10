import datetime
import calendar
import pytest
import data
import reports
import settings
#from test_fixtures import transactions, previous_month, current_month


'''
@pytest.mark.usefixtures('transactions')
@pytest.mark.usefixtures('previous_month')
'''

def test_print_transactions_1(transactions, previous_month):
    ''' Test print_transactions with credits. '''

    start_date = previous_month[0]
    end_date = previous_month[1]

    credits = transactions.get_transactions_by_type('credit')
    reports.print_transactions('Credits', credits)
    reports.print_transaction_totals('Credits', credits)
    assert credits != None


def test_print_print_transactions_2(transactions, previous_month):
    ''' Test the print_transactions with debits. '''
    start_date = previous_month[0]
    end_date = previous_month[1]

    debits = transactions.get_transactions_by_type('debit')
    reports.print_transactions('Debits', debits)
    reports.print_transaction_totals('Debits', debits)
    assert debits != None


def test_print_categories(transactions):
    categories = transactions.get_categories(transactions.transaction_list)
    reports.print_categories(categories)
    assert categories != None


def test_print_category_totals(transactions):
    categories = transactions.get_categories(transactions.transaction_list)
    reports.print_category_totals(categories)
    assert categories != None


def test_print_accounts(transactions):
    accounts = transactions.get_accounts()
    reports.print_accounts(accounts)
    assert accounts != None


def test_print_category_comparison(transactions, previous_month, current_month):
    transactions.start_date = current_month[0]
    transactions.end_date = current_month[1]

    debits = transactions.get_transactions_by_type('debit')
    current_month_categories = transactions.get_categories(debits)
    current_month_totals = transactions.get_category_totals(current_month_categories)

    transactions.start_date = previous_month[0]
    transactions.end_date = previous_month[1]
    debits = transactions.get_transactions_by_type('debit')
    previous_month_categories = transactions.get_categories(debits)
    previous_month_totals = transactions.get_category_totals(previous_month_categories)

    reports.print_category_comparison(previous_month_totals, current_month_totals)
    assert current_month_totals != None
    assert previous_month_totals != None
    