# образ на основе которого создаём контейнер
FROM python:3.11.7-alpine

# Рабочая директория внутри проекта
WORKDIR /genealogy

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем git
RUN apk update && apk add git

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем содержимое текущей папки в контейнер
COPY . .