from cbr_parser import CbrParser
from income import Income
from valute import get_valutes_cbr


class Application:

    def __init__(self):
        self.income = None
        self.assigned_currencies = None

    def start(self, user_information):
        self.assigned_currencies = user_information.get('currencies')
        self.income = Income(user_information.get('value').replace(",", "."), user_information.get('currency'))

        if self.income.currency not in self.assigned_currencies:
            self.assigned_currencies.append(self.income.currency)

    def salary_report(self):
        reports = []

        actual_rates = self.get_actual_rates_with_currencies()

        income_rub = actual_rates.get(self.income.currency) * self.income.value
        formatted_income = "{:,}".format(income_rub.__round__()).replace(",", " ")
        reports.append(f"Ваша зп в валюте RUB: {formatted_income}")

        for key in actual_rates:
            rate = actual_rates.get(key)
            calculated_income = self.calculate_salary(rate, income_rub)
            formatted_income = "{:,}".format(calculated_income.__round__()).replace(",", " ")
            reports.append(f"Ваша зп в валюте {key}: {formatted_income}")

        return reports

    def rate_report(self):
        reports = []

        actual_rates = self.get_actual_rates_with_currencies()

        for key in actual_rates:
            reports.append(f"Курс {key}/RUB: {actual_rates.get(key)}")

        return reports

    def get_actual_rates_with_currencies(self):
        actual_rates = {}

        response = get_valutes_cbr()

        cbr_parser = CbrParser(response)
        currencies = cbr_parser.parse_xml_and_get_currencies()

        for char_code in self.assigned_currencies:
            currency = cbr_parser.get_currency_by_char_code(currencies, char_code)
            actual_rates[currency.char_code] = currency.rate

        return actual_rates

    def update_currencies(self, user_information):
        self.assigned_currencies = user_information.get('currencies')

        if self.income.currency not in self.assigned_currencies:
            self.assigned_currencies.append(self.income.currency)

    def update_salary(self, user_information):
        self.income = Income(user_information.get('value').replace(",", "."), user_information.get('currency'))

        if self.income.currency not in self.assigned_currencies:
            self.assigned_currencies.append(self.income.currency)

    def calculate_salary(self, rate, income_rub):
        k = 1 / rate
        return income_rub * k
