import time
import telebot
from dotenv import load_dotenv
import os

from src.db.db_settings import Db
from src.handlers.income_handlers import IncomeHandler
from src.handlers.user_handler import UserHandler
from src.view.keyboard import KeyBoard

if __name__ == '__main__':
    load_dotenv()
    # Получение значения токена бота из переменных окружения
    bot_token = os.getenv("BOT_TOKEN")
    print("ВЫЖДЛФЖВЫДЛ")
    print(bot_token)
    print(Exception(bot_token))
    print("End")

    session = Db().session

    # TODO: Убрать хардкод
    bot = telebot.TeleBot(bot_token, parse_mode=None)

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
        bot.send_message(message.from_user.id, "Инициализация бота")
        bot.set_my_commands(commands)
        UserHandler.add_user(message.from_user.id, session)



    @bot.message_handler(commands=['add_income'], content_types=['text'])
    def add_income_bot(command):
        chat_id = command.from_user.id
        bot.send_message(command.from_user.id,
                         "Введите отслеживаемый доход в формате: NAM:Название VAL:Сумма CUR:Валюта")

        @bot.message_handler(content_types=['text'])
        def income_message(message):
            income_text = message.text
            try:
                IncomeHandler.add_income(income_text, chat_id, session)
                bot.send_message(command.from_user.id, "Добавлен новый доход")
                time.sleep(3)
            except Exception as e:
                bot.send_message(command.from_user.id, "Ошибка добавления дохода:" + str(e))


    # Хендлер для обработки запроса: удаления дохода
    @bot.message_handler(commands=['delete_income'])
    def delete_income_bot(command):
        chat_id = command.from_user.id
        try:
            income_list = IncomeHandler.get_income_list(chat_id, session)

            keyboard = KeyBoard.generate_income_keyboard(2, "delete_income", income_list)

            bot.send_message(chat_id, "Выберите доход для удаления:", reply_markup=keyboard)
        except Exception as e:
            bot.send_message(command.from_user.id, "Ошибка удаления дохода:" + str(e))




    # Хендлер для обработки запроса: изменения существующего запроса
    @bot.message_handler(commands=['change_income'])
    def change_income_bot(command):
        chat_id = command.from_user.id
        income_list = IncomeHandler.get_income_list(chat_id, session)

        keyboard = KeyBoard.generate_income_keyboard(2, "change_income", income_list)

        bot.send_message(chat_id, "Выберите доход для изменения:", reply_markup=keyboard)


    # Обработчик для кнопок выбора дохода
    @bot.callback_query_handler(func=lambda call: True)
    def handle_income_button_click(call):
        income_id = call.data.split(":")[1]
        chat_id = call.message.chat.id

        if call.data.startswith("delete_"):
            # Обработчик для удаления дохода
            IncomeHandler.delete_income(income_id, session)
            bot.send_message(chat_id, "Доход удален")
            time.sleep(3)
        elif call.data.startswith("change_"):
            bot.send_message(chat_id, "Введите изменяемый доход в формате: NAM:Название VAL:Сумма CUR:Валюта")
            bot.send_message(chat_id, "Неизменяемый значения можно пропустить")

            # Обработчик для изменения дохода
            @bot.message_handler(content_types=['text'])
            def income_message(message):
                income_text = message.text
                IncomeHandler.change_income(income_id, income_text, session)
                bot.send_message(chat_id, "Доход изменен")
                time.sleep(3)


    # TODO: Реализовать чистку сообщений после выполнения команды

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
