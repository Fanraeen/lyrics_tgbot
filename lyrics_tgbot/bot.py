from aiogram import Bot, Dispatcher, executor, types
from answers import *
from config import TOKEN


# initial
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=start_aw)


# inline search
@dp.inline_handler(lambda query: query['query'] != '')
async def search(query: types.InlineQuery):
    await bot.answer_inline_query(query['id'],
                                  build_query_aw(query['query']),
                                  cache_time=1000)


# track lyrics
@dp.message_handler(lambda message: message.text.startswith('/track'))
async def get_text(message: types.Message):
    api_id = message.text[6:]
    lyrics = lyrics_aw(api_id)
    if len(lyrics) > 4096:
        for part in range(0, len(lyrics), 4096):
            await bot.send_message(chat_id=message.chat.id,
                                   text=lyrics[part:part+4096])
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=lyrics)


# long-polling
executor.start_polling(dp, skip_updates=True)
