from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Article, Like, Profile, Category, Tag, Comment
from .serializer import ArticleSerializer, LikeSerializer, CategorySerializer, TagSerializer, CommentSerializer

# Create your views here.

def index(request):
    return HttpResponse("Hello, this is the article index page.")


safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'


class MyPermission(permissions.BasePermission):
    """Class with my premissions.

    Args:
        permissions: Base django premissions
    """

    def has_permission(self, request: HttpRequest, _):
        """Check user premissions.

        Args:
            request (HttpRequest): request

        Returns:
            Bool user premissions.
        """
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False
    

def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [MyPermission]
        authentication_classes = [
            # Здесь можно добавить классы аутентификации, например:
            # SessionAuthentication,
            # TokenAuthentication,
            BasicAuthentication,
        ]
    return ViewSet

ArticleViewSet = create_viewset(Article, ArticleSerializer)
LikeViewSet = create_viewset(Like, LikeSerializer)
CategoryViewSet = create_viewset(Category, CategorySerializer)
TagViewSet = create_viewset(Tag, TagSerializer)
CommentViewSet = create_viewset(Comment, CommentSerializer)