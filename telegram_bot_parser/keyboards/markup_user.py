from aiogram.types import ReplyKeyboardMarkup


class user_markup:
    class buttons:
        channel = "💼Our channel"

    @staticmethod
    def menu():
        mark = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        mark.add(user_markup.buttons.channel)

        return mark