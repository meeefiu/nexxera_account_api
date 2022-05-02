from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from core.models import Transaction, Account
from core.exceptions import AccountNotExistsException, InsufficientAccountBalanceException, InvalidTransactionValueException


def create_account(holder_name, number):
    account = Account(holder_name=holder_name, number=number)
    account.save()
    return account


def make_deposit(account_number, value, description):
    validate_transaction_value(value)
    account = get_account_by_number_or_fail(account_number)
    transaction = Transaction(
        value=value, operation=Transaction.CREDIT, description=description, account=account)
    transaction.save()
    account.balance += value
    account.save()

    return transaction


def make_withdraw(account_number, value, description):
    validate_transaction_value(value)
    account = get_account_by_number_or_fail(account_number)

    has_balance = account.balance >= value
    if not has_balance:
        raise InsufficientAccountBalanceException(account_number)

    transaction = Transaction(
        value=value, operation=Transaction.DEBIT, description=description, account=account)
    transaction.save()

    account.balance -= value
    account.save()
    return transaction


def validate_transaction_value(value):
    invalid_value = value <= 0
    if invalid_value:
        raise InvalidTransactionValueException()


def get_account_by_number_or_fail(number):
    try:
        return Account.objects.get(number=number)
    except ObjectDoesNotExist:
        raise AccountNotExistsException(number)
