class Token:
    def __init__(self, tokenType, value=None):
        self.value = value
        self.type = tokenType

    def __repr__(self):
        if self.value:
            return f'Token({self.type}, {self.value})'
        return f'{self.type}'
