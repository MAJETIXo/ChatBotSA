from aiogram import types
from loader import dp
from db.db_api_users import db_api_users
from datetime import datetime


# Команда /start - добавляем нового пользователя в БД
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_info = db_api_users().get_user_info(message.from_user.id)

    if user_info is not None:
        date = datetime.strptime(str(user_info.join_date), "%Y-%m-%d %H:%M:%S")
        await message.answer("Мне кажется или ты уже регистрировался " + date.strftime("%d %b %Y") + " в "
                             + date.strftime("%H:%M:%S") + " ?")
    else:
        data = (message.from_user.id, message.from_user.username)
        db_api_users().add_user(data)
        await message.answer("Привет, теперь я буду уведомлять тебя о выходе новых серий, воспользуйся командой"
                             " /help чтобы посмотреть, что я умею")


# Команда /help - Выводим список всех возможных команд
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("/add_serial [Название сериала] - добавляет сериал в список отслеживаемого;\n"
                         "/add_anime [Название аниме] - добавляет аниме в список отслеживаемого.\n"
                         "/delete [Название сериала/аниме] - удаляет сериал из списка отслеживаемого (чувствителен к регистру).\n"
                         "/info - выводит информацию о отслеживаемых сериалах\n"
                         "/leave - вводи эту команду, если я тебе надоел.\n")