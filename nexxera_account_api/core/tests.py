from django.test import TestCase
from core.services import create_account, make_deposit, make_withdraw
from core.models import Account
from core.exceptions import AccountNotExistsException, InsufficientAccountBalanceException, InvalidTransactionValueException


# Create your tests here.
class AccountServiceTest(TestCase):
    def test_new_accounts_must_be_zero_balance(self):
        account = create_account('Test Holder', number='00001')
        self.assertEqual(account.balance, 0)


class CoreTransactionTest(TestCase):
    def test_make_a_deposit_and_account_balance_must_increase_the_transactions_value(self):
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
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        initial_balance = account.balance

        withdraw_value = 10
        transaction = make_withdraw('11111', withdraw_value, 'Withdraw of 10')

        expected = initial_balance - withdraw_value
        actual = transaction.account.balance
        self.assertEqual(expected, actual)

    def test_try_to_make_deposit_with_an_invalid_number(self):
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        with self.assertRaises(InvalidTransactionValueException):
            make_deposit('11111', 0, 'Deposit of 0')

    def test_try_to_make_withdraw_with_an_invalid_number(self):
        account = Account(holder_name='Test Holder',
                          balance=100, number='11111')
        account.save()

        with self.assertRaises(InvalidTransactionValueException):
            make_withdraw('11111', -5, 'Withdraw of -5')

    def test_try_to_make_withdraw_with_insufficient_balance(self):
        account = Account(holder_name='Test Holder',
                          balance=0, number='11111')
        account.save()

        with self.assertRaises(InsufficientAccountBalanceException):
            make_withdraw('11111', 10, 'Withdraw of 10')

    def test_try_to_make_a_transaction_with_non_existing_account(self):
        with self.assertRaises(AccountNotExistsException):
            make_withdraw('12345', 10, 'Deposit of 10')

        with self.assertRaises(AccountNotExistsException):
            make_deposit('12345', 10, 'Withdraw of 10')
