# Командный проект по курсу «Профессиональная работа с Python»

## VKinder

### Цель проекта

Цель командного проекта - разработать программу-бота для взаимодействия с базами данных социальной сети. Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

Вам предстоит:
- разработать программу-бота на Python
- спроектировать и реализовать базу данных (БД) для программы
- настроить взаимодействие бота с ВК
- написать документацию по использованию программы

В результате выполнения этого задания вы:
- получите практический опыт работы в команде
- прокачаете навыки коммуникации и умение выполнять задачи в срок
- закрепите навыки работы с GitHub и программирования на языке Python
- разработаете с нуля полноценный программный продукт, который можно будет добавить в портфолио бэкенд-разработчика.

------

### Чеклист готовности к работе над проектом

1. Изучили «Инструкцию по выполнению командного проекта» и «Правила работы в команде» в личном кабинете.
1. Знаете, кто с вами в команде.
1. Познакомились со своей командой и определились, каким способом будете общаться (переписка в любом мессенджере, видеозвонки).
1. Договорились, кто будет размещать общий репозиторий проекта и отправлять его на проверку.
1. У вас должен быть установлен Python 3.x и любая IDE. Мы рекомендуем работать с Pycharm.
1. Настроен компьютер для работы с БД PostgreSQL.
1. Установлен git и создан аккаунт на Github.
1. Должна быть создана группа во Вконтакте, от имени которой будет общаться разрабатываемый бот. Инструкцию можно будет посмотреть [здесь](group_settings.md).

Если все этапы чеклиста пройдены, то можете стартовать работу над проектом. Успехов в работе!

------

### Инструменты/ дополнительные материалы, которые пригодятся для выполнения задания

1. [Python](https://www.python.org/) + IDE([Pycharm](https://www.jetbrains.com/ru-ru/pycharm/download))
2. [Git](https://git-scm.com/) + [Github](https://github.com/)
3. [Postgre](https://www.postgresql.org/) + [PgAdmin](https://www.pgadmin.org/)
4. [ВКонтакте](https://vk.com/)

------

### Инструкция к работе над проектом

Необходимо разработать программу-бота, которая должна выполнять следующие действия:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВК, сделать поиск других людей (других пользователей ВК) для знакомств.
2. У тех людей, которые подошли под критерии поиска, получить три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводить в чат с ботом информацию о пользователе в формате:
```
Имя Фамилия
ссылка на профиль
три фотографии в виде attachment(https://dev.vk.com/method/messages.send)
```
4. Должна быть возможность перейти к следующему человеку с помощью команды или кнопки.
5. Сохранить пользователя в список избранных.
6. Вывести список избранных людей.

*Обратите внимание: токен для ВК можно получить выполнив [инструкцию](https://docs.google.com/document/d/1_xt16CMeaEir-tWLbUFyleZl6woEdJt-7eyva1coT3w/edit?usp=sharing).*