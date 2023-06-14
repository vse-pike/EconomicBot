from _decimal import Decimal


class Income:

    def __init__(self, value, currency):
        self.value = Decimal(value)
        self.currency = currency
