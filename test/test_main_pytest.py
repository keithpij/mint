'''
Main module that starts both pytest and coverage.py.
'''
import coverage
import pytest


if __name__ == '__main__':

    # Start code coverage tracking and erase previous results.
    cov = coverage.Coverage()
    cov.erase()
    cov.start()

    # Start the pytest runner.
    #pytest.main(['--maxfail=5', '--durations=5', '--color=yes'])
    pytest.main()

    # End coverage tracking and save the results.
    cov.stop()
    cov.save()

    # Create the HTML reports.
    cov.html_report()

    # Show the coverage summary.
    cov.report()
