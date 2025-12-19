import logging

from django.http import HttpRequest, HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.authentication import BasicAuthentication

from .decorators import track_db_latency
from .models import Article, Category, Comment, Like, Tag
from .serializer import (
    ArticleSerializer,
    CategorySerializer,
    CommentSerializer,
    LikeSerializer,
    TagSerializer,
)

# Create your views here.

logger = logging.getLogger(__name__)


@track_db_latency("index")
def index(request):
    logger.info("AAAAAAAAAAAAAAAAa")
    return HttpResponse("Hello, this is the article index page.")


safe_methods = "GET", "HEAD", "OPTIONS"
unsafe_methods = "POST", "DELETE", "PUT"


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

        @track_db_latency(f"{model_class.__name__}_create")
        def create(self, request, *args, **kwargs):
            return super().create(request, *args, **kwargs)

        @track_db_latency(f"{model_class.__name__}_list")
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

        @track_db_latency(f"{model_class.__name__}_retrieve")
        def retrieve(self, request, *args, **kwargs):
            return super().retrieve(request, *args, **kwargs)

        @track_db_latency(f"{model_class.__name__}_update")
        def update(self, request, *args, **kwargs):
            return super().update(request, *args, **kwargs)

        @track_db_latency(f"{model_class.__name__}_destroy")
        def destroy(self, request, *args, **kwargs):
            return super().destroy(request, *args, **kwargs)

    return ViewSet


ArticleViewSet = create_viewset(Article, ArticleSerializer)
LikeViewSet = create_viewset(Like, LikeSerializer)
CategoryViewSet = create_viewset(Category, CategorySerializer)
TagViewSet = create_viewset(Tag, TagSerializer)
CommentViewSet = create_viewset(Comment, CommentSerializer)
