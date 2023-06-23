from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyBoard:

    @staticmethod
    def generate_income_keyboard(row_width, content_list):
        keyboard = InlineKeyboardMarkup(row_width=row_width)

        for content in content_list:
            button = InlineKeyboardButton(content["NAME"], callback_data=content["ID"])
            keyboard.add(button)

        return keyboard
