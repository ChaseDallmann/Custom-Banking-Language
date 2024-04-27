import sys
import os
import json
from json import JSONDecodeError


class AccountManager:
    def __init__(self):
        self.accounts = []
        self.fileDIR = os.path.dirname(os.path.abspath(sys.argv[0]))  # Getting the current directory
        self.filePath = self.fileDIR + '/' + 'Accounts.JSON'  # Getting Accounts.JSON in the directory

    def addAccount(self, account):
        try:
            file = open(self.filePath, 'r')
            fileContents = json.load(file)
        except JSONDecodeError:
            fileContents = []
        fileContents.append(account.to_dict())
        file = open(self.filePath, 'w')
        json.dump(fileContents, file)
        file.close()
        print(f'Account added to the Accounts.JSON file')

    def dropAccount(self, account):
        self.accounts.remove(account)
        
    def loadAccounts(self,):
        try:
            file = open(self.filePath, 'r')
        except JSONDecodeError:
            fileContents = []
        for line in file:
            accounts = json.load(file)
            for account in accounts:
                self.accounts.append(account)
        return self.accounts