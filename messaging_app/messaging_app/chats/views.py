from rest_framework import viewsets, routers
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """Conversation View Set"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    

class MessageViewSet(viewsets.ModelViewSet):
    """Message View Set"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
