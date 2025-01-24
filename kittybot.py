import logging
import os
import requests

from dotenv import load_dotenv
from telebot import TeleBot, types


load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = 'https://api.thecatapi.com/v1/images/search'

bot = TeleBot(token=TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def get_new_image():
    """Fetch a random cat image URL from the Cat API.

    If the primary API fails, it falls back to the Dog API.

    Returns:
        str: URL of a random cat or dog image.
    """
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    """Send a random cat image in response to the /newcat command.

    Args:
        message (telebot.types.Message): The message object containing chat info.
    """
    chat_id = message.chat.id
    bot.send_photo(chat_id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    """Handle the /start command to welcome the user and send a random cat image.

    Args:
        message (telebot.types.Message): The message object containing chat info.
    """
    chat_id = message.chat.id
    name = message.from_user.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/newcat')
    keyboard.add(button)

    bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашел',
        reply_markup=keyboard,
    )

    bot.send_photo(chat_id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    """Respond to any text message with a simple greeting.

    Args:
        message (telebot.types.Message): The message object containing chat info.
    """
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


def main():
    """Start the bot and enable polling."""
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
