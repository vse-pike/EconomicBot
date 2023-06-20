from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from application import Application
import telebot

from src.db.db_settings import Db
from src.handlers.income_handlers import IncomeHandler

if __name__ == '__main__':
    session = Db().session

    # Убрать хардкод
    bot = telebot.TeleBot("5935761898:AAGzVoZToD9ttlbcjJ_bF5SypJQ7tPTaS-w", parse_mode=None)

    commands = [
        telebot.types.BotCommand('add_income', 'Добавить доход'),
        telebot.types.BotCommand('add_investment', 'Добавить инвестицию'),
        telebot.types.BotCommand('delete_income', 'Удалить доход'),
        telebot.types.BotCommand('delete_investment', 'Удалить инвестицию'),
        telebot.types.BotCommand('add_new_report', 'Добавить новый отчет'),
        telebot.types.BotCommand('change_income', 'Изменить доход'),
        telebot.types.BotCommand('income_history', 'Вывести отчет о доходах'),
        telebot.types.BotCommand('investment_history', 'Вывести отчет об инвестициях')
    ]


    @bot.message_handler(commands=['start'])
    def start_bot(message):
        # Убрать хардкод
        if message.from_user.id == 266532751:
            bot.send_message(message.from_user.id, "Инициализация бота")
            co = bot.set_my_commands(commands)


    @bot.message_handler(commands=['add_income'], content_types=['text'])
    def add_income_bot(command):
        @bot.message_handler(content_types=['text'])
        def income_message(message):
            income_text = message.text
            IncomeHandler.add_income(income_text, session)
            bot.send_message(command.from_user.id, "Добавлен новый доход")


    @bot.message_handler(commands=['delete_income'])
    def delete_income_bot(command):

        #Реализовать удаление через кнопки по существующим доходам
        @bot.message_handler(content_types=['text'])
        def income_message(message):
            income_text = message.text
            IncomeHandler.delete_income(income_text, session)
            bot.send_message(command.from_user.id, "Удален доход")


    @bot.message_handler(commands=['add_investment'])
    def add_investment_bot(message):
        bot.send_message(message.from_user.id, "Добавлена новая инвестиция")


    @bot.message_handler(commands=['delete_investment'])
    def delete_investment_bot(message):
        bot.send_message(message.from_user.id, "Удалена инвестиция")


    @bot.message_handler(commands=['add_new_report'])
    def add_new_report_bot(message):
        bot.send_message(message.from_user.id, "Добавлен новый отчет")


    @bot.message_handler(commands=['change_income'])
    def change_income_bot(message):
        bot.send_message(message.from_user.id, "Изменен доход")


    @bot.message_handler(commands=['income_history'])
    def income_history_bot(message):
        bot.send_message(message.from_user.id, "Выведена история дохода")


    @bot.message_handler(commands=['investment_history'])
    def investment_history_bot(message):
        bot.send_message(message.from_user.id, "Выведена история инвестиций")


    bot.infinity_polling()
