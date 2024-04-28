'''
Chase Dallmann & John Petrie
4/28/2024
Nodes
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

#Creating a Number Node
class NumberNode:
    def __init__(self, tok):
        self.value = tok

    def __repr__(self):
        return f'{self.value}'

#Creating a Name Node
class NameNode:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def __repr__(self):
        return f'{self.firstName.value} {self.lastName.value}'

#Creating an Operator Node
class OperatorNode:
    # Operation has been decoupled from the token to support operation words
    def __init__(self, tok, operation, IDNode, NumberNode):
        self.tok = tok
        self.operation = operation
        self.IDNode = IDNode
        self.NumberNode = NumberNode

    def __repr__(self):
        return f'{self.IDNode.value} {self.tok} {self.NumberNode.value}'

#Creating an ID node
class IDNode:
    def __init__(self, tok):
        self.account_id = tok

    def __repr__(self):
        return f'{self.account_id}'

#Creating a Transaction Node
class TransactionNode:
    def __init__(self, nameNode, operatorNode):
        self.nameNode = nameNode
        self.operatorNode = operatorNode

    def __repr__(self):
        return f'{self.nameNode} {self.operatorNode.IDNode} {self.operatorNode.tok} {self.operatorNode.NumberNode}'