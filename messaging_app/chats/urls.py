from rest_framework import viewsets, routers
from .views import ConversationViewSet, MessageViewSet
router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = router.urls