'''
Chase Dallmann & John Petrie
4/28/2024
Token
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

#Creating a token
class Token:
    def __init__(self, tokenType, value=None):
        self.type = tokenType
        self.value = value

    def __repr__(self):
        if self.value:
            return f'Token({self.type}, {self.value})'
