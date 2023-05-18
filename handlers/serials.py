from aiogram import types
from loader import dp
from parser.serials import Serials
from db.db_api_users import db_api_users
from db.db_api_serial import db_api_serial


def convert_to_lower(list_of_strings: tuple):
    list_of_strings = [string.lower() for string in list_of_strings]
    return list_of_strings


# Команда /add_serial - добавляет сериал в БД
@dp.message_handler(commands=['add_serial'])
async def process_add_serial_command(message: types.Message):
    user_info = db_api_users().get_user_info(message.from_user.id)

    if user_info:
        title = str(message.text[12:]).strip()

        if title != "":
            await message.answer(f"Тааак, сейчас посмотрим...")
            title_info = db_api_serial().get_user_title(user_info.id)

            title_info = convert_to_lower(title_info)

            if title.lower() not in title_info:
                serial = Serials("https://myshows.me/search/all/")
                result = serial.run(title)

                if type(result) is str:
                    await message.answer(result)
                else:
                    db_api_serial().add([user_info.id] + result)
                    await message.answer(f"Сериал {title} добавлен в ваш список!")
            else:
                await message.answer(f"Сериал {title} уже есть в вашем списке")
        else:
            await message.answer(f"Неправильно используется команда /add_serial, воспользуйтесь командой /help "
                                 f"чтобы ознакомиться с возможностями бота.")
    else:
        await message.answer("Может стоит для начала познакомиться со мной?(введи команду /start).")