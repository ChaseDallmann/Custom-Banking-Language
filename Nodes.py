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
    def __init__(self, tok, operation, IDNode, NumberNode):
        self.tok = tok
        self.operation = operation
        self.IDNode = IDNode
        self.NumberNode = NumberNode

    def __repr__(self):
        return f'{self.tok}'

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