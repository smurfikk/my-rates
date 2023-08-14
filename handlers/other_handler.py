from aiogram.types import Message

from loader import dp


@dp.message_handler(chat_type="private")
async def send_welcome(message: Message):
    await message.answer(";(")
