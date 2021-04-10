'''
Module to test the dataaccess module.
'''
import pytest
import settings
import data
#from test_fixtures import transactions, previous_month, current_month


def test_load_transaction_file():
    ''' Make sure we have data.'''
    transactions = data.Transactions()
    assert transactions.transaction_list != None


def test_load_transaction_file_error_1():
    ''' Make sure the correct exception is raised. '''
    with pytest.raises(data.MissingTransactionFile):
        data_file = 'does_not_exist.csv'
        transactions = data.Transactions(data_file)


def test_load_transaction_file_error_2():
    ''' Make sure the correct message is created with the exception. '''
    with pytest.raises(data.MissingTransactionFile) as exception_info:
        data_file = 'does_not_exist.csv'
        transactions = data.Transactions(data_file)
    assert data_file in str(exception_info.value)


def test_get_categories(transactions):
    ''' Test the get_categories function.'''
    categories = transactions.get_categories(transactions.transaction_list)
    assert 'Groceries' in categories


def test_get_category_by_name_1(transactions):
    search_name = 'mort'
    category = transactions.get_category_by_name(search_name, transactions.transaction_list)
    assert category != None


def test_get_category_by_name_2(transactions):
    search_name = 'zzzzz'
    category = transactions.get_category_by_name(search_name, transactions.transaction_list)
    assert category is None


def test_get_category_totals(transactions):
    categories = transactions.get_categories(transactions.transaction_list)
    category_totals = transactions.get_category_totals(categories)
    assert category_totals != None


def test_get_accounts(transactions):
    accounts = transactions.get_accounts()
    assert accounts != None


def test_get_transactions_by_type_1(transactions, previous_month):
    '''
    Will test the get_transactions_by_type function by requesting transactions of type credit.
    '''
    transactions.start_date = previous_month[0]
    transactions.end_date = previous_month[1]

    credits_list = transactions.get_transactions_by_type('credit')
    assert credits_list != None


def test_get_transactions_by_type_2(transactions, previous_month):
    '''
    Will test the get_transactions_by_type function by requesting transactions of type debit.
    '''
    transactions.start_date = previous_month[0]
    transactions.end_date = previous_month[1]

    debits_list = transactions.get_transactions_by_type('debit')
    assert debits_list != None
