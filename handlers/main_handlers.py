from aiogram.types import Message, CallbackQuery

from keyboards import main_menu
from functions import graph_func
from loader import dp


# Обработка команды /start
@dp.message_handler(chat_type="private", commands=["start"])
async def handler_start(message: Message):
    await message.answer("Пока я могу только нарисовать график", reply_markup=main_menu.main())


# Главное меню как и в handler_start
@dp.callback_query_handler(regexp=r"^draw_graph$")
async def handler_call_draw_graph(call: CallbackQuery):
    await call.message.edit_text("Пока я могу только нарисовать график", reply_markup=main_menu.main())


# Выбор типа графика
@dp.callback_query_handler(regexp=r"^draw_graph:\w+:\w+$")
async def handler_call_draw_graph_currency(call: CallbackQuery):
    from_currency = call.data.split(":")[1]
    to_currency = call.data.split(":")[2]
    if call.message.content_type == "text":
        await call.message.edit_text("Выбери тип графика:",
                                     reply_markup=main_menu.select_type_graph(from_currency, to_currency))
    else:
        await call.message.answer("Выбери тип графика:",
                                  reply_markup=main_menu.select_type_graph(from_currency, to_currency))
        await call.message.delete()


# Получение графика
@dp.callback_query_handler(regexp=r"^draw_graph:\w+:\w+:\w+$")
async def handler_call_draw_graph_type(call: CallbackQuery):
    from_currency = call.data.split(":")[1]
    to_currency = call.data.split(":")[2]
    _type = call.data.split(":")[3]
    file_name = graph_func.get_graph(_type, from_currency, to_currency)
    with open(file_name, 'rb') as photo:
        await call.message.answer_photo(photo, reply_markup=main_menu.back(f"draw_graph:{from_currency}:{to_currency}"))
    await call.message.delete()
