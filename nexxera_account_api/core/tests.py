from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from core.services import create_account, get_account_balances_between_period, make_deposit, make_withdraw
from core.models import Account, Transaction
from core.exceptions import (
    AccountNotExistsException,
    AccountNumberAlreadyExists,
    InsufficientAccountBalanceException,
    InvalidTransactionValueException
)


# Create your tests here.
class AccountServiceTest(TestCase):
    def test_new_accounts_must_be_zero_balance(self):
        '''
            Should create a new account and test if the initial balance is equal to 0
        '''
        account = create_account('Test Holder', number='00001')
        self.assertEqual(account.balance, 0)

    def test_create_an_account_with_number_that_already_exists(self):
        '''
            Should try to create an account with a number that already exists
            and an exception must be raised
        '''
        create_account('Test Holder', number='00001')
        with self.assertRaises(AccountNumberAlreadyExists):
            create_account('Test Holder', number='00001')


class TransactionServiceTest(TestCase):
    def test_make_a_deposit_and_account_balance_must_increase_the_transactions_value(self):
        '''
            Should make a deposit and test if the account balance is updated with that value
            The balance must increase their value
        '''
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        initial_balance = account.balance

        deposit_value = 100
        transaction = make_deposit('11111', deposit_value, 'Deposit of 100')

        expected = initial_balance + deposit_value
        actual = transaction.account.balance
        self.assertEqual(expected, actual)

    def test_make_a_withdraw_and_account_must_decrease_the_transactions_value(self):
        '''
            Should make a withdraw and test if the account balance is updated with that value
            The balance must decrease their value
        '''
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        initial_balance = account.balance

        withdraw_value = 10
        transaction = make_withdraw('11111', withdraw_value, 'Withdraw of 10')

        expected = initial_balance - withdraw_value
        actual = transaction.account.balance
        self.assertEqual(expected, actual)

    def test_try_to_make_deposit_with_an_invalid_value(self):
        '''
            Should make a deposit with an invalid value and an exception must be raised
        '''
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        with self.assertRaises(InvalidTransactionValueException):
            make_deposit('11111', 0, 'Deposit of 0')

    def test_try_to_make_withdraw_with_an_invalid_value(self):
        '''
            Should make a withdraw with an invalid value and an exception must be raised
        '''
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        with self.assertRaises(InvalidTransactionValueException):
            make_withdraw('11111', -5, 'Withdraw of -5')

    def test_try_to_make_withdraw_with_insufficient_balance(self):
        '''
            Should make a withdraw with a value that is bigger then account balance
            and an exception must be raised
        '''
        account = Account(holder_name='Test Holder',
                          balance=0, number='11111')
        account.save()

        with self.assertRaises(InsufficientAccountBalanceException):
            make_withdraw('11111', 10, 'Withdraw of 10')

    def test_try_to_make_a_transaction_with_non_existing_account(self):
        '''
            Should make a deposit and an withdraw with an account number that not exists
            and an exception must be raised
        '''
        with self.assertRaises(AccountNotExistsException):
            make_withdraw('12345', 10, 'Deposit of 10')

        with self.assertRaises(AccountNotExistsException):
            make_deposit('12345', 10, 'Withdraw of 10')

    def test_get_account_balance_in_the_start_and_in_the_end_of_a_period(self):
        '''
            Should validate if the balance in the start and in the end of a period is valid
        '''
        account = Account(holder_name='Test Holder', number='11111')
        account.save()

        Transaction(value=20, operation=Transaction.CREDIT,
                    description='description', account=account, created_at=datetime(2022, 1, 2, tzinfo=timezone.utc)).save()
        account.balance += 20

        Transaction(value=30, operation=Transaction.CREDIT,
                    description='description', account=account, created_at=datetime(2022, 1, 3, tzinfo=timezone.utc)).save()
        account.balance += 30

        Transaction(value=20, operation=Transaction.DEBIT,
                    description='description', account=account, created_at=datetime(2022, 1, 3, tzinfo=timezone.utc)).save()
        account.balance -= 20

        Transaction(value=50, operation=Transaction.CREDIT,
                    description='description', account=account, created_at=datetime(2022, 1, 4, tzinfo=timezone.utc)).save()
        account.balance += 50

        Transaction(value=10, operation=Transaction.DEBIT,
                    description='description', account=account, created_at=datetime(2022, 1, 9, tzinfo=timezone.utc)).save()
        account.balance -= 10
        account.save()

        balance = get_account_balances_between_period('11111', datetime(
            2022, 1, 2, 23, 59, 59, tzinfo=timezone.utc), datetime(2022, 1, 3, 23, 59, 59, tzinfo=timezone.utc))
        expected = {
            'balance_start': 20,
            'balance_end': 30
        }
        self.assertEqual(expected, balance)
