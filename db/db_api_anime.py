from db.db_api import db_api


class db_api_anime(db_api):

    # Добавляем аниме в таблицу anime_titles
    def add(self, data: list):
        self.cur.execute("INSERT INTO anime_titles(user_id, title, genres, rating, release) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()

    # Получаем данные о аниме, которые отслеживает пользователь
    def get_user_info(self, user_id: str) -> list:
        self.cur.execute("SELECT title, genres, rating, release "
                         "FROM anime_titles WHERE user_id=?;", (user_id,))
        return self.cur.fetchall()

    # Удаляем аниме из отслеживаемого у определенного пользователя
    def delete(self, user_id: str, title: str):
        self.cur.execute("DELETE FROM anime_titles WHERE user_id=? and title=?;", (user_id, title, ))
        self.conn.commit()

    # Получаем даты всех релизов аниме
    def get_releases(self) -> list:
        self.cur.execute("SELECT DISTINCT release FROM anime_titles WHERE title IN (SELECT title FROM anime_titles);")
        return self.cur.fetchall()

    # Получаем все тайтлы, которые выходят в определенную дату
    def get_titles(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT title FROM anime_titles WHERE release = ?;", (date, ))

        data = ()

        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Получаем user_id пользователей, которым нужно будет отправлять уведомление
    def get_userid_notify(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT user_id FROM anime_titles WHERE title "\
                         "IN (SELECT DISTINCT title FROM anime_titles WHERE release = ?);", (date, ))
        data = ()
        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Изменяем значение в таблице anime_titles
    def update_table(self, date: str, title: str):
        self.cur.execute("UPDATE anime_titles SET release=? WHERE title=?", (date, title, ))
        self.conn.commit()

    # Удаляем данные по определенному аниме
    def delete_column(self, title: str):
        self.cur.execute("DELETE FROM anime_titles WHERE title=?", (title, ))
        self.conn.commit()