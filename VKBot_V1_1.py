from datetime import datetime
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dataclasses import dataclass

from config import group_token, user_token

@dataclass()
class BotMsg():
    '''Класс сообщений бота для пользователя'''
    
    misunderstand: str = 'Я вас не понял %s. Но давайте покажу вам меню!'
    start: str = 'Привет %s! Начнем поиск? Или взглянем кто там у нас уже есть?'
    criterions: str = 'Выберите критерии поиска'
    again: str = 'Начнём сначала?'
    city: str = 'Введите название города:'
    greetings: tuple = ('start', 'старт', 'hello', 'hi', 'привет', 'хай', 'ку')
    leaving: tuple = ('goodbye', 'пока', 'end', 'конец')
    city: str = 'Введите название города:'
    city_error: str = 'Город не найден. Попробуйте ещё раз:'
    sex: str = 'Выберите интересующий вас пол:'
    sex_again: str = 'Нажмите кнопку выбора пола'
    boy: str = 'Выбраны мальчики'
    girl: str = 'Выбраны девочки'
    minage: str = 'Введите минимальный возраст (от 18 до 99):'
    minage_select: str = 'Будем искать кандидатов от %s лет'
    minage_error: str = 'Введите целое число от 18 до 99'
    maxage: str = 'Введите максимальный возраст (от 18 до 99):'
    maxage_select: str = 'Будем искать кандидатов до %s лет'
    maxage_error: str = 'Введите целое число от 18 до 99:'

