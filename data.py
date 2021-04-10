'''
Contains the Transaction class and logic to load the file downloaded from Mint.
'''
import csv
import re
import os
import convert
import datetime
import calendar
import settings


TAGS = ['Keith', 'Eileen', 'Split', 'Lake House', 'Glen Rock House']

class MissingTransactionFile(Exception):
    '''Custom exception to be thrown when the transaction file is missing.'''
    pass


class Transactions:
    '''
    Transactions class
    Holds a list of collection objects as well as all the functions that process transaction objects.
    '''

    def __init__(self, data_file = None):
        '''
        Loads the transaction file specified in settings into memory.
        This function does not load hidden transactions.
        '''
        if data_file is None:
            data_file = settings.DATA_FILE

        # Setup needed variables
        line_count = 0
        transactions = []

        if not os.path.isfile(data_file):
            raise MissingTransactionFile('Missing transaction file: ' + data_file)

        fhand = open(data_file, 'r')
        reader = csv.reader(fhand)

        # Read through each line of the file.
        for line in reader:
            line_count += 1

            '''
            The first line contains the column headers.
            Determines the index into the transaction list for each field.
            By not hard coding these values we are insulated from changes to the underlying export file.
            '''
            if line_count == 1:
                field_count = len(line)
                for i in range(0, field_count):
                    Transaction.index_dict[line[i].lower()] = i
            else:
                transaction = Transaction(line)
                # Do not add any transactions in a 'hide*' category.
                if transaction.category.lower()[0:4] != 'hide':
                    transactions.append(transaction)

        fhand.close()

        self.count = line_count - 1
        self.transaction_list = transactions

        # Get the current year and month.
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        # Calculate the last day of the month.
        # calendar.monthrange returns a touple which is the day of the week of the first day
        # of the month and the number of days in the month.
        last_day = calendar.monthrange(year, month)[1]

        self.start_date = datetime.date(year, month, 1)
        self.end_date = datetime.date(year, month, last_day)


    def get_accounts(self):
        '''
        Goes through the list of transactions and creates a dictionary 
        of unique account names which is returned by this function.

        Return value: account[account name] = transaction total
        The transaction total is not used anywhere but I set it in the dictionary values anyway.
        '''
        accounts = dict()
        for transaction in self.transaction_list:
            # Do not add any 'Hide' categories.
            if transaction.account_name in accounts:
                accounts[transaction.account_name] += transaction.amount
            else:
                accounts[transaction.account_name] = transaction.amount
        return accounts


    def get_daily_spending(self):
        '''
        Creates a dictionary of daily spending for the current data range.
        '''
        days = dict()
        for transaction in self.transaction_list:
            if (transaction.transaction_date >= self.start_date) and (transaction.transaction_date <= self.end_date):
                if transaction.transaction_type.lower() == 'debit':
                    if transaction.transaction_date in days:
                        days[transaction.transaction_date] = days[transaction.transaction_date] + transaction.amount
                    else:
                        days[transaction.transaction_date] = transaction.amount
        return days


    def get_categories(self, transactions_param):
        '''
        Creates a dictionary of categories based on the list of transactions passed in.
        Category names are the keys.
        Total transaction amount are the values.
        '''
        categories = dict()
        for transaction in transactions_param:
            # Do not add any 'Hide' categories.
            if transaction.category.lower()[0:3] == 'hide':
                continue
            elif transaction.category in categories:
                categories[transaction.category].append(transaction)
            else:
                categories[transaction.category] = []
                categories[transaction.category].append(transaction)

        return categories


    def get_category_by_name(self, search_name, transactions_param):
        '''
        Returns the first category that matches search_name which is treated as a regular expression.
        '''
        categories = self.get_categories(transactions_param)
        for category_name in categories:
            if re.search(search_name.lower(), category_name.lower()):
                return categories[category_name]
        # If we get here then nothing was found.
        return None


    def get_tags(self, transactions_param):
        '''
        Creates a dictionary of tags based on the list of transactions passed in.
        Tag names are the keys.
        Total transaction amount are the values.
        '''
        tags_dict = dict()
        for transaction in transactions_param:
            for tag in TAGS:
                if tag in transaction.tags:
                    if tag in tags_dict:
                        tags_dict[tag].append(transaction)
                    else:
                        tags_dict[tag] = []
                        tags_dict[tag].append(transaction)

        return tags_dict


    def get_tag_by_name(self, search_name, transactions_param):
        '''
        Returns the first tag that matches search_name which is treated as a regular expression.
        '''
        tags = self.get_tags(transactions_param)
        for tag_name in tags:
            if re.search(search_name.lower(), tag_name.lower()):
                return tags[tag_name]
        # If we get here then nothing was found.
        return None


    def get_transactions_by_type(self, tran_type, start_date = None, end_date = None):
        '''
        Returns a list of transactions for a transaction type which is either
        debit or credit.
        '''
        if start_date is None:
            start_date = self.start_date

        if end_date is None:
            end_date = self.end_date

        matches = []
        for transaction in self.transaction_list:
            if (transaction.transaction_date >= start_date) and (transaction.transaction_date <= end_date):
                if transaction.transaction_type.lower() == tran_type.lower():
                    matches.append(transaction)
        return matches


    def get_category_totals(self, categories):
        ''' Create a dictionary of totals by category. '''
        category_totals = dict()
        for category_name in categories.keys():
            total = 0
            for transaction in categories[category_name]:
                total += transaction.amount
            category_totals[category_name] = total
        return category_totals


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
    TAGS_HEADER = 'labels'
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
        self.tags = transaction_details[d[Transaction.TAGS_HEADER]]
        self.notes = transaction_details[d[Transaction.NOTES_HEADER]]
