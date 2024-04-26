class AccountManager:
    def __init__(self):
        self.accounts = []

    def addAccount(self, account):
        self.accounts.append(account)

    def dropAccount(self, account):
        self.accounts.remove(account)
        
    def getAccount(self, accountNumber):
        for account in self.accounts:
            if account.accountNumber == accountNumber:
                return account
        return None