import os
import random
from dotenv import load_dotenv
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from get_quiz import get_quiz
from connect_to_db import connect_to_db


def answer(event, vk_api, keyboard):
    vk_api.messages.send(
        user_id=event.user_id,
        message='Пример клавиатуры',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def create_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.PRIMARY)

    return keyboard


def get_new_question(event, vk_api, quiz, keyboard, db):
    question = random.choice(list(quiz.keys()))
    db.set(f'vk-{event.user_id}', question)
    vk_api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )
    return question


def capitulate(event, vk_api, keyboard, quiz, question):
    vk_api.messages.send(
        user_id=event.user_id,
        message=quiz[question],
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def get_score(event, vk_api, keyboard, db):
    if not db.get(f'vk_score_{event.user_id}'):
        db.set('vk_score_{}'.format(event.user_id), 0)
    vk_api.messages.send(
        user_id=event.user_id,
        message=db.get(f'vk_score_{event.user_id}'),
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def congratulate(event, vk_api, keyboard, db):
    current_score = db.get(f'vk_score_{event.user_id}')
    updated_score = int(current_score) + 1
    db.set(f'vk_score_{event.user_id}', updated_score)
    vk_api.messages.send(
        user_id=event.user_id,
        message="Верный ответ!",
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def main():
    load_dotenv()
    quiz = get_quiz()
    db = connect_to_db()
    vk_token = os.getenv("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = create_keyboard()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Новый вопрос":
                question = get_new_question(event, vk_api, quiz, keyboard, db)
            elif event.text == "Сдаться":
                capitulate(event, vk_api, keyboard, quiz, question)
            elif event.text == "Мой счёт":
                get_score(event, vk_api, keyboard, db)
            elif event.text == quiz[db.get(f'vk-{event.user_id}')].split('.')[0] or event.text == quiz[db.get(f'vk-{event.user_id}')].split('(')[0]:
                congratulate(event, vk_api, keyboard, db)
            else:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message="К сожалению, нет... Попробуйте ещё!",
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                )


if __name__ == "__main__":
    main()
