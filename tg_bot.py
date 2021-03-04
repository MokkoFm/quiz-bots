#!/usr/bin/env python
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi! I am a quiz-bot!')


def help(bot, update):
    update.message.reply_text('Help!')


def answer(bot, update):
    custom_keyboard = [['New question', 'Сapitulation'],
                       ['My score']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    if update.message.text == 'New question':
        bot.send_message(
            chat_id=update.message.chat_id,
            text="А вот и вопросик: столица Аргентины?",
            reply_markup=reply_markup)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="You are the best!",
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
