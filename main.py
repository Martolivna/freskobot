import asyncio
import random
from contextlib import suppress

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor, exceptions
from make_image import make_image

TOKEN = ""
TIME = 60

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


class Check(StatesGroup):
    check = State()


@dp.message_handler(content_types=["new_chat_members"], state='*')
async def new_member_handler(message: types.Message, state: FSMContext):
    question, answer = make_question()
    bot_message = await message.reply_photo(make_image(question, TIME), reply_markup=types.ForceReply(selective=True))
    await state.update_data(answer=answer, bot_message=bot_message)
    await Check.check.set()
    await asyncio.sleep(TIME)

    data = await state.get_data()
    if data and data['bot_message'] == bot_message:             # Если пользователь не ответил то data еще не очищен
        await kick_user(message.chat, message.from_user)        # и bot_message-ы совпадают.   в таком случае кикаем
        await state.finish()
    with suppress(exceptions.MessageToDeleteNotFound):
        await bot_message.delete()


@dp.message_handler(state=Check.check)
async def answer_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if str(data['answer']) not in message.text:
        await kick_user(message.chat, message.from_user)
    else:
        await data['bot_message'].delete()
        await message.delete()
    await state.finish()                                        # Пользователь ответил, стейт = None


def make_question():
    a, b, c = [random.randint(1, 9) for _ in range(3)]
    question = f'{a} + {b} * {c}'
    answer = a+b*c
    return question, answer


async def kick_user(chat: types.Chat, user: types.User):
    try:
        await chat.kick(user.id)
        await chat.unban(user.id, only_if_banned=True)
    except exceptions.ChatAdminRequired:
        await bot.send_message(chat.id, f'Я бы c радостью кикнул {user.mention}, но у меня нету админки :(')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
