from datetime import datetime
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dataclasses import dataclass

from config import group_token, user_token

@dataclass(frozen=True)
class BotMsg():
    '''Сообщения бота для пользователя'''
    misunderstand: str = 'Я вас не понял %s. Но давайте покажу вам меню!'
    start: str = 'Привет %s! Начнем поиск? Или взглянем кто там у нас уже есть?'
    criterions: str = 'Выберите критерии поиска'
    again: str = 'Начнём сначала?'
    city: str = 'Введите название города:'
    greetings: tuple = ('start', 'старт', 'hello', 'hi', 'привет', 'хай', 'ку')
    leaving: tuple = ('goodbye', 'пока', 'end', 'конец')

class VKinder():
    
    def __init__(self, group_api, user_api):
        self.group_api = group_api
        self.group_get_api = group_api.get_api()
        self.user_api = user_api
        self.longpoll = VkLongPoll(self.group_api)
        #self.db_session = для активации подключения БД
        
        for event in self.longpoll.listen():
            self.handle_start_event(event)
    
    @staticmethod
    def is_message_to_bot(event):
        return event.type == VkEventType.MESSAGE_NEW and event.to_me
    
    def send_msg(self, user_id, message, attachment=None, keyboard=None):
        params = {
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': randrange(10 ** 5),
            'keyboard': keyboard 
        }     
        self.group_api.method('messages.send', params)

    def set_search_keyboard(self):
        search_keyboard = VkKeyboard()
        search_keyboard.add_button('Выбрать город', VkKeyboardColor.PRIMARY)
        search_keyboard.add_button('Выбрать пол', VkKeyboardColor.PRIMARY)
        search_keyboard.add_button('Искать!', VkKeyboardColor.PRIMARY)
        search_keyboard.add_line()
        search_keyboard.add_button('Возраст от', VkKeyboardColor.PRIMARY)
        search_keyboard.add_button('Возраст до', VkKeyboardColor.PRIMARY)
        search_keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        search_keyboard = search_keyboard.get_keyboard()
        return search_keyboard
   
    def handle_start_event(self, event):
        '''Функция отрабатывает стартовые сообщения от пользователя бота
           Если пользователь здоровается или прощается показывает или скрывает меню.
           Если сообщение от пользователя не опознано - тоже показывает меню'''
        if VKinder.is_message_to_bot(event):
            message = event.text.lower()
            user_id = event.user_id
            
            # где то тут когда пользователь что-либо написал - нужно 
            # сначала проверить если ли он в бд - если есть написать с возвращением
            # если нет - добавить его в бд

            if message in BotMsg.greetings:
                user_name = self.group_get_api.users.get(user_id=user_id)[0]['first_name']
                start_keyboard = VkKeyboard()
                start_keyboard.add_button('Поиск!', VkKeyboardColor.PRIMARY)
                start_keyboard.add_button('Избранное', VkKeyboardColor.PRIMARY)
                start_keyboard = start_keyboard.get_keyboard()
                self.send_msg(user_id, BotMsg.start % user_name, keyboard=start_keyboard)
                return
            
            elif message in BotMsg.leaving:
                leave_keyboard = VkKeyboard()
                leave_keyboard = leave_keyboard.get_empty_keyboard()
                self.send_msg(user_id, 'Пока!', keyboard=leave_keyboard)
                return
            
            elif message == 'поиск!':
                self.set_search_params(event)
                
            
            elif message == 'избранное':
                self.send_msg(user_id, 'Не готово!')
            
            else:
                user_name = self.group_get_api.users.get(user_id=user_id)[0]['first_name']
                start_keyboard = VkKeyboard()
                start_keyboard.add_button('Поиск!', VkKeyboardColor.PRIMARY)
                start_keyboard.add_button('Избранное', VkKeyboardColor.PRIMARY)
                start_keyboard = start_keyboard.get_keyboard()
                self.send_msg(user_id, BotMsg.misunderstand % user_name, keyboard=start_keyboard)
                return
        
    def set_search_params(self, event):
         if VKinder.is_message_to_bot(event):
            message = event.text.lower()
            user_id = event.user_id
            
            self.send_msg(user_id, 'Скоро начнем!', keyboard=self.set_search_keyboard())
            
           

    