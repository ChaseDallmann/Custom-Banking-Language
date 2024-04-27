import Nodes
import Lexer




class Parser:
    
    operator_types = (Lexer.PLUS, Lexer.MINUS, Lexer.MULTIPLY, Lexer.CREATE, Lexer.DROP, Lexer.VIEW)
    
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
        tok = tok.type
        if tok in self.operator_types:
            operation = tok
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
            if tok.type in self.operator_types: #Operator Token handling
                op = self.operator(tok)
            elif tok.type == (Lexer.WORD): #Word Token handling
                first = self.currentToken
                self.advance()
                if self.currentToken.type == (Lexer.WORD):
                    last = self.currentToken
                    full = self.fullName(first, last)
            elif self.currentToken.type == Lexer.NEWTRANS:
                trans = Nodes.TransactionNode(full, op)
                transList.append(trans)
                self.advance()
            else:
                self.advance()
        return transList
