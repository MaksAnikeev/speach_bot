# import vk_api
# import environs
#
# from vk_api.longpoll import VkLongPoll, VkEventType
# from pprint import pprint
#
#
# env = environs.Env()
# env.read_env()
#
# vk_token = env.str("VK_TOKEN")
# vk_session = vk_api.VkApi(token=vk_token)
#
# longpoll = VkLongPoll(vk_session)
#
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         print('Новое сообщение:')
#         if event.to_me:
#             print('Для меня от: ', event.user_id)
#         else:
#             print('От меня для: ', event.user_id)
#         print('Текст:', event.text)


import random
import environs
import vk_api as vk

from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = environs.Env()
    env.read_env()

    vk_token = env.str("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)