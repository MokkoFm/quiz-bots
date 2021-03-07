#!/usr/bin/env python
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from main import get_quiz
import telegram
import redis
import logging
import os
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

quiz = get_quiz()
question = random.choice(list(quiz.keys()))
print(quiz[question].split('.')[0])


def start(bot, update):
    db_host = os.getenv("REDIS_DB")
    db_password = os.getenv("REDIS_DB_PASSWORD")
    db = redis.Redis(
        host=db_host, port=10513,
        db=0, password=db_password, decode_responses=True)
    db.set(update.message.chat_id, question)
    update.message.reply_text(
        'Hi! I am a quiz-bot! Click on New question to start a quiz!')


def help(bot, update):
    update.message.reply_text('Help!')


def answer(bot, update):
    custom_keyboard = [['New question', 'Сapitulation'],
                       ['My score']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    if update.message.text == 'New question':
        bot.send_message(
            chat_id=update.message.chat_id,
            text=question,
            reply_markup=reply_markup)
    elif update.message.text == quiz[question].split('.')[0] or update.message.text == quiz[question].split('(')[0]:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Perfect! Please, push New question for the next challange.',
            reply_markup=reply_markup)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Unfortunately, no... Try again!",
            reply_markup=reply_markup)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")

    updater = Updater(tg_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, answer))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
