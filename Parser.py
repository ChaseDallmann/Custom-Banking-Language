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

    #Creating a node for parts of a name
    def namePart(self, part):
        tok = part
        if tok.type == Lexer.WORD:
            self.advance()
            return tok

    #Creating a name node
    def fullName(self, firstName, lastName):
        return Nodes.NameNode(firstName, lastName)

    #Creating a number node
    def number(self, tok):
        if tok.type in (Lexer.INT, Lexer.FLOAT):
            return Nodes.NumberNode(tok.value)

    # Creating an ID node
    def id(self, tok):
        if tok.type in (Lexer.ID):
            return Nodes.IDNode(tok.value)

    # Creating an operator node
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
        account_node = self.id(self.tokens[self.tokenIndex - 1]) # THIS NEEDS TO BE CHANGED TO FIND THE ACCOUNT NODE BASED ON THE ACCOUNT NUMBER
        number_node = self.number(self.tokens[self.tokenIndex + 1])

        self.advance()
        return Nodes.OperatorNode(tok, operation, account_node, number_node)

    #Creates a transaction AST by passing in seperate nodes, then adds it to a list of ASTs
    def transaction(self):
        transList = []
        trans = None
        while self.currentToken is not None and self.tokenIndex < len(self.tokens):
            tok = self.currentToken
            if tok.type in (Lexer.PLUS, Lexer.MINUS): #Operator Token handling
                op = self.operator(tok)
            elif tok.type in (Lexer.WORD): #Word Token handling
                if tok.value in self.operator_words:
                    op = self.operator(tok)
                else:
                    first = self.currentToken
                    self.advance()
                    if self.currentToken.type in (Lexer.WORD):
                        last = self.currentToken
                        full = self.fullName(first, last)
            if tok.type in (Lexer.ID): #Creating an ID
                self.advance()
            if tok.type in (Lexer.INT, Lexer.FLOAT): #Int/Float Token hanlding
                self.advance()
                trans = Nodes.TransactionNode(full, op)
            if self.currentToken.type == Lexer.NEWTRANS:
                transList.append(trans)
                self.advance()
        return transList
