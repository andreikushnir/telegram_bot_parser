from aiogram import types

class user_inlines:
    @staticmethod
    def news(article_link):
        keyboard = types.InlineKeyboardMarkup()
        news_open = (types.InlineKeyboardButton(text=f'Смотреть', url=f'https://www.pravda.com.ua{article_link}'))

        keyboard.add(news_open)

        return keyboard