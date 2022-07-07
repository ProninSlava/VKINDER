import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
from config import user_token, group_token
from pprint import pprint

TOKEN_VK_USER = user_token
TOKEN_VK_GROUP = group_token

# Для работы с vk_api
session = vk_api.VkApi(token=TOKEN_VK_USER)
# longpoll = VkLongPoll(session)


# Ищет людей по критериям используем метод 'users.search'
# gender 1-ж  2-м
# age_from возраст от .. age_to возраст до
def search_users(gender, age_at, age_to, city):
    all_persons = []
    link = 'https://vk.com/id'
    vk_ = session
    response = vk_.method('users.search',
                          {'sort': 1,
                           'sex': gender,
                           'status': 1,
                           'age_from': age_at,
                           'age_to': age_to,
                           'has_photo': 1,
                           'count': 15,
                           'online': 1,
                           'hometown': city,
                           'fields': 'bdate'
                           })
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link + str(element['id']),
            element['id'],
            element['bdate']

        ]
        all_persons.append(person)
    # pprint(all_persons)
    return all_persons

# search_users(1, 20, 25, 'Москва')

# Находит фото людей
def get_photo(user_owner_id):
    vk_ = session
    try:
        response = vk_.method('photos.get',
                              {  'access_token': TOKEN_VK_USER,
                                  'v': '5.131',
                                  'owner_id': user_owner_id,
                                  'album_id': 'profile',
                                  'count': 5,
                                  'extended': 1,
                              })
    except ApiError:
        return 'в доступе к фото отказано'
    # pprint(response)
    users_photos = []
    for i in range(5):
        try:
            users_photos.append(
                [response['items'][i]['likes']['count'],
                 response['items'][i]['sizes'][-1]['url']])
        except IndexError:
            users_photos.append(['фото нет'])
    # pprint(users_photos)
    return users_photos


# get_photo(733074985)

# search_users(1, 30, 45, 'Новосибирск')


# def get_top_3_photo(self, user_id):

#         params = {'owner_id': user_id, 'album_id': 'profile', 'extended': 1}
#         response = self.user_vk.method('photos.get', params)
#         photos = response['items']
#         sorted_photo = sorted(photos, reverse=True, key=lambda photo: int(photo['likes']['count']))[:3]
#         photo_ids = [photo['id'] for photo in sorted_photo]
#         return photo_ids