from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, DeleteUserView, NotificationViewSet, ThreadedConversationView

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/account/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('conversation/<int:message_id>/', ThreadedConversationView.as_view(), name='threaded_conversation')
] 
