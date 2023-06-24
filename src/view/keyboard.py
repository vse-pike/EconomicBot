from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyBoard:

    @staticmethod
    def generate_income_keyboard(row_width, command_init, content_list):
        keyboard = InlineKeyboardMarkup(row_width=row_width)

        for content in content_list:
            button = InlineKeyboardButton(content["NAME"], callback_data=f"{command_init}:{content['ID']}")
            keyboard.add(button)

        return keyboard
