from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from core.models import Transaction, Account
from core.exceptions import (
    AccountNotExistsException,
    InsufficientAccountBalanceException,
    InvalidTransactionValueException
)


def create_account(holder_name, number):
    account = Account(holder_name=holder_name, number=number)
    account.save()
    return account


def make_deposit(account_number, value, description):
    validate_transaction_value(value)
    account = get_account_by_number_or_fail(account_number)
    transaction_attributes = {
        'value': value,
        'operation': Transaction.CREDIT,
        'description': description,
        'account': account,
        'created_at': datetime.now(tz=timezone.utc)
    }
    transaction = Transaction(**transaction_attributes)
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

    transaction_attributes = {
        'value': value,
        'operation': Transaction.DEBIT,
        'description': description,
        'account': account,
        'created_at': datetime.now(tz=timezone.utc)
    }
    transaction = Transaction(**transaction_attributes)
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


def get_account_extract_between_period(account_number, start, end):
    return Transaction.objects.filter(account__number=account_number,
                                      created_at__gte=start, created_at__lte=end)


def get_account_balances_between_period(account_number, start, end):
    balance_of_start_period = get_balance_until(account_number, start)
    balance_of_end_period = get_balance_until(account_number, end)

    return {
        'balance_start': balance_of_start_period,
        'balance_end': balance_of_end_period
    }


def get_balance_until(account_number, date):
    sum_debts_until_date = get_transactions_sum_of_operation_until(
        account_number, Transaction.DEBIT, date)
    sum_credits_until_date = get_transactions_sum_of_operation_until(
        account_number, Transaction.CREDIT, date)
    balance = sum_credits_until_date - sum_debts_until_date
    return balance


def get_transactions_sum_of_operation_until(account_number, operation, date):
    aggregate = Transaction.objects.filter(
        created_at__lte=date, operation=operation, account__number=account_number).aggregate(sum=Sum('value'))
    sum_value = 0 if aggregate['sum'] == None else aggregate['sum']
    return sum_value
