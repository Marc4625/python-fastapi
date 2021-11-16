import pytest 
from app.calculations import add, divide, multiply, substract, BankAccount, InsufficientFunds


# a fixture is a function that runs before a test case function
@pytest.fixture
def zero_bank_account():
    print("creating empty bank account ...")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("creating bank account with initial value ...")
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function") 
    assert add(num1, num2) == expected 

def test_substract():
    assert substract(9, 4) == 5


def test_multiply():
    assert multiply(9, 4) == 36


def test_divide():
    assert divide(9, 3) == 3


# Testing BankAccount class and methods
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50 

# using above defined fixture to do the test 
def test_bank_account_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(40)
    assert bank_account.balance == 90

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

# using parameterization and fixture to test a function with multiple inputs
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected 

def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)