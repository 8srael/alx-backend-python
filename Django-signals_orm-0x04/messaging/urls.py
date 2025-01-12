from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
