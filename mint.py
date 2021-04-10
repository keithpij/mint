'''
CLI interface for the Mint app.
'''
import sys
import datetime
import calendar
import convert
import charts
import reports
import data


def print_menu():
    '''
    Prints a list of all commands and parameters.
    '''
    print('\n')
    print('a - to get a list of accounts being tracked by your Mint account.')
    print('cat [category name] - to see spending by category. If a category name is passed then the details for that category will be shown.')
    print('cp - to compare the current month to the previous month.')
    print('day [date] - to show daily spend for the current date range. If a date is passed then the details for that day will be shown.')
    print('dr [start date] [end date] - to change the date range for which pricing data is loaded.')
    print('help - to show this help menu')
    print('income - to see income for the current date range.')
    print('lf - to load the transaction file.')
    print('pie - to see a pie chart of spending by category.')
    print('spending - to see spending for the current date range.')
    print('tag [tag name] - to see spending by tag. If a tag name is passed then the details for that tag will be shown.')
    print('quit - to quit this program')
    print('\n')


def get_user_requests():
    '''
    User request loop. Reads the next command from the user and then calls
    the appropriate function.
    '''

    transactions = data.Transactions()
    print(str(transactions.count) + ' transactions loaded.')

    # User request loop
    while True:

        prompt = str(transactions.start_date) + ' - ' + str(transactions.end_date)
        command = input(prompt + ' --> ')

        if command[0:2] == 'a':
            accounts = transactions.get_accounts()
            reports.print_accounts(accounts)
            continue

        if command[0:3] == 'cat':
            params = command[3:].strip()
            params_list = params.split(' ')
            search_name = params_list[0]
            debits = transactions.get_transactions_by_type('debit')

            if len(search_name) == 0:
                categories = transactions.get_categories(debits)
                reports.print_category_totals(categories)
            else:
                category_transactions = transactions.get_category_by_name(search_name, debits)
                if category_transactions is None:
                    print('No transactions found for category: ' + search_name + '.')
                else:
                    reports.print_transactions(search_name, category_transactions)
            continue

        if command[0:3] == 'tag':
            params = command[3:].strip()
            params_list = params.split(' ')
            search_name = params_list[0]
            debits = transactions.get_transactions_by_type('debit')

            if len(search_name) == 0:
                tags = transactions.get_tags(debits)
                reports.print_category_totals(tags)
            else:
                tag_transactions = transactions.get_tag_by_name(search_name, debits)
                if tag_transactions is None:
                    print('No transactions found for tag: ' + search_name + '.')
                else:
                    reports.print_transactions(search_name, tag_transactions)
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
            debits = transactions.get_transactions_by_type('debit', start_date, end_date)
            current_month = transactions.get_categories(debits)
            current_month_totals = transactions.get_category_totals(current_month)

            # Get previous month.
            if month == 1:
                year -= 1
                month = 12
            else:
                month -= 1

            last_day = calendar.monthrange(year, month)[1]
            start_date = datetime.date(year, month, 1)
            end_date = datetime.date(year, month, last_day)
            debits = transactions.get_transactions_by_type('debit', start_date, end_date)
            previous_month = transactions.get_categories(debits)
            previous_month_totals = transactions.get_category_totals(previous_month)

            reports.print_category_comparison(previous_month_totals, current_month_totals)
            continue

        if command[0:3] == 'day':
            report_date = command[3:].strip()
            if len(report_date) > 0:
                report_date = report_date.split(' ')
                report_date = convert.to_date(report_date)
            else:
                days = transactions.get_daily_spending()
                reports.print_daily_spending(days)
            continue

        if command[0:2] == 'dr':
            params = command[2:].strip()
            params_list = params.split(' ')
            start_date = params_list[0]
            end_date = params_list[1]
            transactions.start_date = convert.to_date(start_date)
            transactions.end_date = convert.to_date(end_date)
            continue

        if command == 'help':
            print_menu()
            continue

        if command == 'income':
            credit_transactions = transactions.get_transactions_by_type('credit')
            reports.print_transactions('Credits', credit_transactions)
            reports.print_transaction_totals('Credits', credit_transactions)
            continue

        if command == 'spending':
            debit_transactions = transactions.get_transactions_by_type('debit')
            reports.print_transactions('Debits', debit_transactions)
            reports.print_transaction_totals('Debits', debit_transactions)
            continue

        if command == 'lf':
            print('Reloading transaction file ...')
            transactions = transactions.Transactions()
            continue

        if command == 'pie':
            debits = transactions.get_transactions_by_type('debit')
            categories = transactions.get_categories(debits)
            charts.category_pie_chart(categories)
            continue

        if command == 'quit' or command == 'q':
            break

        print('*** Unrecognized command ***')


if __name__ == '__main__':
    # Main execution
    # Passed arguments
    print(sys.argv)

    # This function is a user request loop.
    get_user_requests()
