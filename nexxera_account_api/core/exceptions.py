class AccountNotExistsException(Exception):
    def __init__(self, number):
        super().__init__(f'Account with number {number} not exists')


class InsufficientAccountBalanceException(Exception):
    def __init__(self, number):
        super().__init__(f'Insufficient balance for account {number}')


class InvalidTransactionValueException(Exception):
    def __init__(self):
        super().__init__('The number must be a number grater then 0')
