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
        if tok.type == Lexer.WORD:
            self.advance()
            return Nodes.NameNode(tok.value)

    def fullName(self, firstName, lastName):
        return Nodes.NameNode(firstName, lastName)

    def number(self):
        tok = self.currentToken
        if tok.type in (Lexer.INT, Lexer.FLOAT):
            self.advance()
            return Nodes.NumberNode(tok.value)

    def id(self):
        pass


    def operator(self, tok):
        if tok in ('+', '-', '*'):
            operation = tok
        elif tok == 'deposited':
            operation = '+'
        elif tok == 'withdrew':
            operation = '-'
        elif tok == 'accrued':
            operation = '*'
        else:
            raise Exception(f"Unsupported operator: {tok}")

        return Nodes.OperatorNode(tok, operation)

    def transaction(self):
        while self.currentToken is not None and self.tokenIndex < len(self.tokens):
            tok = self.currentToken
            if tok.type in (Lexer.PLUS, Lexer.MINUS):
                op = self.operator()
            elif tok.type in (Lexer.WORD):
                first = self.namePart(tok.value)
                if tok.type in (Lexer.WORD):
                    last = self.namePart(tok.value)
                    full = self.fullName(first, last)
            if tok.type in (Lexer.INT, Lexer.FLOAT):
                amount = self.number()
                trans = Nodes.TransactionNode(full, 47343, op, amount)
        return trans
