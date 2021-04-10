import convert
import datetime
import pytest

# TODO: Create and test custom errors for each conversion function.

def test_to_date_1():
    test_value = '3/15/2017'
    valid_date = datetime.date(2017, 3, 15)
    assert convert.to_date(test_value) == valid_date


def test_to_date_2():
    test_value = '15/3/2017'
    valid_date = datetime.date(2017, 3, 15)
    assert convert.to_date(test_value, 'dd/mm/yyyy') == valid_date


def test_to_date_3():
    test_value = '20170315'
    valid_date = datetime.date(2017, 3, 15)
    assert convert.to_date(test_value, 'yyyymmdd') == valid_date


def test_to_date_4():
    test_value = '2/30/2017'
    with pytest.raises(ValueError):
        returned_value = convert.to_date(test_value)


def test_to_date_5():
    test_value = 'February 22, 2017'
    with pytest.raises(ValueError):
        returned_value = convert.to_date(test_value)


def test_to_date_6():
    test_value = ''
    assert convert.to_date(test_value) == None


def test_to_date_7():
    test_value = '2/1/2017'
    with pytest.raises(convert.InvalidDateFormat):
        returned_value = convert.to_date(test_value, 'abcdefg')


def test_to_int_1():
    assert convert.to_int('99') == 99


def test_to_int_2():
    assert convert.to_int('xxx') == 0


def test_to_float_1():
    assert convert.to_float('$12,000.87') == 12000.87


def test_to_float_2():
    assert convert.to_float('xxx') == 0


def test_to_float_3():
    assert convert.to_float('') == 0
