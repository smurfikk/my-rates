# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

import config

logging.basicConfig(filename="error.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = Bot(token=config.bot_token, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
