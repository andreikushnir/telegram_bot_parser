import sqlite3
from random import randint
import time


data_base = sqlite3.connect('data/database.db', check_same_thread=False)
cur_base = data_base.cursor()
cur_base.execute('CREATE TABLE IF NOT EXISTS {}(id, link, datetime, title, description, photo, unix_time)'.format('articles'))
cur_base.execute('CREATE TABLE IF NOT EXISTS {}(id_chat, username, status)'.format('users'))
data_base.commit()

class SQLiteConnector:
    def __init__(self, db_path):
        self.db_path = db_path
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                conn.commit()
    def id_generation(self):
        id = randint(100000000, 999999999)
        return id
    def insert_article(self, link, datetime, title, description, photo):
        query = "INSERT INTO articles (id ,link, datetime, title, description, photo, unix_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
        unix_time = time.time()
        params = (self.id_generation(), link, datetime, title, description, photo, unix_time)
        self.execute_query(query, params)
    def delete_article_by_link(self, link):
        params = []
        query = f"DELETE FROM articles WHERE link=?"
        params.append(link)
        self.execute_query(query, params)
    def get_article_by_link_chat(self, link, fields=None):
        if fields is not None:
            query = f"SELECT {fields} FROM articles WHERE link=?"
            result = self.execute_query(query, (link,), fetch_one=True)
            if result is not None:
                return result[0]
        else:
            return None
    def update_article_by_link(self, link, title=None, description=None, photo=None):
        query = "UPDATE users SET "
        params = []
        if title is not None:
            query += "title=?, "
            params.append(title)
        if description is not None:
            query += "description=?, "
            params.append(description)
        if photo is not None:
            query += "photo=?, "
            params.append(photo)
        query = query.rstrip(", ") + " WHERE link=?"
        params.append(link)
        self.execute_query(query, tuple(params))
    def insert_users(self, id_chat, username, status):
        query = "INSERT INTO users (id_chat, username, status) VALUES (?, ?, ?)"
        params = (id_chat, username, status)
        self.execute_query(query, params)
    def get_users_by_id_chat(self, id_chat, fields=None):
        if fields is not None:
            query = f"SELECT {fields} FROM users WHERE id_chat=?"
            result = self.execute_query(query, (id_chat,), fetch_one=True)
            if result is not None:
                return result[0]
        else:
            return None
    def update_users_id_chat(self, id_chat, status=None):
        query = "UPDATE users SET "
        params = []
        if status is not None:
            query += "status=?, "
            params.append(status)
        query = query.rstrip(", ") + " WHERE id_chat=?"
        params.append(id_chat)
        self.execute_query(query, tuple(params))

db_path = "data/database.db"
connector = SQLiteConnector(db_path)