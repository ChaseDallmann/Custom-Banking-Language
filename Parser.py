import Nodes
import Lexer




class Parser:
    operator_words = ['deposited', 'withdrew', 'accrued']
    
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
        tok = tok.value
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
        
        # Get the tokens before and after the operator
        node_a = self.tokens[self.tokenIndex - 1] # THIS NEEDS TO BE CHANGED TO FIND THE ACCOUNT NODE BASED ON THE ACCOUNT NUMBER
        node_b = self.tokens[self.tokenIndex + 1]

        self.advance()
        return Nodes.OperatorNode(tok, operation, node_a, node_b)

    def transaction(self):
        transList = []
        trans = None
        while self.currentToken is not None and self.tokenIndex < len(self.tokens):
            tok = self.currentToken
            if tok.type in (Lexer.PLUS, Lexer.MINUS):
                op = self.operator(tok)
            elif tok.type in (Lexer.WORD):
                if tok.value in self.operator_words:
                    op = self.operator(tok)
                else:
                    first = self.namePart(tok.value)
                    if tok.type in (Lexer.WORD):
                        last = self.namePart(tok.value)
                        full = self.fullName(first, last)
            if tok.type in (Lexer.INT, Lexer.FLOAT):
                amount = self.number()
                trans = Nodes.TransactionNode(full, 47343, op, amount)
            if self.currentToken.type == Lexer.NEWTRANS:
                transList.append(trans)
                self.advance()
        return transList
