class Account:
    def __init__(self, accountNumber, ID, balance=0):
        self.ID = ID
        self.accountNumber = accountNumber
        self.balance = balance

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance