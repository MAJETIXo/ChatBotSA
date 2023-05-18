from db.db_api import db_api


class db_api_serial(db_api):

    # Добавляем сериал в таблицу serial_titles
    def add(self, data: list):
        self.cur.execute("INSERT INTO serial_titles(user_id, title, rating_imdb, genres, releases) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()

    # Получаем сериалы, которые добавил пользователь к себе в список
    def get_user_title(self, user_id: str) -> tuple:
        self.cur.execute("SELECT title FROM serial_titles WHERE user_id=?;", (user_id,))

        result = ()
        for title in self.cur.fetchall():
            result += title

        return result

    # Получаем данные о сериалах, которые отслеживает определенный пользователь
    def get_user_info(self, user_id: str) -> tuple:
        self.cur.execute("SELECT title, rating_imdb, genres, releases FROM serial_titles WHERE user_id=?;", (user_id,))
        return self.cur.fetchall()

    # Удаляем сериал из отслеживаемого у определенного пользователя
    def delete(self, user_id: str, title: str):
        self.cur.execute("DELETE FROM serial_titles WHERE user_id=? and title=?;", (user_id, title, ))
        self.conn.commit()

    # Получаем даты всех релизов сериалов
    def get_releases(self) -> list:
        self.cur.execute("SELECT DISTINCT releases FROM serial_titles")
        return self.cur.fetchall()

    # Получаем тайтлы, которые выходят в определенную дату
    def get_titles(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT title FROM serial_titles WHERE releases = ?;", (date,))

        data = ()

        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Получаем user_id пользователей, которым нужно будет отправлять уведомление
    def get_userid_notify(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT user_id FROM serial_titles WHERE title "\
                         "IN (SELECT DISTINCT title FROM serial_titles WHERE releases = ?);", (date,))
        data = ()
        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Обновляем данные о сериале
    def update_table(self, date: str, title: str):
        self.cur.execute("UPDATE serial_titles SET releases=? WHERE title=?", (date, title,))
        self.conn.commit()

    # Удаляем данные по определенному сериалу
    def delete_column(self, title: str):
        self.cur.execute("DELETE FROM serial_titles WHERE title=?", (title,))
        self.conn.commit()


