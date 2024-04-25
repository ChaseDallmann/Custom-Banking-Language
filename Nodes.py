class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class NameNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class OperatorNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self}'

class TransNode:

    def __init__(self, operatorNode, numberNode):
        self.operatorNode = operatorNode
        self.numberNode = numberNode

    def __repr__(self):
        return f'{self.operatorNode.tok} {self.numberNode.tok}'
