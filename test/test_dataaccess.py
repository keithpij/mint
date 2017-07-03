'''
Module to test the dataaccess module.
'''
import pytest
import settings
import dataaccess
#from test_fixtures import transactions, previous_month, current_month


def test_load_transaction_file():
    ''' Make sure we have data.'''
    transactions_list = dataaccess.load_transaction_file(settings.DATA_FILE)
    assert transactions_list != None


def test_load_transaction_file_error_1():
    ''' Make sure the correct exception is raised. '''
    with pytest.raises(dataaccess.MissingTransactionFile):
        transactions = dataaccess.load_transaction_file('does_not_exist.csv')


def test_load_transaction_file_error_2():
    ''' Make sure the correct message is created with the exception. '''
    with pytest.raises(dataaccess.MissingTransactionFile) as exception_info:
        file_name = 'does_not_exist.csv'
        transactions = dataaccess.load_transaction_file(file_name)
    assert file_name in str(exception_info.value)


def test_get_categories(transactions):
    ''' Test the get_categories function.'''
    transactions = dataaccess.load_transaction_file(settings.DATA_FILE)
    categories = dataaccess.get_categories(transactions)
    assert 'Food' in categories


def test_get_category_by_name_1(transactions):
    search_name = 'mort'
    category = dataaccess.get_category_by_name(search_name, transactions)
    assert category != None


def test_get_category_by_name_2(transactions):
    search_name = 'zzzzz'
    category = dataaccess.get_category_by_name(search_name, transactions)
    assert category == None


def test_get_category_totals(transactions):
    categories = dataaccess.get_categories(transactions)
    category_totals = dataaccess.get_category_totals(categories)
    assert category_totals != None


def test_get_accounts(transactions):
    accounts = dataaccess.get_accounts(transactions)
    assert accounts != None


def test_get_transactions_by_type_1(transactions, previous_month):
    '''
    Will test the get_transactions_by_type function by requesting transactions of type credit.
    '''
    start_date = previous_month[0]
    end_date = previous_month[1]

    credits_list = dataaccess.get_transactions_by_type(start_date, end_date, transactions, 'credit')
    assert credits_list != None


def test_get_transactions_by_type_2(transactions, previous_month):
    '''
    Will test the get_transactions_by_type function by requesting transactions of type debit.
    '''
    start_date = previous_month[0]
    end_date = previous_month[1]

    debits_list = dataaccess.get_transactions_by_type(start_date, end_date, transactions, 'debit')
    assert debits_list != None


if __name__ == '__main__':
    # Method names that represent tests must start with the string 'test'.
    # This naming convention informs the test runner which methods represent tests.
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataAccess)
    unittest.TextTestRunner(verbosity=2).run(suite)
