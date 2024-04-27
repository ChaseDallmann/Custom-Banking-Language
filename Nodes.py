import json
import re
import os
import sys
from json import JSONDecodeError


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class NameNode:
    def __init__(self, tok, tok2=None):
        self.tok = tok
        self.tok2 = tok2

    def __repr__(self):
        if self.tok2:
            return f'{self.tok} {self.tok2}'
        else:
            return f'{self.tok}'


class OperatorNode:
    # Operation has been decoupled from the token to support operation words
    def __init__(self, tok, operation, account_node, node_b):
        self.tok = tok
        self.operation = operation
        self.account_node = account_node
        self.node_b = node_b

    def __repr__(self):
        return f'{self.tok}'

class idNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

#Creating a node that has the account information
class AccountNode:
    def __init__(self, nameNode):
        self.ID, self.accountID = 000000, 000000
        self.name = nameNode.tok.tok + ' ' + nameNode.tok2.tok
        self.balance = 0
        self.nameNode = nameNode
        self.fileDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.filePath = self.fileDIR + '/' + 'Accounts.JSON'

    def __repr__(self):
        return f'Account(name={self.name}, ID={self.ID}, accountID={self.accountID}, balance={self.balance})'

    #Finding the ID in the JSON file
    def findAccountID(self):
        try:
            file = open(self.filePath, 'r')  # Opening Accounts.JSON
            for line in file:
                accounts = json.loads(line) #The accounts themselves parsed from the loader
                for account in accounts:
                    self.accountID = account['ID'] #Finding the ID key in accounts
                    if (re.search('([a-zA-Z][a-zA-Z])', self.accountID).group(0)) == (self.nameNode.tok.tok[0] + self.nameNode.tok2.tok[0]): #Checking to see if the initials are equal in the ID
                        self.accountID = re.search('([\\d]+)', self.accountID).group(0) #Finding the number portion of the ID
                        if int(self.accountID) > int(self.ID): #Checking to see if the ID in the JSON is greater then the current ID
                            self.ID = self.accountID
                    else:
                        self.accountID = 0
        except JSONDecodeError:
            pass
        if not self.accountID == 0:
            self.accountID = int(self.accountID) + 1   #Adding 1 to the ID if it isnt 0
        self.ID = self.nameNode.tok.tok[0] + self.nameNode.tok2.tok[0] + str(self.accountID).zfill(6) #Format <letter><letter><digit><digit><digit><digit><digit><digit>
        return self.ID

    #Dictionary entry to create a JSON format
    def to_dict(self):
        self.ID = self.findAccountID()
        return {
            "Name": self.nameNode.tok.tok + ' ' + self.nameNode.tok2.tok,
            "ID": self.ID,
            "BALANCE": self.balance
        }


class TransactionNode:
    def __init__(self, nameNode, accountNode, operatorNode, numberNode):
        self.nameNode = nameNode
        self.accountNode = accountNode
        self.operatorNode = operatorNode
        self.numberNode = numberNode

    def __repr__(self):
        return f'{self.nameNode} {self.accountNode} {self.operatorNode.tok} {self.numberNode.tok}'

    def getAccount(self, accountManager):
        # This method should return the Account object with the given account number.
        # For our purposes a simple linear search will be fine.
        for account in accountManager.accounts:
            if account.accountNumber == self.accountNumber:
                return account
