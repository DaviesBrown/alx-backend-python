from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Conversation, Message, User
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    """User View Set"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'email']
    filterset_fields = ['is_active', 'is_staff']

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
        if request.user.is_authenticated:
            current_user_id = str(request.user.user_id)
            if current_user_id not in participant_ids:
                participant_ids.append(current_user_id)
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

