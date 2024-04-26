class Account:
    def __init__(self, accountNumber, balance=0):
        self.accountNumber = accountNumber
        self.balance = balance

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance