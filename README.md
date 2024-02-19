# genealogy-web-backend

Backend-часть проекта "Генеалогия"

## Начало работы

### 1. Склонировать репозиторий:

```sh
git clone https://github.com/lad-academy/genealogy-web-backend.git
```

### 2. Перейти в папку проекта:

```sh
cd genealogy-web-backend
```

### 3. Установить переменные окружения или создать .env файл:

- Установить переменные окружения в соответствии с шаблоном env.dist или создать .env файл в корне проекта на его 
основе
- SECRET_KEY Django можно получить с помощью функции get_random_secret_key() из модуля django.core.management.utils 
после установки виртуального окружения

### Для сборки проекта и запуска в docker-compose выполнить:

```sh
docker compose up --build
```
или следовать дальнейшим инструкциям по локальной установке.

## Локальная установка и запуск:

### 1. Установить виртуальное окружение:

```sh
python -m venv .venv
```

`.venv` - путь к виртуальному окружению

### 2. Активировать виртуальное окружение:

- Для Windows

```sh
.venv\Scripts\activate
```

- Для Linux и MacOS

```sh
source venv/bin/activate
```

### 3. Обновить pip и установить зависимости python:

```sh
pip install --upgrade pip
```
```sh
pip install -r requirements.txt
```

### 4. Подготовить БД PostgreSQL

#### - Установить PostgreSQL

#### - Открыть SQL Shell и ввести запрашиваемый пароль суперпользователя

#### - Создать нового пользователя 
Переменные, указанные внутри <>, должны быть определены в файле .env

```sh
CREATE USER <POSTGRES_USER> WITH PASSWORD '<POSTGRES_PASSWORD>';
```

#### - Создать БД и задать владельца

```sh
CREATE DATABASE <POSTGRES_DB> OWNER=<POSTGRES_USER>;
```

#### - Проверить наличие созданной БД, открыв список существующих:

```sh
\l
```

Для удаления БД (при наличии ошибок) выполнить:

```sh
DROP DATABASE <POSTGRES_DB>;
```

### 5. Создать и выполнить миграции БД:

```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

### 6. Загрузить фикстуры:

```sh
python manage.py loaddata db.json
```
В дальнейшем для сохранения фикстур можно воспользоваться командой:

```sh
python -Xutf8 manage.py dumpdata --indent=2 --exclude auth --exclude contenttypes -o fixtures/db.json
```

### 7. Запустить тестовый web-сервер:

```sh
python manage.py runserver
```
По умолчанию сервер будет запущен по адресу [127.0.0.1:8000](http://127.0.0.1:8000)
