from django.contrib import admin
from .models import Article, Like, Profile, Category, Tag, Comment
# Здесь регистрируешь свои модели для отображения в админке
admin.site.register([Article, Like, Profile, Category, Tag, Comment])