import os
from dotenv import load_dotenv
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType


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


def main():
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = create_keyboard()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api, keyboard)


if __name__ == "__main__":
    main()
