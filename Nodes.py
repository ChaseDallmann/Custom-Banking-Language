import json
import re
import os
import sys
from json import JSONDecodeError


class NumberNode:
    def __init__(self, tok):
        self.value = tok

    def __repr__(self):
        return f'{self.value}'


class NameNode:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def __repr__(self):
        return f'{self.firstName.value} {self.lastName.value}'


class OperatorNode:
    # Operation has been decoupled from the token to support operation words
    def __init__(self, tok, operation, IDNode, NumberNode):
        self.tok = tok
        self.operation = operation
        self.IDNode = IDNode
        self.NumberNode = NumberNode

    def __repr__(self):
        return f'{self.IDNode.value} {self.tok} {self.NumberNode.value}'

#Creating a node that has the account information
class IDNode:
    def __init__(self, tok):
        self.account_id = tok

    def __repr__(self):
        return f'{self.account_id}'



class TransactionNode:
    def __init__(self, nameNode, operatorNode):
        self.nameNode = nameNode
        self.operatorNode = operatorNode


    def __repr__(self):
        return f'{self.nameNode} {self.operatorNode.IDNode} {self.operatorNode.tok} {self.operatorNode.NumberNode}'