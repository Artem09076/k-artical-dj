from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

# Пишешь сюда свои модели


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True  # Эта модель не будет создавать отдельную таблицу в базе данных


class Profile(UUIDMixin):
    # models.AutoField(primary_key=True, editable=False, auto_created=True) если нужно поле с автоинкрементом
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(
        blank=True
    )  # Текстовойо поле для биографии пользователя(blank=True - значит поле не обязательно для заполнения)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания профиля(auto_now_add=True - устанавливается при создании объекта на текущее время)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = '"public"."profile"'  # Указываем имя таблицы в базе данных


class Category(UUIDMixin):
    name = models.CharField(
        max_length=100, unique=True
    )  # Название категории c ограничением в 100 символов и уникальностью
    description = models.TextField(blank=True)  # Описание категории

    def __str__(self):
        return self.name

    class Meta:
        db_table = '"public"."category"'  # Указываем имя таблицы в базе данных


class Tag(UUIDMixin):
    name = models.CharField(
        max_length=50, unique=True
    )  # Название тега с ограничением в 50 символов и уникальностью

    def __str__(self):
        return self.name


class Article(UUIDMixin):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    categoty = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="articles"
    )
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)
    title = models.CharField(
        max_length=200
    )  # Заголовок статьи с ограничением в 200 символов
    content = models.TextField()  # Основной текст статьи
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )  # Статус статьи (черновик или опубликована)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = '"public"."article"'  # Указываем имя таблицы в базе данных
        ordering = [
            "-created_at"
        ]  # Сортировка по дате публикации и созданию в обратном порядке(из за минуса перед created_at)

    def __str__(self):
        return self.title


class Comment(UUIDMixin):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self",  # Если нужно ссылаться на ту же модель, используем 'self'
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    content = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"

    class Meta:
        db_table = '"public"."comment"'  # Указываем имя таблицы в базе данных
        ordering = ["created_at"]  # Сортировка по дате создания в прямом порядке


class Like(UUIDMixin):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"public"."like"'  # Указываем имя таблицы в базе данных
        unique_together = (
            "article",
            "user",
        )  # Если вам нужен сложный уникальный ключ на несколько полей.

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"
