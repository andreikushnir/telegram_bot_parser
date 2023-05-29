import requests
from bs4 import  BeautifulSoup
import os
import asyncio
from create_bot import bot
from keyboards.inline_user import *
from data.data import *
import time


url = "https://www.pravda.com.ua/rus/news/"

async def check_process():
    while True:

        sql = """SELECT * from articles """
        cur_base.execute(sql)
        records = cur_base.fetchall()
        for row in records:
            end_time = float(time.time()) - float(row[6])
            if end_time >= 208000:
                connector.delete_article_by_link(link=row[1])
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.text
                soup = BeautifulSoup(result, 'html.parser')
                article_blocks = soup.find_all('div', class_='article_news_list')

                for block in article_blocks:
                    article_link = block.find('div', class_='article_header').a['href']
                    article_time = block.find('div', class_='article_time').text
                    article_text = block.find('div', class_='article_header').a.text

                    if not article_link.startswith('https://'):
                        if connector.get_article_by_link_chat(link=article_link, fields='link') != article_link:
                            result = requests.get(f"https://www.pravda.com.ua{article_link}").text
                            soup_page = BeautifulSoup(result, 'html.parser')
                            post_text = soup_page.find('div', class_='post_text')
                            img_tag = soup_page.find('img', class_='post_photo_news_img')
                            file_name = ''

                            if img_tag is not None:
                                image_url = img_tag['src']
                                folder_path = "data/media"
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)
                                file_name = os.path.basename(image_url)
                                file_path = os.path.join(folder_path, file_name)
                                response = requests.get(image_url)

                                with open(file_path, "wb") as file:
                                    file.write(response.content)

                            text_with_spaces = '\n'.join(
                                [f"{' '.join(p.stripped_strings)}" for p in post_text.find_all('p')])

                            sql = """SELECT * from users """
                            cur_base.execute(sql)
                            records = cur_base.fetchall()

                            file_path = f'data/media/{file_name}'
                            trimmed_text =  f'{article_text}\n\n' \
                                            f'{text_with_spaces[:900]}'
                            for row in records:
                                if img_tag is not None:
                                    photo = open(file_path, 'rb')
                                    await bot.send_photo(chat_id=int(row[0]), photo=photo, caption=trimmed_text,reply_markup=user_inlines.news(article_link=article_link))
                                    photo.close()
                                    try:
                                        os.remove(file_path)
                                    except OSError as e:
                                        pass
                                else:
                                    await bot.send_message(int(row[0]), trimmed_text,reply_markup=user_inlines.news(article_link=article_link))

                            connector.insert_article(link=article_link, datetime=article_time, title=article_text, description=text_with_spaces, photo=file_name)
            else:
                print("Ошибка при обращении по ссылке.")
        except requests.exceptions.RequestException:
            print("Невозможно подключиться к серверу.")

        await asyncio.sleep(1000)
