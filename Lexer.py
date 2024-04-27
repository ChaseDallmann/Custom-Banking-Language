import Token
import re

PLUS = '+'
MINUS = '-'
MULTIPLY = '*'
LEFTPAREN = '('
RIGHTPAREN = ')'
COMMA = ','
PERIOD = '.'
SEMICOLON = ';'
COLON = ':'
DOLLARSIGN = '$'
DIGITS = '0123456789'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
INT = 'INT'
FLOAT = 'FLOAT'
WORD = 'WORD'
NEWTRANS = '~'
ID = 'ID'
CREATE = 'CREATE'
REMOVE = 'REMOVE'
VIEW = 'VIEW'


########################## ERROR HANDLING ##########################
class Error:  # Class for Error Handling
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


########################## CHARACTER POSITION ##########################
class Position:
    def __init__(self, index, line, column, text):
        self.index = index
        self.line = line
        self.column = column
        self.text = text

    def advance(self, currentChar):  # Advancing the current char
        self.index += 1
        self.column += 1

        if currentChar == "\n":  # If a newline token is discovered increment the line by 1 and reset the column
            self.line += 1
            self.column = 0

        return self

    # Copying the position and returning it as a new object
    def copy(self):
        return Position(self.index, self.line, self.column, self.text)


# The Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1, text)  # Creating a position object
        self.currentChar = None
        self.advance()

    # Advancing the position of the lexer by 1
    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    # Creating an array of tokens
    def makeTokens(self):
        tokens = []  # Start with a blank token Array

        charDictionary = {
            '+': Token.Token(PLUS, '+'),
            '-': Token.Token(MINUS, '-'),
            '*': Token.Token(MULTIPLY, '*'),
            '(': Token.Token(LEFTPAREN, '('),
            ')': Token.Token(RIGHTPAREN, ')'),
            ',': Token.Token(COMMA, ','),
            ';': Token.Token(SEMICOLON, ';'),
            ':': Token.Token(COLON, ':'),
            '.': Token.Token(PERIOD, '.'),
            '$': Token.Token(DOLLARSIGN, '$'),
            'ID': Token.Token(ID, 'ID'),
            '\n': Token.Token(NEWTRANS, '~'),
            ' ': None,
            '\t': None
        }

        while self.currentChar is not None:
            if self.currentChar.isdigit():
                tokens.append(self.makeNumber())
            elif re.match("[a-zA-Z]",self.currentChar):
                match = re.match('\\d',self.text[self.pos.index + 2]) #Checking to see what the 3rd char is
                if match and self.text[self.pos.index + 2] == match.group(0):
                    tokens.append(self.makeID())
                else:
                    tokens.append(self.makeWord())
            elif self.currentChar in charDictionary:
                if charDictionary[self.currentChar] is not None:
                    tokens.append(charDictionary[self.currentChar])
                self.advance()
            #elif self.currentChar == '\n':
                #tokens.append(Token.Token(NEWTRANS, '\n'))
                #self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "' is not a valid character")

        return tokens, None

    # A function to create a number/float from a string
    def makeNumber(self):
        numberString = ''
        periodCount = 0

        while self.currentChar is not None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if periodCount > 0:
                    break
                periodCount += 1
                numberString += '.'
            else:
                numberString += self.currentChar
            self.advance()

        if periodCount == 0:
            return Token.Token(INT, int(numberString))
        elif periodCount == 1:
            return Token.Token(FLOAT, float(numberString))
        
    def makeWord(self):
        wordString = ''
        while self.currentChar is not None and re.match("[a-zA-Z]",self.currentChar):
            wordString += self.currentChar
            self.advance()

        if wordString.lower() == 'deposited':
            return Token.Token(PLUS, wordString)
        elif wordString.lower() == 'withdrew':
            return Token.Token(MINUS, wordString)
        elif wordString.lower() == 'accrued':
            return Token.Token(MULTIPLY, wordString)
        else:
            return Token.Token(WORD, wordString)

    def makeID(self):
        idString = ''
        while self.currentChar is not None and re.match("[a-zA-Z\\d]",self.currentChar):
            idString += self.currentChar
            self.advance()
        return Token.Token(ID, idString)

# A function to create and run the lexer
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.makeTokens()

    return tokens, error
