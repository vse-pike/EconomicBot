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
    content


class IncomeHandler:

    @staticmethod
    def add_income(content, session):
        id_income = uuid.uuid4()
        value, currency = content.split()
        created_date = datetime.now()
        income = Income(id_income, value, currency, created_date, created_date)

        session.add(income)
        session.commit()

    @staticmethod
    def delete_income(id_income, session):
        if (income := find_income_by_id(id_income, session)) is not None:
            session.delete(income)
            session.commit()

    # @staticmethod
    # def change_income(id_income, content, session):
    #     if (income := find_income_by_id(id_income, session)) is not None:
    #         value, currency = content.split()
    #         income.value =
