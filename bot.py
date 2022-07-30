import os
import json
import logging
from aiogram import Bot, Dispatcher, executor, types

from parser import get_news

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ['AB_TOKEN_API']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    starts_button = ['/all_news', '/last_news', '/3', '/help']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    [keyboard.add(button) for button in starts_button]
    text = "Hi! I'm astronews_bot and I can send you news on planets, cosmology, NASA, space missions, and more. Just choose what you need from menu. /all_news - send you last 10 news, /last_news send last one or get last /3 news."
    await message.answer(text=text, reply_markup=keyboard)


@dp.message_handler(commands=['all_news', 'last_news', '3'])
async def send_news(message: types.Message):
    """
    The bot sends the user the number of news that he has chosen
    """
    # The parser function creates a json(news.json) with the latest 10 astronomy news
    get_news()  

    with open('news.json', encoding='UTF-8') as file:
        news_dict = json.load(file)
        
    if message.text == '/all_news':
        for k in news_dict:
            title = news_dict[k]['Title']
            url = news_dict[k]['Link']
            text = f'{title}| {url}'
            await message.answer(text=text)
    elif message.text == '/last_news':
        title = news_dict['1']['Title']
        url = news_dict['1']['Link']
        text =  f'{title}| {url}'
        await message.answer(text=text)
    else:
        amount = int(message.text[1])
        for k in news_dict:
            title = news_dict[k]['Title']
            url = news_dict[k]['Link']
            text = f'{title}| {url}'
            await message.answer(text=text)
            amount -= 1
            if amount == 0:
                break


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)