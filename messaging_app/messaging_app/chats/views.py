from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ConversationViewSet(viewsets.ModelViewSet):
    """Conversation View Set"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation by accepting a list of participant IDs
        Body:
        {
            "participant_ids": [1, 2, 3]
        }
        """
        participant_ids = request.data.get("participant_ids", [])
        if not participant_ids:
            return Response({"error": "participant_ids list required"}, status=status.HTTP_400_BAD_REQUEST)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """Message View Set"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['conversation']
    search_fields = ['content']

    def perform_create(self, serializer):
        """
        When sending a message, automatically set the sender to the authenticated user
        """
        serializer.save(sender=self.request.user)

