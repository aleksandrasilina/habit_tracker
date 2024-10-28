coursework_7_drf
Трекер полезных привычек

Наполнение базы данных habits привычками: python manage.py loaddata habits.json
Наполнение базы данных users пользователями: python manage.py loaddata users.json

Запуск проекта:
создайте файл .env в соответствии с шаблоном .env.sample
python manage.py migrate
python manage.py runserver
Запуск redis:
redis-server
Запуск celery worker:
celery -A config worker -l INFO -P eventlet
Запуск celery-beat:
celery -A config beat -l info -S django

Создание контейнеров docker-compose:
docker-compose build
docker-compose up

Тестирование:
python manage.py test
