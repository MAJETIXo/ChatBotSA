import datetime
from db.db_api_anime import db_api_anime


# Проверяем выходит ли сегодня какая-либо новая серия аниме
def send_today(current_date: datetime) -> bool:
    release_dates = db_api_anime().get_releases()
    for date in release_dates:
        if current_date in date:
            return True


# Получаем тайтлы, которые выходят сегодня
def get_titles(current_date: datetime) -> tuple:
    titles = db_api_anime().get_titles(current_date)
    return titles


# Собираем все вместе
async def run() -> tuple:
    dt = str(datetime.date.today())
    result = get_titles(dt) if send_today(dt) else None
    return result







