import Token

PLUS = '+',
MINUS = '-'
MULTIPLY = '*'
DIVIDE = '/'
MODULO = '%'
LEFTPAREN = '('
RIGHTPAREN = ')'
COMMA = ','
PERIOD = '.'
SEMICOLON = ';'
COLON = ':'
DOLLARSIGN = '$'
DIGITS = '0123456789'
INT = 'INT'
FLOAT = 'FLOAT'


########################## ERROR HANDLING ##########################
class Error:  # Class for Error Handling
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File{self.pos_start.fileName}:Line {self.pos_start.line + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


########################## CHARACTER POSITION ##########################
class Position:
    def __init__(self, index, line, column, fileName, fileText):
        self.index = index
        self.line = line
        self.column = column
        self.fileName = fileName
        self.fileText = fileText

    def advance(self, currentChar):  # Advancing the current char
        self.index += 1
        self.column += 1

        if currentChar == "\n":  # If a newline token is discovered increment the line by 1 and reset the column
            self.line += 1
            self.column = 0

        return self

    # Copying the position and returning it as a new object
    def copy(self):
        return Position(self.index, self.line, self.column, self.fileName, self.fileText)


# The Lexer class
class Lexer:
    def __init__(self, file_name, text):
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)  # Creating a position object
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
            '/': Token.Token(DIVIDE, '/'),
            '%': Token.Token(MODULO, '%'),
            '(': Token.Token(LEFTPAREN, '('),
            ')': Token.Token(RIGHTPAREN, ')'),
            ',': Token.Token(COMMA, ','),
            ';': Token.Token(SEMICOLON, ';'),
            ':': Token.Token(COLON, ':'),
            '.': Token.Token(PERIOD, '.'),
            '$': Token.Token(DOLLARSIGN, '$'),
            ' ': None,
            '\t': None
        }

        while self.currentChar is not None:
            if self.currentChar.isdigit():
                tokens.append(self.makeNumber())
            elif self.currentChar in charDictionary:
                if charDictionary[self.currentChar] is not None:
                    tokens.append(charDictionary[self.currentChar])
                self.advance()
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


# A function to run the file
def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.makeTokens()

    return tokens, error
