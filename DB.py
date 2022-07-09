import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from vk_info import user_token, group_token

# Класс Base
Base = declarative_base()

DSN = 'postgresql://postgres:slava@localhost:7548/db_vk_person'

# Функциональное использование ORM
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)

# Работа с VK
vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)

# Работа с БД
session = Session()
connection = engine.connect()

# Таблицы
# CREATE TABLE IF NOT EXISTS users(
# id SERIAL PRIMARY KEY,
# vk_id INTEGER
# );
#
# CREATE TABLE IF NOT EXISTS second_half(
# id SERIAL PRIMARY KEY,
# vk_id INTEGER,
# name VARCHAR(40) NOT null,
# surname VARCHAR(40) NOT null,
# year INTEGER,
# gender VARCHAR(40) NOT null,
# city VARCHAR(40) NOT null,
# link VARCHAR(40) NOT null,
# id_user INTEGER REFERENCES users(id)
# );
#
# CREATE TABLE IF NOT EXISTS black_list(
# id SERIAL PRIMARY KEY,
# vk_id INTEGER,
# name VARCHAR(40) NOT null,
# surname VARCHAR(40) NOT null,
# year INTEGER,
# gender VARCHAR(40) NOT null,
# city VARCHAR(40) NOT null,
# link VARCHAR(40) NOT null,
# id_user INTEGER REFERENCES users(id)
# );
#
# CREATE TABLE IF NOT EXISTS photo(
# id SERIAL PRIMARY KEY,
# link_photo VARCHAR(40) NOT NULL,
# count_like INTEGER,
# id_second_half INTEGER REFERENCES second_half(id)
# );

# User бота VK
class User(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)

# Информация о второй половинке добавленная в избранное
class Second_half(Base):
    __tablename__ = 'second_half'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    gender = sq.Column(sq.Integer, unique=True)
    year = sq.Column(sq.Integer, unique=True)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id', ondelete='CASCADE'))

# Фото
class Photos(Base):
    __tablename__ = 'photo'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    count_like = sq.Column(sq.Integer)
    id_second_half = sq.Column(sq.Integer, sq.ForeignKey('second_half.id', ondelete='CASCADE'))

# Черный список
class Blakc_list(Base):
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    gender = sq.Column(sq.Integer, unique=True)
    year = sq.Column(sq.Integer, unique=True)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id', ondelete='CASCADE'))

# Функции______________________________________

#1 Регистрация пользователя
def register_user(vk_id):
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False


#2 Проверка регистрации пользователя бота в БД
def check_db_reg(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id

#3 Проверка Userа в БД
def check_db_user(ids):
    second_half_user = session.query(Second_half).filter_by(vk_id=ids).first()
    blocked_user = session.query(Blakc_list).filter_by(vk_id=ids).first()
    return second_half_user, blocked_user

#4 Проверка Userа в избранном
def check_db_elit(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()

    alls_users = session.query(Second_half).filter_by(id_user=current_users_id.id).all()
    return alls_users

#5 Проверка Userа в черном списке
def check_db_black(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()

    all_users = session.query(Blakc_list).filter_by(id_user=current_users_id.id).all()
    return all_users

#6 Удаляет Userа из избранного
def delet_db_elit(ids):
    current_user = session.query(Second_half).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

#7 Удаляет Userа из черного списка
def delet_db_black(ids):
    current_user = session.query(Blakc_list).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

#8 Пишем сообщение пользователю
def write_msg(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})

#9 Сохраняем нужного пользователя в БД
def add_user(event_id, vk_id, name, surname,year, gender, city, link, id_user):
    try:
        new_user = Second_half(
            vk_id=vk_id,
            name=name,
            surname=surname,
            year=year,
            gender=gender,
            city=city,
            link=link,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Пользователь добавлен в избранное.')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в избранном.')
        return False

#10 Сохранение фото в БД (добавленного пользователя)
def add_user_photos(event_id, link_photo, count_like, id_second_half):
    try:
        new_user = Photos(
            link_photo=link_photo,
            count_like=count_like,
            id_second_half=id_second_half
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Фото пользователя сохранено в избранном')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Невозможно добавить фото')
        return False

#11 Добавление пользователя в черный список
def add_to_black_list(event_id, vk_id, name, surname,year, gender, city, link, id_user):
    try:
        new_user = Blakc_list(
            vk_id=vk_id,
            name=name,
            surname=surname,
            year=year,
            gender=gender,
            city=city,
            link=link,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Пользователь заблокирован.')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в черном списке.')
        return False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
