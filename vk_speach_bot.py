import logging
import random

import environs
import vk_api as vk
from dialogflow import detect_intent_texts
from vk_api.longpoll import VkEventType, VkLongPoll


logger = logging.getLogger(__name__)


def receive_message(vk_token, project_id):
    vk_session = vk.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer, fallback = detect_intent_texts(
                session_id=f'vk-{event.user_id}',
                text=event.text,
                language_code='ru',
                project_id=project_id
            )
            if not fallback:
                send_message(
                    user_id=event.user_id,
                    text=answer,
                    vk_token=vk_token)


def send_message(user_id, text, vk_token):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    vk_api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = environs.Env()
    env.read_env()

    project_id = env.str("PROJECT_ID")
    vk_token = env.str("VK_TOKEN")

    try:
        receive_message(
                vk_token=vk_token,
                project_id=project_id
        )

    except Exception as err:
        print(err)
