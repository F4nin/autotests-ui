class UpperPrintString(str):
    def __new__(cls, obj):
        instance = super().__new__(cls, obj)
        return instance

    def __str__(self):
        return f'{super().__str__().upper()}'


class LowerString(str):
    def __new__(cls, value):
        instance = super().__new__(cls, value.lower())
        return instance

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{super().__str__()}'


