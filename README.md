# Видеохостинг на Django REST framework
Реализация API для видеохостинга. Также реализован простой видеоплеер.
___
## Технологии:
+ Django REST framework
+ Celery
+ Redis
+ PostgreSQL
+ Docker
___
## Функционал
+ Добаление, просмотр, поиск, редактирование видео
+ Оценивание, комментирование видео
+ Регистрация, авторизация JWT
+ Админ-панель
+ Видеоплеер
+ Отправка email 
___
## Установка
Для запуска приложения требуется Python и установленный пакетный менеджер pip. Следуйте инструкциям ниже, чтобы установить зависимости и запустить приложение:

**1. Клонируйте репозиторий на свой компьютер:**
```
git clone https://github.com/a23d45/drf-videohosting.git
```
**2. Перейдите в директорию проекта**

*Создайте виртуальное окружение:*
```
python -m venv venv
```
*Активируйте виртуальное окружение:*

**Windows:**
```
venv\Scripts\activate
```
**macOS и Linux:**
```
source env/bin/activate
```
**3. Установите зависимости:**
```
pip install -r requirements.txt
```
**4. Укажите требуемые настройки в файле settings.py**

**5. Запустите redis**
```
redis-server
```
**6. Запустите celery**

***Windows:***
```
celery -A config.celery worker -l info -P eventlet
```
***macOS и Linux:***
```
celery -A config.celery worker -l info
```
**7. Выполните миграции**
```
python manage.py makemigrations

python manage.py migrate
```
**8. Создайте суперпользователя**
```
python manage.py createsuperuser
```
**9. Запустите локальный сервер**
```
python manage.py runserver
```
___
## Docker
**Перейдите в директорию проекта и выполните команду**
```
docker-compose up --build
```
___
## Начало работы

Адреса для просмотра доступных эндпоинтов:

+ **Redoc**
http://127.0.0.1:8000/api/schema/redoc/

+ **Swagger UI**
http://127.0.0.1:8000/api/schema/swagger-ui/

Админ-панель:
http://127.0.0.1:8000/admin/