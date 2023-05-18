import sqlite3


# Класс для работы с БД
class db_api:

    # Подключаемся к нашей БД
    def __init__(self):
        self.conn = sqlite3.connect("db/notifier.db")
        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER UNIQUE NOT NULL, 
            join_date DATETIME DEFAULT 
            current_timestamp, 
            user_name TEXT);
        """)

        self.conn.commit()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS serial_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, title TEXT NOT NULL, 
            rating_imdb REAL, genres TEXT, 
            releases TEXT, 
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE);
        """)

        self.conn.commit()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS anime_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, 
            title TEXT NOT NULL, 
            genres TEXT NOT NULL, 
            rating TEXT NOT NULL, 
            "release" DATE, 
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE);
        """)

        self.conn.commit()

