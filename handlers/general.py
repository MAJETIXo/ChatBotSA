from aiogram import types
from loader import dp
from db.db_api_users import db_api_users
from db.db_api_serial import db_api_serial
from db.db_api_anime import db_api_anime
import datetime


# Проверяем имеется ли сериал в списке отслеживаемого у пользователя
def check_title(title, target_titles):
    for element in target_titles:
        if title in element:
            return True
    return False


# Команда /info - Выводим список всех сериалов, который добавил к себе пользователь
@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):

    user_info = db_api_users().get_user_info(message.from_user.id)
    if user_info:
        serial_titles = db_api_serial().get_user_info(user_info.id)
        anime_titles = db_api_anime().get_user_info(user_info.id)
        if serial_titles or anime_titles:
            for title in serial_titles:
                await message.answer(f"Название: {title[0]}\n"
                                     f"Рейтинг IMDB: {title[1]} из 10\n"
                                     f"Жанры: {title[2]}\n"
                                     f"Дата выхода следующей"
                                     f" серии: {datetime.datetime.strptime(title[3], '%Y-%m-%d').strftime('%d.%m.%Y')}.")

            for title in anime_titles:
                await message.answer(f"Название: {title[0]}\n"
                                     f"Жанры: {title[1]}\n"
                                     f"Возврастной рейтинг: {title[2]}\n"
                                     f"Дата выхода следующей"
                                     f" серии: {datetime.datetime.strptime(title[3], '%Y-%m-%d').strftime('%d.%m.%Y')}.")
        else:
            await message.answer("Может добавишь что-нибудь в свой список?")
    else:
        await message.answer("Может стоит для начала познакомиться со мной?(введи команду /start).")


# Команда /delete - Удаляем сериал из списка отслеживаемого
@dp.message_handler(commands=['delete'])
async def process_delete_command(message: types.Message):
    user_info = db_api_users().get_user_info(message.from_user.id)

    if user_info:
        serial_titles = db_api_serial().get_user_info(user_info.id)
        anime_titles = db_api_anime().get_user_info(user_info.id)

        title = str(message.text[8:]).strip()

        if title != "":
            if check_title(title, serial_titles):
                db_api_serial().delete(user_info.id, title)
                await message.answer(f"Сериал {title} удален из списка отслеживаемого.")
            elif check_title(title, anime_titles):
                db_api_anime().delete(user_info.id, title)
                await message.answer(f"Аниме {title} удалено из списка отслеживаемого.")
            else:
                await message.answer(f"Сериал {title} не находится в вашем списке отслеживаемого.")
        else:
            await message.answer(f"Неправильно используется команда /delete, воспользуйтесь /help для того,"
                                 f" чтобы ознакомиться с возможностями бота.")
    else:
        await message.answer("Может стоит для начала познакомиться со мной?(введи команду /start).")


# Команда /leave - Удаляем пользователя из БД, если он не хочет пользоваться нашим ботом
@dp.message_handler(commands=['leave'])
async def process_leave_command(message: types.Message):
    user_info = db_api_users().get_user_info(message.from_user.id)
    if user_info:
        db_api_users().delete_user(message.from_user.id)
        await message.answer("Ну ладно, пока, но если я тебе понадоблюсь снова, просто введи команду /start.")
    else:
        await message.answer("Может стоит для начала познакомиться со мной?(введи команду /start).")
