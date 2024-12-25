from django.urls import path, include
from rest_framework.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Root router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Include the routers
urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
