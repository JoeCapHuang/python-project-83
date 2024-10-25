### Hexlet tests and linter status:
[![Actions Status](https://github.com/JoeCapHuang/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/JoeCapHuang/python-project-83/actions)
[![pyCI](https://github.com/JoeCapHuang/python-project-83/actions/workflows/python-ci.yml/badge.svg)](https://github.com/JoeCapHuang/python-project-83/actions/workflows/python-ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/6105c34ce6babd7431e5/maintainability)](https://codeclimate.com/github/JoeCapHuang/python-project-83/maintainability)

Проект задеплоен на Render и доступен по следующему адресу: https://python-project-83-znep.onrender.com
# Анализатор страниц

## Описание проекта

Этот проект был разработан в рамках обучения на платформе [Hexlet](https://hexlet.io).

**Анализатор страниц** — это веб-приложение на базе Flask, предназначенное для проверки доступности веб-сайтов и проведения SEO-анализа. Приложение выполняет HTTP-запросы к заданным сайтам и анализирует наличие важных SEO-тегов, таких как `<h1>`, `<title>`, и `<meta name="description">`. Все результаты сохраняются в базе данных и отображаются в удобном интерфейсе.

## Установка проекта

Следуйте приведенным ниже шагам, чтобы установить проект на вашу машину.

### 1. Клонирование репозитория

Сначала сделайте форк репозитория на GitHub, затем клонируйте свой форк:

```sh
git clone https://github.com/your-username/python-project-83.git
cd python-project-83
```

### 2. Установка зависимостей и настройка базы данных

Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями. Убедитесь, что `Poetry` установлен. Если его нет, установите его с помощью следующей команды:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

После этого установите все зависимости проекта и создайте необходимые таблицы базы данных:

```sh
make build
```

### 3. Создание базы данных

Создайте базу данных PostgreSQL, которая будет использоваться приложением. Для этого выполните следующую команду:

```sh
createdb your_database_name
```

После создания базы данных укажите её URL в файле `.env` и добавьте имя пользователя и пароль.

Пример содержимого `.env`:

```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost/your_database_name
```

Замените `username` и `password` на ваши учетные данные для доступа к базе данных.

### 3. Настройка переменных окружения

Создайте файл `.env` в корневом каталоге проекта и добавьте необходимые переменные окружения. Пример содержимого `.env`:

```
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

### 4. Запуск проекта в режиме разработки

Для локального запуска сервера в режиме разработки используйте следующую команду:

```sh
make dev
```

Сервер будет доступен по адресу: `http://127.0.0.1:5000`

### 5. Запуск проекта в продакшн-режиме

Для запуска сервера в продакшн-режиме используйте следующую команду:

```sh
make start
```

По умолчанию сервер будет запущен на порту 8000. Вы можете изменить порт, передав переменную `PORT`:

```sh
make start PORT=8080
```

## Используемые технологии
- Python 3.11+
- Flask 3.0.3
- Python-dotenv 1.0.1
- Gunicorn 23.0.0
- Psycopg2-binary 2.9.9
- Validators 0.34.0
- Requests 2.32.3
- BeautifulSoup4 4.12.3
- PostgreSQL
- Poetry


