from django.contrib import admin

from .models import Article, Category, Comment, Like, Profile, Tag

# Здесь регистрируешь свои модели для отображения в админке
admin.site.register([Article, Like, Profile, Category, Tag, Comment])
