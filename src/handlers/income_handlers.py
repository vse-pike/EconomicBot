from src.models.income import Income
import uuid
from datetime import datetime
from sqlalchemy import text


# commands = [
#         telebot.types.BotCommand('add_income', 'Добавить доход'),
#         telebot.types.BotCommand('delete_income', 'Удалить доход'),
#         telebot.types.BotCommand('change_income', 'Изменить доход'),
#         telebot.types.BotCommand('income_history', 'Вывести отчет о доходах'),
#     ]

def get_incomes_by_condition(condition, session):
    incomes = session.query(Income).filter(text(condition)).all()

    return incomes


def get_income_by_condition(condition, session):
    income = session.query(Income).filter(text(condition)).first()

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
    # TODO: Реализовать обработку ошибок
    except KeyError:
        print('Такого ключа не существует')

    return name, value, currency


class IncomeHandler:

    @staticmethod
    def add_income(content, chat_id, session):
        id_income = uuid.uuid4()
        name, value, currency = get_parsed_values(content)
        created_date = datetime.now()
        income = Income(id_income, chat_id, name, value, currency, created_date, created_date)

        session.add(income)
        session.commit()

    @staticmethod
    def delete_income(id_income, session):
        condition = f"id_income = '{id_income}'"
        if (income := get_income_by_condition(condition, session)) is not None:
            session.delete(income)
            session.commit()
        # TODO: Проработать исключения

    @staticmethod
    def change_income(id_income, content, session):
        condition = f"id_income = '{id_income}'"
        if (income := get_income_by_condition(condition, session)) is not None:
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
        # TODO: Проработать исключения

    @staticmethod
    def get_income_list(chat_id, session):
        condition = f"id_user = {chat_id}"
        if (incomes := get_incomes_by_condition(condition, session)) is not None:
            incomes_list = []
            for income in incomes:
                income_dict = {"ID": str(income.id_income), "NAME": income.name}
                incomes_list.append(income_dict)

            # TODO: Проработать исключения

            return incomes_list

    # TODO: Доделать, когда связь м/у таблицами репортов и дохода будет проработана
    @staticmethod
    def get_income_report(id_income, session):
        pass
