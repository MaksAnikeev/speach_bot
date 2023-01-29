import random
import environs
import vk_api as vk
import google.cloud.dialogflow_v2 as dialogflow

from vk_api.longpoll import VkLongPoll, VkEventType


def receive_message(vk_token, session_id, project_id):
    vk_session = vk.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            answer = detect_intent_texts(
                session_id=session_id,
                text=event.text,
                language_code='ru',
                project_id=project_id)

            user_id = event.user_id
            return answer, user_id


def detect_intent_texts(session_id, text, language_code, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        answer = None
    else:
        answer = response.query_result.fulfillment_text

    return answer




def send_message(user_id, text, vk_token):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    vk_api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
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
