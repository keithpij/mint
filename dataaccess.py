'''
Contains the Transaction class and logic to load the file downloaded from Mint.
'''
import csv
import re
import os
import convert


class MissingTransactionFile(Exception):
    '''Custom exception to be thrown when the transaction file is missing.'''
    pass


class Transaction:
    '''
    Transaction class
    '''

    DATE_HEADER = 'date'
    DESCRIPTION_HEADER = 'description'
    ORIGINAL_DESCRIPTION_HEADER = 'original description'
    AMOUNT_HEADER = 'amount'
    TRANSACTION_TYPE_HEADER = 'transaction type'
    CATEGORY_HEADER = 'category'
    ACCOUNT_NAME_HEADER = 'account name'
    LABELS_HEADER = 'labels'
    NOTES_HEADER = 'notes'

    index_dict = dict()

    def __init__(self, transaction_details):

        d = Transaction.index_dict
        self.transaction_date = convert.to_date(transaction_details[d[Transaction.DATE_HEADER]])
        self.description = transaction_details[d[Transaction.DESCRIPTION_HEADER]]
        self.original_description = transaction_details[d[Transaction.ORIGINAL_DESCRIPTION_HEADER]]
        self.amount = float(transaction_details[d[Transaction.AMOUNT_HEADER]])
        self.transaction_type = transaction_details[d[Transaction.TRANSACTION_TYPE_HEADER]]
        self.category = transaction_details[d[Transaction.CATEGORY_HEADER]]
        self.account_name = transaction_details[d[Transaction.ACCOUNT_NAME_HEADER]]
        self.labels = transaction_details[d[Transaction.LABELS_HEADER]]
        self.notes = transaction_details[d[Transaction.NOTES_HEADER]]


def set_indecies(header_list):
    '''
    Determines the index into the transaction list for each field.
    By not hard coding these values we are insulated from changes to the underlying export file.
    '''
    field_count = len(header_list)

    for i in range(0, field_count):
        Transaction.index_dict[header_list[i].lower()] = i


def load_transaction_file(file):
    '''
    Loads the transaction file specified in settings into memory.
    This function does not load hidden transactions.
    '''
    # Setup needed variables
    line_count = 0
    transactions = []

    if not os.path.isfile(file):
        raise MissingTransactionFile('Missing transaction file: ' + file)

    fhand = open(file, 'r')
    reader = csv.reader(fhand)

    # Read through each line of the file.
    for line in reader:
        line_count += 1

        # The first line contains the column headers.
        if line_count == 1:
            set_indecies(line)
        else:
            transaction = Transaction(line)
            # Do not add any transactions in a 'hide*' category.
            if transaction.category.lower()[0:4] != 'hide':
                transactions.append(transaction)

    fhand.close()
    return transactions


def get_categories(transactions):
    categories = dict()
    for transaction in transactions:
        # Do not add any 'Hide' categories.
        if transaction.category.lower()[0:3] == 'hide':
            continue
        elif transaction.category in categories:
            categories[transaction.category].append(transaction)
        else:
            categories[transaction.category] = []
            categories[transaction.category].append(transaction)

    return categories


def get_accounts(transactions):
    accounts = dict()
    for transaction in transactions:
        # Do not add any 'Hide' categories.
        if transaction.account_name in accounts:
            accounts[transaction.account_name] += transaction.amount
        else:
            accounts[transaction.account_name] = transaction.amount
    return accounts


def get_category_by_name(search_name, transactions):
    '''
    Returns the first category that matches search_name which is treated as a regular expression.
    '''
    categories = get_categories(transactions)
    for category_name in categories:
        if re.search(search_name.lower(), category_name.lower()):
            return categories[category_name]
    # If we get here then nothing was found.
    return None


def get_category_totals(categories):
    ''' Create a dictionary of totals by category. '''
    category_totals = dict()
    for category_name in categories.keys():
        total = 0
        for transaction in categories[category_name]:
            total += transaction.amount
        category_totals[category_name] = total
    return category_totals


def get_transactions_by_type(start_date, end_date, transactions, type):
    matches = []
    for transaction in transactions:
        if (transaction.transaction_date >= start_date) and (transaction.transaction_date <= end_date):
            if transaction.transaction_type.lower() == type.lower():
                matches.append(transaction)
    return matches
