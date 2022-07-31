import os
import json
import logging
from aiogram import Bot, Dispatcher, executor, types

from parser import get_news

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ['AB_TOKEN_API']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def set_default_commands(dp):
    """
    Creates a menu for sending commands to the bot
    """
    await dp.bot.set_my_commands(
        [
            types.BotCommand('help', 'Help'), 
            types.BotCommand("all_news", "Get last 10 astronomy news"), 
            types.BotCommand("3", "Get last 3 astronomy news"),
            types.BotCommand("last_news", "Get last one"),
        ]
    )


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or '/help' command
    """
    await set_default_commands(dp)
    text = "Hi! I'm astronews_bot and I can send you news on planets, cosmology, NASA, space missions, and more. Just choose what you need from menu(blue button in the lower left corner)."
    await message.answer(text=text)
    await set_default_commands(dp)


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