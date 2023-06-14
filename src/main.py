from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from application import Application
import telebot

if __name__ == '__main__':
    bot = telebot.TeleBot("6298565882:AAEbeyIie_F1xL-9QKOu0G03TwjjS95tUgk", parse_mode=None)

    app = Application()

    user_information = {}

    menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_currency = KeyboardButton('Вывести актуальный курс')
    button_salary = KeyboardButton('Вывести актуальную зп')
    button_update_currencies = KeyboardButton('Изменить отслеживаемые валюты')
    button_update_salary = KeyboardButton('Изменить установленную зп')
    menu_buttons.add(button_currency, button_salary, button_update_currencies, button_update_salary)


    @bot.message_handler(commands=['start'])
    def start_bot(message):
        if message.from_user.id == 266532751:
            bot.send_message(message.from_user.id, "Введите свою зп c валютой: ")
            bot.register_next_step_handler(message, get_salary_information)


    @bot.message_handler(func=lambda message: True)
    def callback_handler(message):
        if message.from_user.id == 266532751:
            if message.text == 'Вывести актуальный курс':
                reports = app.rate_report()
                pretty_report = '\n'.join(reports)
                bot.send_message(message.chat.id, pretty_report)
            elif message.text == 'Вывести актуальную зп':
                reports = app.salary_report()
                pretty_report = '\n'.join(reports)
                bot.send_message(message.chat.id, pretty_report)
            elif message.text == 'Изменить отслеживаемые валюты':
                bot.send_message(message.from_user.id, "Введите отслеживаемые валюты: ")
                bot.register_next_step_handler(message, update_assigned_currencies)
            elif message.text == 'Изменить установленную зп':
                bot.send_message(message.from_user.id, "Введите свою зп c валютой: ")
                bot.register_next_step_handler(message, update_salary_information)
            else:
                bot.send_message(message.chat.id, "Неизвестная команда")
        else:
            bot.send_message(message.chat.id, "Доступ запрещен")


    def update_salary_information(message):
        salary = message.text.split()

        user_information["value"] = salary[0]
        user_information["currency"] = salary[1]

        app.update_salary(user_information)


    def update_assigned_currencies(message):
        currencies = message.text.split()

        user_information["currencies"] = currencies

        app.update_currencies(user_information)


    def get_salary_information(message):
        salary = message.text.split()

        user_information["value"] = salary[0]
        user_information["currency"] = salary[1]

        bot.send_message(message.from_user.id, "Введите отслеживаемые валюты: ")

        bot.register_next_step_handler(message, get_assigned_currencies)


    def get_assigned_currencies(message):
        currencies = message.text.split()

        user_information["currencies"] = currencies

        bot.send_message(message.from_user.id, "Сбор информации завершен", reply_markup=menu_buttons)

        app.start(user_information)


    bot.infinity_polling()
