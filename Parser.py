import Nodes
import Lexer
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = 0
        self.currentToken = self.tokens[self.tokenIndex]

    def parse(self):
        res = self.transaction()
        return res

    def advance(self):
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]
        return self.currentToken

    def firstName(self, firstName):
        return Nodes.NameNode(firstName)

    def lastName(self, lastName):
        return Nodes.NameNode(lastName)

    def fullName(self):
        first = self.firstName()
        last = self.lastName()
        return first + " " + last

    def number(self):
        tok = self.currentToken
        if tok.type in (Lexer.INT, Lexer.FLOAT):
            self.advance()
            return Nodes.NumberNode(tok.value)

    def operator(self):
        tok = self.currentToken
        if tok.type in (Lexer.PLUS, Lexer.MINUS):
            self.advance()
            return Nodes.OperatorNode(tok)

    def transaction(self):
        tok = self.currentToken
        if tok.type in (Lexer.PLUS, Lexer.MINUS):
            left = self.operator()
        right = self.number()
        trans = Nodes.TransNode(left, right)
        return trans