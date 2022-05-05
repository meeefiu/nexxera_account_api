class AccountNotExistsException(Exception):
    def __init__(self, number):
        self.message = f'Account with number {number} does not exists'
        super().__init__(self.message)


class InsufficientAccountBalanceException(Exception):
    def __init__(self, number):
        self.message = f'Insufficient balance for account {number}'
        super().__init__(self.message)


class InvalidTransactionValueException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AccountNumberAlreadyExists(Exception):
    def __init__(self, number):
        self.message = f'The {number} account already exists'
        super().__init__(self.message)
