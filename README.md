# Трекер полезных привычек

## Содержание
- [Описание](#описание)
- [Технологии](#технологии)
- [Запуск проекта](#запуск-проекта)
- [Запуск в docker-контейнере](#запуск-в-docker-контейнере)
- [Тестирование](#тестирование)
- [Документация](#просмотр-документации)
- [Административная панель](#административная-панель)

## Описание
Пример привычки описывается как конкретное действие

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку пользователю необходимо себя вознаграждать или сразу после делать приятную привычку.

Реализована работа с отложенными задачами для напоминания о том, в какое время и какие привычки необходимо выполнять.

Сервис интегрирован с мессенджером Телеграм, через который осуществляется рассылка уведомлений.

### Эндпоинты
- Регистрация
- Авторизация
- CRUD привычек
- Список публичных привычек
- Просмотр публичной привычки

### Валидаторы
- Исключен одновременный выбор связанной привычки и указания вознаграждения.
В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.

- Время выполнения должно быть не больше 120 секунд.
- В связанные привычки могут попадать только привычки с признаком приятной привычки.
- У приятной привычки не может быть вознаграждения или связанной привычки.
- Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
Нельзя не выполнять привычку более 7 дней. Например, привычка может повторяться раз в неделю, но не раз в 2 недели. За одну неделю необходимо выполнить привычку хотя бы один раз.

### Пагинация
Для вывода списка привычек реализована пагинация с выводом по 5 привычек на страницу.

### Права доступа
- Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.
- Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.

### Безопасность
Настроен CORS для подключения фронтенда.

## Технологии
- Python
- Django
- DRF
- PostgreSQL
- Simple JWT 
- drf-yasg
- Redis
- Celery
- Django-celery-beat
- Docker
- Docker Compose


## Запуск проекта
1. Клонируйте проект
```
git clone git@github.com:aleksandrasilina/habit_tracker.git
```
2. Установите зависимости
```
pip install poetry
```
```
poetry install
```
3. Создайте файл .env в соответствии с шаблоном .env.sample
4. Наполните базу данных тестовыми данными:
- привычки
```
python manage.py loaddata habits.json
```
- группы пользователей
```
python manage.py loaddata users.json
```
3. Создайте суперпользователя (почта: admin@example.ru, пароль: 123456)
```
python manage.py csu
```
4. Примените миграции
```
python manage.py migrate
```
5. Запустите проект
```
python manage.py runserver
```
6. Запустите redis
```
redis-server
```
7. Запустите celery worker:
```
celery -A config worker -l INFO -P eventlet
```
8. Запустите celery-beat:
```
celery -A config beat -l info -S django
```

## Запуск в docker-контейнере

1. Установите POSTGRES_HOST=db
2. 
```
docker-compose build
```
3.
```
docker-compose up
```

## Тестирование:
```
python manage.py test
```

## Просмотр документации
http://127.0.0.1:8000/swagger/

http://127.0.0.1:8000/redoc/

## Административная панель
http://127.0.0.1:8000/admin/
