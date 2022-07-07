import vk_api
from pprint import pprint
from VKtoken import access_token
from datetime import datetime


session = vk_api.VkApi(token=access_token)
vk = session.get_api()


def processing_photos(user_id):
    photos = vk.photos.getAll(access_token=access_token,
                              owner_id=user_id,
                              extended=1,
                              count=200,
                              photo_sizes=0)
    best_three_photos = sorted(photos['items'], key=lambda x: x['likes']['count'])[-3:]
    return [photo['sizes'][-1]['url'] for photo in best_three_photos]

def processing_applicant(user_id):
    user = vk.users.get(user_id=[user_id], fields='bdate,city,country,sex')[0]
    photos = processing_photos(user['id'])
    user_url = 'https://vk.com/id' + str(user_id)
    return f"{user['first_name']} {user['last_name']} {user_url} {photos}"


def search_applicants(age, user_sex, city_id):
    offset = 0
    while offset < 15:
        offset += 1
        applicants = vk.users.search(city=city_id,
                                     sex=user_sex % 2 + 1,
                                     age_from=age - 2,
                                     age_to=age + 2,
                                     has_photo=1,
                                     offset=offset,
                                     count=1)
        if applicants['items'][0]['can_access_closed']:
            yield processing_applicant(applicants['items'][0]['id'])


if __name__ == '__main__':
    user = vk.users.get(user_id=['loggvi'], fields='bdate,city,country,sex')[0]
    user_city = user['city']['id']
    user_sex = user['sex']
    user_age_days = datetime.date(datetime.now()) - datetime.date(datetime.strptime(user['bdate'], '%d.%m.%Y'))
    user_age = user_age_days.days // 365
    for i in search_applicants(user_age, user_sex, user_city):
        pprint(i)