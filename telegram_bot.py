import os
import time
from os import listdir

import telegram
from dotenv import load_dotenv


def send_images(bot, image_folder, chat_id, timer_seconds):
    while True:
        for image in listdir(image_folder):
            with open(f'{image_folder}/{image}', 'rb') as file:
                bot.send_document(
                    chat_id=chat_id,
                    document=file
                )
                time.sleep(timer_seconds)


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    timer_seconds = 86400
    image_folder = 'images'
    bot = telegram.Bot(token=token)
    send_images(bot, image_folder, chat_id, timer_seconds)