class VKinder():
    
    def __init__(self, group_api, user_api):
        self.group_api = group_api
        self.group_get_api = group_api.get_api()
        self.user_api = user_api
        self.longpoll = VkLongPoll(self.group_api)
        #self.db_session = для активации подключения БД
        
        for event in self.longpoll.listen():
            self.handle_start_event(event)
    
    def is_message_to_bot(event):
        return event.type == VkEventType.MESSAGE_NEW and event.to_me
    
    def send_msg(self, user_id, message, attachment=None, keyboard=None):
        '''Функция отправки сообщений пользователю бота'''
        
        params = {
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': randrange(10 ** 5),
            'keyboard': keyboard 
        }     
        self.group_api.method('messages.send', params)

    def set_search_keyboard(self):
        '''Функция возвращает клавиатуру "Поиск" бота'''
        
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
    
    def set_start_keyboard(self):
        '''Функция возвращает стартовую клавиатуру бота'''
        
        start_keyboard = VkKeyboard()
        start_keyboard.add_button('Поиск!', VkKeyboardColor.PRIMARY)
        start_keyboard.add_button('Избранное', VkKeyboardColor.PRIMARY)
        start_keyboard = start_keyboard.get_keyboard()
        return start_keyboard
    
    def set_sex_keyboard(self):
        '''Функция возвращает клавиатуру для выбора пола'''
        
        sex_keyboard = VkKeyboard(one_time=True)
        sex_keyboard.add_button('Он', VkKeyboardColor.PRIMARY)
        sex_keyboard.add_button('Она', VkKeyboardColor.POSITIVE)
        sex_keyboard = sex_keyboard.get_keyboard()
        return sex_keyboard
    
    def set_results_keyboard(self):
        '''Функция возвращает клавиатуру для работы с результатами поиска'''
        
        results_keyboard = VkKeyboard(one_time=True)
        results_keyboard.add_button('Следующий', VkKeyboardColor.PRIMARY)
        results_keyboard.add_button('В избранное', VkKeyboardColor.PRIMARY)
        results_keyboard.add_button('В игнор', VkKeyboardColor.PRIMARY)
        results_keyboard.add_line()
        results_keyboard.add_button('Назад в главное меню', VkKeyboardColor.PRIMARY)
        results_keyboard = results_keyboard.get_keyboard()
        return results_keyboard
        
   
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
                self.send_msg(user_id, BotMsg.start % user_name, keyboard=self.set_start_keyboard())
                return
            
            elif message in BotMsg.leaving:
                leave_keyboard = VkKeyboard()
                leave_keyboard = leave_keyboard.get_empty_keyboard()
                self.send_msg(user_id, 'Пока!', keyboard=leave_keyboard)
                return
            
            elif message == 'поиск!':
                self.set_search_params(user_id)
                return
                   
            elif message == 'избранное':
                self.send_msg(user_id, 'Не готово!')
                return
            
            else:
                user_name = self.group_get_api.users.get(user_id=user_id)[0]['first_name']
                self.send_msg(user_id, BotMsg.misunderstand % user_name, keyboard=self.set_start_keyboard())
                return
        
    def set_search_params(self, user_id):
        '''Функция определяет стартовые параметры для поиска'''
        
        self.send_msg(user_id, 'Выберите параметры для поиска:', keyboard=self.set_search_keyboard())
        for event in self.longpoll.listen():
            if VKinder.is_message_to_bot(event):
                message = event.text.lower()
                user_id = event.user_id
                
                if message == 'назад':
                    self.send_msg(user_id, BotMsg.again, keyboard=self.set_start_keyboard())
                    return
                
                elif message == 'выбрать город':
                    self.get_city_id(user_id)
                
                elif message == 'выбрать пол':
                    self.get_sex(user_id)
                
                elif message == 'возраст от':
                    self.get_min_age(user_id)
                
                elif message == 'возраст до':
                    self.get_max_age(user_id)                    
                    
    def get_city_id(self, user_id):
        '''Функция возвращает id выбранного для поиска города'''
        
        self.send_msg(user_id, BotMsg.city, keyboard=self.set_search_keyboard())
        for event in self.longpoll.listen():
            if VKinder.is_message_to_bot(event):
                city_param = {
                    'q': event.text,
                    'country_id': 1,
                    'count': 1,
                    'v': 5.131
                }

                city_result = self.user_api.method('database.getCities', city_param).get('items')
                if not city_result:
                    self.send_msg(user_id, BotMsg.city_error)
                else:
                    self.send_msg(user_id, f'Выбран город: {event.text.capitalize()}')
                    return city_result[0].get('id')
    
    def get_sex(self, user_id):
        '''Функция возвращает желаемый пол для поиска'''
        
        self.send_msg(user_id, BotMsg.sex, keyboard=self.set_sex_keyboard())
        for event in self.longpoll.listen():
            if VKinder.is_message_to_bot(event):
                if event.text == 'Он':
                    self.send_msg(user_id, BotMsg.boy, keyboard=self.set_search_keyboard())
                    return 2
                elif event.text == 'Она':
                    self.send_msg(user_id, BotMsg.girl, keyboard=self.set_search_keyboard())
                    return 1
                else:
                    self.send_msg(user_id, BotMsg.sex_again, keyboard=self.set_sex_keyboard())
    
    def get_min_age(self, user_id):
        '''Функция возвращает минимальный возраст для поиска
           Возвращает строку'''
        
        self.send_msg(user_id, BotMsg.minage)
        for event in self.longpoll.listen():
            if VKinder.is_message_to_bot(event):
                min_age = event.text
                if min_age.isdigit() and int(min_age) >= 18 and int(min_age) <= 99:
                    self.send_msg(user_id, BotMsg.minage_select % min_age)
                    return min_age
                else:
                    self.send_msg(user_id, BotMsg.minage_error, keyboard=self.set_search_keyboard())
    
    def get_max_age(self, user_id):
        '''Функция возвращает максимальный возраст для поиска
           Возвращает строку'''
        
        self.send_msg(user_id, BotMsg.maxage)
        for event in self.longpoll.listen():
            if VKinder.is_message_to_bot(event):
                max_age = event.text
                if max_age.isdigit() and int(max_age) >= 18 and int(max_age) <= 99:
                    self.send_msg(user_id, BotMsg.maxage_select % max_age)
                    return max_age
                else:
                    self.send_msg(user_id, BotMsg.minage_error, keyboard=self.set_search_keyboard())
