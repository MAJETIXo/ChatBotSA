from db.db_api_users import db_api_users
from db.db_api_serial import db_api_serial
from db.db_api_anime import db_api_anime
from tasks.anime_check import run as anime_run
from tasks.serial_check import run as serial_run
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from parser.anime import Anime
from parser.serials import Serials
import datetime


# Изменяем данные в таблице anime_titles
def update_anime_table(target_titles: tuple):
    for title in target_titles:
        anime = Anime("https://animego.org/search/all?q=")
        result = anime.run(title)
        if type(result) is list and result is not None:
            db_api_anime().update_table(result[3], result[0])
        elif type(result) is str:
            db_api_anime().delete_column(title)


# Изменяем данные в таблице serial_titles
def update_serial_table(target_titles: tuple):
    for title in target_titles:
        serial = Serials("https://myshows.me/search/all/")
        result = serial.run(title)
        if type(result) is list and result is not None:
            db_api_serial().update_table(result[3], result[0])
        elif type(result) is str:
            db_api_serial().delete_column(title)


# Отправляем сообщение о выходе новых серий аниме соответствующим пользователям
async def send_msg_anime():
    target_titles = await anime_run()
    today = datetime.datetime.now().strftime("%Y-%m-%#d")
    if target_titles:
        users = db_api_anime().get_userid_notify(today)
        for user in users:
            user_titles = db_api_anime().get_user_info(user)
            for title in user_titles:
                if title[0] in target_titles:
                    chat_id = db_api_users().get_userid_for_bot(user)[0]
                    await bot.send_message(chat_id, f"Сегодня выйдет новая серия аниме \"{title[0]}\"!")
        update_anime_table(target_titles)


# Отправляем сообщение о выходе новых серий сериалов соответствующим пользователям
async def send_msg_serial():
    target_titles = await serial_run()
    today = str(datetime.date.today())
    if target_titles:
        users = db_api_serial().get_userid_notify(today)
        for user in users:
            user_titles = db_api_serial().get_user_info(user)
            for title in user_titles:
                if title[0] in target_titles:
                    chat_id = db_api_users().get_userid_for_bot(user)[0]
                    await bot.send_message(chat_id, f"Сегодня выйдет новая серия сериала \"{title[0]}\"!")
        update_serial_table(target_titles)


# Запускаем функции send_msg_anime и send_msg_serial с интервалом в один день.
scheduler = AsyncIOScheduler()

scheduler.add_job(send_msg_anime, "cron", hour=12, minute=0)
scheduler.add_job(send_msg_serial, "cron", hour=12, minute=0)

scheduler.start()
