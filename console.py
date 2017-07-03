''' 
Console for the Mint app.
'''
import sys
import csv
import re
import datetime
import calendar
import convert
import charting
import reports


class Transaction:

    FIELD_COUNT = 0

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
    # The field count from the header line will help to correct scenarios
    # where the user put a comma in the Account Name field.
    global FIELD_COUNT
    FIELD_COUNT = len(header_list)

    # By not hard coding these value we are insulated from changes to the
    # underlying export file.
    for i in range(0, FIELD_COUNT):
        Transaction.index_dict[header_list[i].lower()] = i


def load_transaction_file(file):

    # Setup needed variables
    line_count = 0
    transactions = []
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
            # Do not add any transactions in the a 'Hide*' category.
            if transaction.category.lower()[0:4] == 'hide':
                print('Hidden transaction: ' + str(transaction.transaction_date) +
                      ' ' + transaction.description)
            else:
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


def get_daily_spending():
    days = dict()
    for transaction in TRANSACTIONS:
        if (transaction.transaction_date >= START_DATE) and (transaction.transaction_date <= END_DATE):
            if transaction.transaction_type.lower() == 'debit':
                if transaction.transaction_date in days:
                    days[transaction.transaction_date] = days[transaction.transaction_date] + transaction.amount
                else:
                    days[transaction.transaction_date] = transaction.amount
    return days


def get_accounts(transactions):
    accounts = dict()
    for transaction in transactions:
        # Do not add any 'Hide' categories.
        if transaction.account_name in accounts:
            accounts[transaction.account_name] += transaction.amount
        else:
            accounts[transaction.account_name] = transaction.amount
    return accounts


def get_category_by_name(search_name, debits):
    categories = get_categories(debits)
    for category_name in categories:
        if re.search(search_name.lower(), category_name.lower()):
            return categories[category_name]


def get_category_totals(categories):
    ''' Create a dictionary of totals for each category. '''
    category_totals = dict()
    for category_name in categories.keys():
        total = 0
        for transaction in categories[category_name]:
            total += transaction.amount
        category_totals[category_name] = total
    return category_totals


def get_transactions_by_type(start_date, end_date, transactions, type):
    debits = []
    for transaction in transactions:
        if (transaction.transaction_date >= start_date) and (transaction.transaction_date <= end_date):
            if transaction.transaction_type.lower() == type.lower():
                debits.append(transaction)
    return debits


def print_menu():
    '''
    Prints a list of all commands and parameters.
    '''
    print('\n')
    print('a - to get a list of accounts.')
    print('cat - to see spending by category.')
    print('cp - to compare the current month to the previous month.')
    print('day - to show daily spend for the current date range.')
    print('dr [start date] [end date] - to change the date range for which pricing data is loaded.')
    print('help - to show this help menu')
    print('income - to see income for the current date range.')
    print('lf - to load the transaction file.')
    print('pie - to see a pie chart of spending by category.')
    print('spending - to see spending for the current date range.')
    print('quit - to quit this program')
    print('\n')


def print_command_help(command):
    '''
    Prints help text for a spcific command.
    '''
    if command == 'cfs':
        print('cfs [symbol] [buy_trigger(%)] [sell_trigger(%)] [shares_per_lot] [max_lots] [max_hold_days] - to run a strategy')


def get_user_requests():
    '''
    User request loop. Reads the next command from the user and then calls
    the appropriate function.
    '''
    global START_DATE
    global END_DATE
    global TRANSACTIONS

    # User request loop
    while True:
        prompt = str(START_DATE) + ' - ' + str(END_DATE)
        command = input(prompt + ' --> ')


        if command[0:2] == 'a':
            accounts = get_accounts(TRANSACTIONS)
            reports.print_accounts(accounts)
            continue

        if command[0:3] == 'day':
            report_date = command[3:].strip()
            if len(report_date) > 0:
                report_date = report_date.split(' ')
                report_date = convert.to_date(report_date)
            else:
                days = get_daily_spending()
                reports.print_daily_spending(days)
            continue

        if command[0:2] == 'dr':
            params = command[2:].strip()
            params_list = params.split(' ')
            start_date = params_list[0]
            end_date = params_list[1]
            START_DATE = convert.to_date(start_date)
            END_DATE = convert.to_date(end_date)
            continue

        if command[0:3] == 'cat':
            params = command[3:].strip()
            params_list = params.split(' ')
            search_name = params_list[0]
            debits = get_transactions_by_type(START_DATE, END_DATE, TRANSACTIONS, 'debit')

            if len(search_name) == 0:
                categories = get_categories(debits)
                reports.print_category_totals(categories)
            else:
                category_transactions = get_category_by_name(search_name, debits)
                reports.print_transactions(search_name, category_transactions)
            continue

        if command == 'income':
            credits = get_transactions_by_type(START_DATE, END_DATE, TRANSACTIONS, 'credit')
            reports.print_transactions('Credits', credits)
            reports.print_transaction_totals('Credits', credits)
            continue

        if command == 'spending':
            debits = get_transactions_by_type(START_DATE, END_DATE, TRANSACTIONS, 'debit')
            reports.print_transactions('Debits', debits)
            reports.print_transaction_totals('Debits', debits)
            continue

        if command == 'cp':
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            # returns a touple which is the day of the week of the first day of the month and
            # the number of days in the month.
            last_day = calendar.monthrange(year, month)[1]
            start_date = datetime.date(year, month, 1)
            end_date = datetime.date(year, month, last_day)
            debits = get_transactions_by_type(start_date, end_date, TRANSACTIONS, 'debit')
            current_month = get_categories(debits)
            current_month_totals = get_category_totals(current_month)

            # Get previous month.
            if month == 1:
                year -= 1
                month = 12
            else:
                month -= 1

            last_day = calendar.monthrange(year, month)[1]
            start_date = datetime.date(year, month, 1)
            end_date = datetime.date(year, month, last_day)
            debits = get_transactions_by_type(start_date, end_date, TRANSACTIONS, 'debit')
            previous_month = get_categories(debits)
            previous_month_totals = get_category_totals(previous_month)
            reports.print_category_comparison(previous_month_totals, current_month_totals)
            continue

        if command == 'help':
            param = command[4:].strip()
            if len(param) > 0:
                print_command_help(param)
            else:
                print_menu()
            continue

        if command == 'lf':
            print('Reading transaction file ...')
            TRANSACTIONS = load_transaction_file('transactions.csv')
            continue

        if command == 'pie':
            debits = get_transactions_by_type(START_DATE, END_DATE, TRANSACTIONS, 'debit')
            categories = get_categories(debits)
            charting.category_pie_chart(categories)
            continue

        if command == 'quit' or command == 'q':
            break

        print('*** Unrecognized command ***')


if __name__ == '__main__':
    # Main execution
    # Passed arguments
    print(sys.argv)

    TRANSACTIONS = load_transaction_file('transactions.csv')

    # Get the current year and month.
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # Calculate the last day of the month.
    # calendar.monthrange returns a touple which is the day of the week of the first day
    # of the month and the number of days in the month.
    last_day = calendar.monthrange(year, month)[1]
    START_DATE = datetime.date(year, month, 1)
    END_DATE = datetime.date(year, month, last_day)

    # This function is a user request loop.
    get_user_requests()
