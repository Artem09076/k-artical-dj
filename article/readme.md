## 5. Создание моделей 
Создаются классы сущностей
* Profile
* Article
* Category
* Tag
* Comment
* Like

Все эти классы населдуются от ```models.Model```.

Также используются ```UUIDMixin``` для добавления ```id``` во все сущности
```python
class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True # Нужен, чтобы django не считал миксин за отдельную таблицу в бд
```
## Добавление моделей в админ панель
Для этого в файле ```admin.py```
```python
from .models import Article, Category, Comment, Like, Profile, Tag

# Здесь регистрируешь свои модели для отображения в админке
admin.site.register([Article, Like, Profile, Category, Tag, Comment])

```


## 6. Django REST Framework
### 6.1 Сериализаторы
```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__" # Это значит, что выводит все поля, если нужны какие то конкретные, то тогда [<название аттрибута 1>, <названия аттрибута 2>]
```
### 6.1 ViewSet с кастомными permissions
```python
class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user.is_authenticated
        return request.user.is_superuser
```

## 7. Подсчет мерик
### 7.1 Latency (Histogram)
Создаём в файле ```metrics.py``` гистограмму 
```python
from prometheus_client import Histogram

DB_LATENCY = Histogram(
    name="db_latency_seconds",
    documentation="Latency of database operations in seconds",
    labelnames=["handler"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],
)
```
После создаём в файле ```decorators.py``` декоратор, который будет отсчитывать время выполнения запроса
```python
import time
from functools import wraps

from .metrics import DB_LATENCY
def track_db_latency(method_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_time = time.time() - start_time
                DB_LATENCY.labels(handler=method_name).observe(elapsed_time)

        return wrapper
    return decorator
```
Применение
``` python
@track_db_latency("index")
def index(request):
    return HttpResponse("Hello, this is the article index page.")
```
Чтобы посмотреть метрику заходите на ```localhost:9090```, и пишите
```shell
db_latency_seconds_bucket{handler="<название handler>",le="0.1"} # Считает сколько вызовов выполнились быстрее или ровно за 0.1 секунды
db_latency_seconds_sum{handler="<название handler>"} # Считает суммарное время запросов
db_latency_seconds_count{handler="<название handler>"} # Считает сколько вызовов было сделано
```
### 7.2 Middleware для HTTP-метрик
Счётчики:

* Общее число запросов
* 2xx
* 4xx
* 5xx

Реализовано через ```prometheus_client.Counter``` и ```Django middleware```.

Для этого в файле ```settings.py``` добавьте в переменную ```INSTALLED_APPS``` ```"django_prometheus"```

И измените переменную ```MIDDLEWARE```
```python
MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware", # Добавляете этот в самое начало
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "article.middleware.CorrelationIdMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware", # Добавляете этот в самый конец
]
```
Чтобы посмотреть метрику заходите на ```localhost:9090```, и пишите
```shell
django_http_responses_total_by_status_total{status="200"} # если надо посмотреть сколько ответов со status_code 200
django_http_responses_total_by_status_total{status="404"} # если надо посмотреть сколько ответов со status_code 404
```

## 8. Correlation-ID Middleware
### 8.1 Middleware
```python
class CorrelationIdMiddleware:
    def __call__(self, request):
        correlation_id = request.META.get("HTTP_X_CORRELATION_ID") or uuid4()
        request.correlation_id = str(correlation_id)
        _thread_local.correlation_id = request.correlation_id
        response = self.get_response(request)
        response["X-Correlation-ID"] = request.correlation_id
        return response
```
## 9 Логирование с Correlation-ID
### 9.1 Logging Filter
```python
class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        return True
```
### 9.2 Подключение 
Создаёте в ```settings.py``` переменную ```LOGGING```
```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id_filter": {
            "()": "article.logging.CorrelationIdFilter",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] [%(levelname)s] [Correlation ID: %(correlation_id)s] %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["correlation_id_filter"],
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```
### 9.3 Применение
```python
logger = logging.getLogger(__name__)

@track_db_latency("index")
def index(request):
    logger.info("AAAAAAAAAAAAAAAAa")
    return HttpResponse("Hello, this is the article index page.")
```
## 10. Интеграционный тест
```python
class HealthEndpointIntegrationTest(TestCase):
    def test_root_endpoint_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
```
**Запуск**:
```shell
python manage.py test
```
