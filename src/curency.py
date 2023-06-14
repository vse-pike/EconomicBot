
from _decimal import Decimal


class Currency:

    def __init__(self, num_code, char_code, nominal, name, value):
        self.num_code = num_code
        self.char_code = char_code
        self.nominal = Decimal(nominal)
        self.name = name
        self.value = Decimal(value.replace(',', '.')).quantize(Decimal('.0001'))
        self.rate = self.rate = self.value / self.nominal
