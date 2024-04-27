class Token:
    def __init__(self, tokenType, value=None):
        self.type = tokenType
        self.value = value

    def __repr__(self):
        if self.value:
            return f'Token({self.type}, {self.value})'
