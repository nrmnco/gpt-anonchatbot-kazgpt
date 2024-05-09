from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config_reader import config

bot = Bot(config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher()