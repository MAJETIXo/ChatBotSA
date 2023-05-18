import datetime
from db.db_api_serial import db_api_serial


# Проверяем выходит ли сегодня новая серия какого-либо сериала
def send_today(current_date: str) -> bool:
    release_dates = db_api_serial().get_releases()
    for date in release_dates:
        if current_date in date:
            return True


# Получаем тайтлы, которые выходят сегодня
def get_titles(current_date: str) -> tuple:
    titles = db_api_serial().get_titles(current_date)
    return titles


# Собираем все вместе
async def run() -> tuple:
    dt = str(datetime.date.today())
    result = get_titles(dt) if send_today(dt) else None
    return result
