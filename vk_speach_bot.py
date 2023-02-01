import logging
import random

import environs
import vk_api as vk
from dialogflow_functions import detect_intent_texts, logging_config
from vk_api.longpoll import VkEventType, VkLongPoll


logger = logging.getLogger(__name__)


def receive_message(vk_token, session_id, project_id):
    vk_session = vk.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            answer = detect_intent_texts(
                session_id=session_id,
                text=event.text,
                language_code='ru',
                project_id=project_id,
                vk_token=vk_token)

            return answer, event.user_id


def send_message(user_id, text, vk_token):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    vk_api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":

    logging_config()

    env = environs.Env()
    env.read_env()

    project_id = env.str("PROJECT_ID")
    vk_token = env.str("VK_TOKEN")
    session_id = '1234567'

    while True:

        answer, user_id = receive_message(
            vk_token=vk_token,
            session_id=session_id,
            project_id=project_id
        )
        if not answer:
            pass
        else:
            send_message(
                user_id=user_id,
                text=answer,
                vk_token=vk_token)
