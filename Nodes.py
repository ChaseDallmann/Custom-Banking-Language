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

class TransactionNode:
    def __init__(self, nameNode, accountNode, operatorNode, numberNode):
        self.nameNode = nameNode
        self.accountNode = accountNode
        self.operatorNode = operatorNode
        self.numberNode = numberNode

    def __repr__(self):
        return f'{self.nameNode} {self.accountNode} {self.operatorNode.tok} {self.numberNode.tok}'
    
class AccountNode:
    def __init__(self, tok):
        self.accountNumber = tok
        
    def getAccount(self, accountManager):
        # This method should return the Account object with the given account number.
        # For our purposes a simple linear search will be fine.
        for account in accountManager.accounts:
            if account.accountNumber == self.accountNumber:
                return account

    def __repr__(self):
        return f'{self.tok}'
