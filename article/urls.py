from django.urls import path, include
from . import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'likes', views.LikeViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)



urlpatterns = [
    path("", views.index, name="article_index"),
    path("api/", include(router.urls), name="api"),
]