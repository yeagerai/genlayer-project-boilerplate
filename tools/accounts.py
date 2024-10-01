from eth_account import Account


def create_new_account() -> Account:
    return Account.create()
