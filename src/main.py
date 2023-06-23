from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import time
import telebot

from src.db.db_settings import Db
from src.handlers.income_handlers import IncomeHandler
from src.handlers.user_handler import UserHandler
from src.view.keyboard import KeyBoard

if __name__ == '__main__':
    session = Db().session

    # TODO: Убрать хардкод
    bot = telebot.TeleBot("5935761898:AAGzVoZToD9ttlbcjJ_bF5SypJQ7tPTaS-w", parse_mode=None)

    commands = [
        telebot.types.BotCommand('add_income', 'Добавить доход'),
        # telebot.types.BotCommand('add_investment', 'Добавить инвестицию'),
        telebot.types.BotCommand('delete_income', 'Удалить доход'),
        # telebot.types.BotCommand('delete_investment', 'Удалить инвестицию'),
        # telebot.types.BotCommand('add_new_report', 'Добавить новый отчет'),
        telebot.types.BotCommand('change_income', 'Изменить доход'),
        # telebot.types.BotCommand('income_history', 'Вывести отчет о доходах'),
        # telebot.types.BotCommand('investment_history', 'Вывести отчет об инвестициях')
    ]


    @bot.message_handler(commands=['start'])
    def start_bot(message):
        # TODO: Убрать хардкод
        # TODO: Добавить авторизацию
        if message.from_user.id == 266532751:
            bot.send_message(message.from_user.id, "Инициализация бота")
            bot.set_my_commands(commands)

        UserHandler.add_user(message.from_user.id, session)


    @bot.message_handler(commands=['add_income'], content_types=['text'])
    def add_income_bot(command):
        chat_id = command.from_user.id
        bot.delete_message(chat_id, command.message_id)
        message_from_bot_start = bot.send_message(command.from_user.id,
                                                  "Введите отслеживаемый доход в формате: NAM:Название VAL:Сумма CUR:Валюта")

        @bot.message_handler(content_types=['text'])
        def income_message(message):
            income_text = message.text
            IncomeHandler.add_income(income_text, chat_id, session)
            bot.delete_message(chat_id, message_from_bot_start.message_id)
            bot.delete_message(chat_id, message.message_id)
            message_from_bot_end = bot.send_message(command.from_user.id, "Добавлен новый доход")
            time.sleep(3)
            bot.delete_message(chat_id, message_from_bot_end.message_id)


    @bot.message_handler(commands=['delete_income'])
    def delete_income_bot(command):
        chat_id = command.from_user.id
        bot.delete_message(chat_id, command.message_id)

        income_list = IncomeHandler.get_income_list(chat_id, session)

        keyboard = KeyBoard.generate_income_keyboard(2, income_list)

        bot.send_message(chat_id, "Выберите доход для удаления:", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def handle_income_button_click(call):
            income_id = call.data
            IncomeHandler.delete_income(income_id, session)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            message_from_bot = bot.send_message(command.from_user.id, "Доход удален")
            time.sleep(3)
            bot.delete_message(chat_id, message_from_bot.message_id)


    @bot.message_handler(commands=['change_income'])
    def change_income_bot(command):
        chat_id = command.from_user.id
        bot.delete_message(chat_id, command.message_id)

        income_list = IncomeHandler.get_income_list(chat_id, session)

        keyboard = KeyBoard.generate_income_keyboard(2, income_list)

        bot.send_message(chat_id, "Выберите доход для изменения:", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def handle_income_button_click(call):
            income_id = call.data
            bot.delete_message(call.message.chat.id, call.message.message_id)

            @bot.message_handler(content_types=['text'])
            def income_message(message):
                income_text = message.text
                IncomeHandler.change_income(income_id, income_text, session)
                message_from_bot = bot.send_message(command.from_user.id, "Доход изменен")
                time.sleep(3)
                bot.delete_message(chat_id, message_from_bot.message_id)

        # @bot.message_handler(content_types=['text'])
        # def income_message(message):
        #     income_text = message.text
        #     # TODO: Убрать хардкод
        #     IncomeHandler.change_income('273e6823-acc5-473f-9b92-788a570b3f9f', income_text, session)
        #     bot.send_message(command.from_user.id, "Изменен доход")


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
