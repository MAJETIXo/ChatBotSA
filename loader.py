from aiogram import Bot, Dispatcher
import config


# Инициализируем бота и диспетчер
bot = Bot(token=config.token)
dp = Dispatcher(bot)
