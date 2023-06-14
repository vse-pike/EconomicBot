import xml.etree.ElementTree as Et

from curency import Currency


class CbrParser:

    def __init__(self, raw_body):
        self.prepared_xml = Et.fromstring(raw_body)

    def parse_xml_and_get_currencies(self):
        currencies = []

        for valute in self.prepared_xml.findall('Valute'):
            num_code = valute.find('NumCode').text
            char_code = valute.find('CharCode').text
            nominal = valute.find('Nominal').text
            name = valute.find('Name').text
            value = valute.find('Value').text

            currency = Currency(num_code, char_code, nominal, name, value)
            currencies.append(currency)

        return currencies

    @staticmethod
    def get_currency_by_char_code(currencies, char_code):
        for currency in currencies:
            if currency.char_code == char_code:
                return currency
