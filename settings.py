'''
Settings file that contains global settings for the mint project.
'''
import os
import inspect


MAIN_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DATA_FILE = os.path.join(MAIN_DIRECTORY, 'transactions.csv')
#DATA_FILE = os.path.join(MAIN_DIRECTORY, 'chase.csv')
OTHER_LIMIT = 300


if __name__ == '__main__':  # pragma: no cover
    print(MAIN_DIRECTORY)
    print(DATA_FILE)
