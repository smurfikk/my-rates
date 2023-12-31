# - *- coding: utf- 8 - *-
from aiogram import executor

import middlewares
from handlers import dp
from functions import repeat_func
import migrate
from loader import bot, scheduler
import config


async def scheduler_start():
    # Запускаем таймер на каждые 5 минут, вызывая функцию получения курсов валют
    scheduler.add_job(repeat_func.get_rates, "cron", minute="*/5")


async def on_startup(dp):
    middlewares.setup(dp)  # Ставим антиспам
    await scheduler_start()
    info_bot = await bot.get_me()
    config.bot_username = info_bot.username
    print(f"~~~~~ Bot @{info_bot.username} was started ~~~~~")


if __name__ == "__main__":
    migrate.run()  # Проверяем таблицы в базе данных
    scheduler.start()  # Запускаем scheduler (все таймеры)
    executor.start_polling(dp, on_startup=on_startup)  # Запускаем бота
