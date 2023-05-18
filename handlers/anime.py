from aiogram import types
from loader import dp
from parser.anime import Anime
from db.db_api_users import db_api_users
from db.db_api_anime import db_api_anime


# Команда /add_anime - добавляет аниме в БД
@dp.message_handler(commands=['add_anime'])
async def process_add_anime_command(message: types.Message):

    user_info = db_api_users().get_user_info(message.from_user.id)

    if user_info:
        title = str(message.text[11:]).strip()

        titles_info = db_api_anime().get_user_info(user_info.id)

        merge_titles_info = []
        for element in titles_info:
            merge_titles_info += element

        merge_titles_info = [element.lower() for element in merge_titles_info]

        if title != "":
            await message.answer(f"Тааак, сейчас посмотрим...")
            if title.lower() not in merge_titles_info:
                anime = Anime("https://animego.org/search/all?q=")
                result = anime.run(title)
                if type(result) is str:
                    await message.answer(result)
                else:
                    db_api_anime().add([user_info.id] + result)
                    await message.answer(f"Аниме {title} Добавлено в список отслеживаемого.")
            else:
                await message.answer(f"Аниме {title} уже есть в вашем списке.")
        else:
            await message.answer(f"Неправильно используется команда /add_anime, воспользуйтесь командой /help "
                                 f"чтобы ознакомиться с возможностями бота.")
    else:
        await message.answer("Может стоит для начала познакомиться со мной?(введи команду /start).")