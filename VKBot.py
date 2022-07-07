from dataclasses import dataclass
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dataclasses import dataclass

from config import group_token, user_token


greetings = ['start', 'hello', 'hi', 'привет', 'хай', 'ку']

@dataclass(frozen=True)
class BotMsg():
    '''Сообщения бота для пользователя'''
    misunderstand: str = 'Я вас не понимаю.'
    start: str = 'Привет %s! Начнем поиск? Или посмотрим кто у нас уже есть?'
    criterions: str = 'Выберите критерии поиска'
    again: str = 'Начнём сначала?'
    city: str = 'Введите название города:'
    

vk_session = vk_api.VkApi(token=group_token)
api_vk = vk_session.get_api()
user_vk = vk_api.VkApi(token = user_token)
longpoll = VkLongPoll(vk_session)

def get_city_id(): 
        '''Поиск id города. Возвращает первые 3 результата.'''
        send_message(user_id, BotMsg.city)
        city_name = event.text.capitalize()
        params = {'q': city_name, 'country_id': 1}
        response = user_vk.method('database.getCities', params)
        # send_message(user_id, f'Выбран: {event.text.capitalize()}')
        return response['items'][:3]

def send_message(user_id, message, keyboard=None):
    params = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 5)
    }
    
    if keyboard != None:
        params['keyboard'] = keyboard.get_keyboard()
        
    vk_session.method('messages.send', params)

def set_keyboard_start(one_time=True):
    keyboard = VkKeyboard()
    keyboard.add_button('Поиск!', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Избранное', VkKeyboardColor.PRIMARY)
    return keyboard

def set_keyboard_search():
    keyboard = VkKeyboard()
    keyboard.add_button('Выбрать город', VkKeyboardColor.PRIMARY)
    keyboard.add_button('В моём городе', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Выбрать пол', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Возраст от', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Возраст до', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
    return keyboard


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id
        
        if text in greetings:
            user_name = api_vk.users.get(user_id=user_id)[0]['first_name']
            send_message(user_id, BotMsg.start % user_name, set_keyboard_start())
        elif text == 'поиск!':
            send_message(user_id, BotMsg.criterions, set_keyboard_search())
        elif text == 'назад':
            send_message(user_id, BotMsg.again, set_keyboard_start())
        elif text == 'выбрать город':
            city = get_city_id()
            
            
        
        else:
            send_message(user_id, BotMsg.misunderstand)
        

