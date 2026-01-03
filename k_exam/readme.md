## 3. Настройка переменных окружения 
Создаётся файл ```.env```
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
В ```settings.py``` используется ```dotenv```:
```python
from dotenv import load_dotenv
from os import getenv

load_dotenv()
```
## 4. Настройка PostgreSQL:
В ```settings.py```:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "PORT": getenv("DB_PORT"),
    }
}
```

## Добавление article в проект 
Добавляешь в ```INSTALLED_APPS``` ```article.apps.ArticleConfig```
```python
INSTALLED_APPS = [
    ...
    "article.apps.ArticleConfig",
    ...
]
```
