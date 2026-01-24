# Создание и запуск проекта 
## 1. Инициализация проекта 
```commandline
django-admin startproject k_exam
cd k_exam
python manage.py startapp article
```
## 2. Установка poetry
### 2.1 Инициализация poetry
```bash 
poetry init
``` 
### 2.2 Установка основных зависимостей 
Список зависимостей 
```
django
djangorestframework
psycopg2-binary
python-dotenv
django-prometheus
prometheus-client
```
Установка зависимостей
```bash
poetry add <package_name>
``` 
## Миграции 
Запускаете ваш контейнер Postgres, пишете ваши модели, после чего выполняете команду 
```shell
python manage.py makemigrations
```
Далее создаётся файл в папке ```migrations```. После чего выполняете команду 
```shell
python3 manage.py migrate
```

## Запуск проекта 
```shell
docker compose up --build
```
Проект находится на адресе
```http://localhost:8080``` 

## Ruff — линтер
Настройки находятся ```pyproject.toml```
```
[tool.ruff]
target-version = "py312"
line-length = 88
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "migrations",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "B",   # bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

ignore = [
    "E501",  # line too long (если не используешь ruff format)
]

fixable = ["ALL"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
```
Запуск 
```shell
ruff check .
```
## Настройка 
Чтобы установить Django
```shell
pip install Django
```
Чтобы установить rest_framework
```shell
pip install djangorestframework
```

Если будет ситуация, что docker запускается только с sudo(т.е из под root)

```
sudo usermod -aG docker $USER
```
После чего пересоздайте терминал