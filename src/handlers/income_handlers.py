from src.models.income import Income
import uuid
from datetime import datetime


# commands = [
#         telebot.types.BotCommand('add_income', 'Добавить доход'),
#         telebot.types.BotCommand('delete_income', 'Удалить доход'),
#         telebot.types.BotCommand('change_income', 'Изменить доход'),
#         telebot.types.BotCommand('income_history', 'Вывести отчет о доходах'),
#     ]

def find_income_by_id(id_income, session):
    income = session.query(Income).get(id_income)

    return income


def parse_content(content):
    values = {'NAM': None, 'VAL': None, 'CUR': None}

    parts = content.split()

    for part in parts:
        if part.startswith("NAM:"):
            values['NAM'] = part.split(":")[1].strip()
        elif part.startswith("VAL:"):
            values['VAL'] = part.split(":")[1].strip()
        elif part.startswith("CUR:"):
            values['CUR'] = part.split(":")[1].strip()

    return {k: v for k, v in values.items() if v is not None}


def get_parsed_values(content):
    parsed_content = parse_content(content)

    name = None
    value = None
    currency = None

    try:
        name = parsed_content.get('NAM')
        value = parsed_content.get('VAL')
        currency = parsed_content.get('CUR')
    except KeyError:
        print('Такого ключа не существует')

    return name, value, currency


class IncomeHandler:

    @staticmethod
    def add_income(content, session):
        id_income = uuid.uuid4()
        name, value, currency = get_parsed_values(content)
        created_date = datetime.now()
        income = Income(id_income, name, value, currency, created_date, created_date)

        session.add(income)
        session.commit()

    @staticmethod
    def delete_income(id_income, session):
        if (income := find_income_by_id(id_income, session)) is not None:
            session.delete(income)
            session.commit()

    @staticmethod
    def change_income(id_income, content, session):
        if (income := find_income_by_id(id_income, session)) is not None:
            name, value, currency = get_parsed_values(content)

            if name is not None:
                income.name = name
            if value is not None:
                income.value = value
            if currency is not None:
                income.currency = currency

            modified_date = datetime.now()
            income.modified_date = modified_date

            session.commit()

    #TODO: Доделать, когда связь м/у таблицами репортов и дохода будет проработана
    @staticmethod
    def get_income_report(id_income, session):
        pass
