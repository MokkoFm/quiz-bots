from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from get_quiz import get_quiz
from connect_to_db import connect_to_db
import telegram
import logging
import os
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

NEW_QUESTION, ANSWER = range(2)

custom_keyboard = [['New question', 'Сapitulation'],
                   ['My score']]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
quiz = get_quiz()
db = connect_to_db()


def start(bot, update):
    user = update.message.chat_id
    update.message.reply_text(
        'Hi! I am a quiz-bot! Click on New question to start a quiz!',
        reply_markup=reply_markup)
    if not db.get('score-' + str(user)):
        db.set('score-' + str(user), 0)
    return NEW_QUESTION


def new_question(bot, update):
    question = random.choice(list(quiz.keys()))
    db.set(update.message.chat_id, question)
    update.message.reply_text(
        text=question,
        reply_markup=reply_markup,
    )
    return ANSWER


def answer(bot, update):
    answer = update.message.text
    user = update.message.chat_id
    question = db.get(user)
    user_score = 'score-' + str(user)
    score = db.get(user_score)
    if answer == quiz[question].split('.')[0] or answer == quiz[question].split('(')[0]:
        update.message.reply_text(
            text='Congrats! Push New question if you want one more!',
            reply_markup=reply_markup
        )
        db.set(user_score, ++ 1)
        return NEW_QUESTION
    elif answer == 'Сapitulation':
        update.message.reply_text(
            text=quiz[question],
            reply_markup=reply_markup,
        )
        return NEW_QUESTION
    elif answer == 'My score':
        update.message.reply_text(
            text=score,
            reply_markup=reply_markup,
        )
        return ANSWER
    else:
        update.message.reply_text(
            text='Unfortunately, no... Try again!',
            reply_markup=reply_markup
        )
        return ANSWER


def help(bot, update):
    update.message.reply_text('Help!')


def cancel(update, context):
    update.message.reply_text(
        'Have a good day!', reply_markup=telegram.ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")

    updater = Updater(tg_token)
    dp = updater.dispatcher
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
