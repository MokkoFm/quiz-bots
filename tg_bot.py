from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from main import get_quiz
import telegram
import redis
import logging
import os
import random
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

NEW_QUESTION, ANSWER = range(2)


custom_keyboard = [['New question', 'Сapitulation'],
                   ['My score']]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
quiz = get_quiz()
db_host = os.getenv("REDIS_DB")
db_password = os.getenv("REDIS_DB_PASSWORD")
db = redis.Redis(
    host=db_host, port=10513,
    db=0, password=db_password, decode_responses=True)


def start(bot, update):
    update.message.reply_text(
        'Hi! I am a quiz-bot! Click on New question to start a quiz!',
        reply_markup=reply_markup)
    return NEW_QUESTION


def new_question(bot, update):
    question = random.choice(list(quiz.keys()))
    db.set(update.message.chat_id, question)
    update.message.reply_text(
        text=question,
        reply_markup=reply_markup,
    )

    return ANSWER


def help(bot, update):
    update.message.reply_text('Help!')


def cancel(update, context):
    update.message.reply_text(
        'Have a good day!', reply_markup=telegram.ReplyKeyboardRemove())

    return ConversationHandler.END


def answer(bot, update):
    message = update.message.text
    question = db.get(update.message.chat_id)
    if message == quiz[question].split('.')[0] or message == quiz[question].split('(')[0]:
        update.message.reply_text(
            text='Congrats! Push New question if you want one more!',
            reply_markup=reply_markup
        )
        return NEW_QUESTION
    else: 
        update.message.reply_text(
            text='Unfortunately, no... Try again!',
            reply_markup=reply_markup
        )
        return ANSWER


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    tg_token = os.getenv("TG_BOT_TOKEN")

    updater = Updater(tg_token)
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(MessageHandler(Filters.text, answer))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NEW_QUESTION: [MessageHandler(Filters.regex('^New question$'), new_question)],

            ANSWER: [MessageHandler(Filters.text, answer)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
