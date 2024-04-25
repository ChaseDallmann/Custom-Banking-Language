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

    def namePart(self, part):
        tok = self.currentToken
        if tok.type in (Lexer.WORD):
            self.advance()
            return Nodes.NameNode(part)


    def fullName(self, firstName, lastName):
        tok = self.currentToken
        if tok.type in (Lexer.WORD):
            first = self.namePart(firstName)
            last = self.namePart(lastName)
        return first, last

    def number(self):
        tok = self.currentToken
        if tok.type in (Lexer.INT, Lexer.FLOAT):
            self.advance()
            return Nodes.NumberNode(tok.value)
    
    def id(self):
        pass

    def operator(self):
        tok = self.currentToken
        if tok.type in (Lexer.PLUS, Lexer.MINUS):
            self.advance()
            return Nodes.OperatorNode(tok)

    def transaction(self):
        tok = self.currentToken
        while self.currentToken is not None:
            if tok.type in (Lexer.PLUS, Lexer.MINUS):
                op = Nodes.OperatorNode(tok)
            elif tok.type in (Lexer.WORD):
                first = self.namePart(tok.value)
                if tok.type in (Lexer.WORD):
                    last = self.namePart(tok.value)
                    full = self.fullName(first, last)
            if tok.type in (Lexer.INT, Lexer.FLOAT):
                amount = self.number(tok)
            trans = Nodes.TransNode(full, 47343, op, amount)
        return trans