'''
Chase Dallmann & John Petrie
4/28/2024
Lexer
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

import Token
import re

# Defining all the Tokens Types that can exist
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
DROP = 'DROP'
VIEW = 'VIEW'


class Error:  # Class for Error Handling
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result


# Creating an IllegalCharError incase a character is entered that can't be handled
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


# Handling the tracking of the current character by index, line, and column
class Position:
    def __init__(self, index, line, column, text):
        self.index = index
        self.line = line
        self.column = column
        self.text = text

    # A function to advance to the next character
    def advance(self, currentChar):
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
        self.pos = Position(-1, 0, -1, text)  # Creating a position object starting at the first character in the text
        self.currentChar = None
        self.advance()

    # Advancing the position of the Lexer by 1 from the current character
    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    # Creating an array of tokens
    def makeTokens(self):
        tokens = []  # Start with a blank token Array

        # A dictionary to create TOKENS based in their KEY/VALUE if the lexer encounters this character
        charDictionary = {
            '+': Token.Token(PLUS, '+'),
            '-': Token.Token(MINUS, '-'),
            '*': Token.Token(MULTIPLY, '*'),
            '.': Token.Token(PERIOD, '.'),
            '$': Token.Token(DOLLARSIGN, '$'),
            'ID': Token.Token(ID, 'ID'),
            '\n': Token.Token(NEWTRANS, '~'),
            ' ': None,
            '\t': None
        }

        while self.currentChar is not None:  # Making sure a character is trying to be read and not blank
            if self.currentChar.isdigit():  # Checking to see if the character is a digit
                tokens.append(self.makeNumber())
            elif re.match("[a-zA-Z]", self.currentChar):  # Seeing if a character is a-z or A-Z
                match = re.match('\\d', self.text[self.pos.index + 2])  # Checking to see what the 3rd char is
                if match and self.text[self.pos.index + 2] == match.group(
                        0):  # If the 3rd character is a digit we can make an ID token
                    tokens.append(self.makeID())
                else:
                    tokens.append(self.makeWord())  # Make a word token
            elif self.currentChar in charDictionary:  # Checking to see if the current char exists in the dictionary
                if charDictionary[self.currentChar] is not None:
                    tokens.append(charDictionary[self.currentChar])  # Add that token to the list if found
                self.advance()
            else:  # INVALID ENTRY: If none of the conditions are found create and error and return no tokens
                pos_start = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "' is not a valid character")

        return tokens, None

    # A function to create a number/float from a string
    def makeNumber(self):
        numberString = ''

        while self.currentChar is not None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.': # Checking for periods
                if "." in numberString:
                    raise IllegalCharError(self.pos.copy(), self.pos, "Multiple periods in number")
                numberString += '.'
            else:
                numberString += self.currentChar
            self.advance()

        if "." in numberString:
            return Token.Token(FLOAT, float(numberString)) 
        else:
            return Token.Token(INT, int(numberString))

    # A function to create a word token from letter characters
    def makeWord(self):
        wordString = ''
        while self.currentChar is not None and re.match("[a-zA-Z]", self.currentChar):
            wordString += self.currentChar
            self.advance()
        # Checking to see if the word is an operator word
        if wordString.lower() in ('deposited', 'deposit', 'deposits'):  # Deposit handling
            return Token.Token(PLUS, wordString)
        elif wordString.lower() in ('withdrew', 'withdraw', 'withdraws'):  # Withdraw handling
            return Token.Token(MINUS, wordString)
        elif wordString.lower() in ('accrued', 'accrue', 'accrues'):  # Intrest handling
            return Token.Token(MULTIPLY, wordString)
        elif wordString.lower() in ('create', 'open', 'creates', 'opens', 'opened'):  # Account Creation handling
            return Token.Token(CREATE, wordString)
        elif wordString.lower() in ('drop', 'close', 'drops', 'closes', 'closed'):  # Account Deletion handling
            return Token.Token(DROP, wordString)
        elif wordString.lower() in ('view', 'views', 'viewed'):  # View an account handling
            return Token.Token(VIEW, wordString)
        else:
            # If the word is not an operator word make it an agent name
            return Token.Token(WORD, wordString.upper())

    # A function to create an ID token from a string
    def makeID(self):
        idString = ''
        while self.currentChar is not None and re.match("[a-zA-Z\\d]", self.currentChar):
            idString += self.currentChar.upper()
            self.advance()
        return Token.Token(ID, idString)


# A function to create and run the lexer
def run(text):
        if text.strip() == '':
            print('No entry found')
            return '', None
        else:
            lexer = Lexer(text)
            result = lexer.makeTokens()
            if result is not None:
                tokens, error = result
            else:
                tokens = error = None
            return tokens, error
