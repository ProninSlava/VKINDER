import vk_api
from vk_api.longpoll import VkLongPoll

from config import group_token, user_token
from VKBot_V1_1 import VKinder


if __name__ == '__main__':
    
    group_api = vk_api.VkApi(token=group_token)
    user_api = vk_api.VkApi(token=user_token)
    
    VKinder(group_api=group_api, user_api=user_api)

