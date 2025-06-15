# config/chats/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, serializers
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    Permissions are handled to ensure users can only access their own conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
        return self.request.user.conversations.prefetch_related('participants', 'messages').all()

    def perform_create(self, serializer):
        """
        Override to add the creating user to the participants list.
        """
        participants_data = serializer.validated_data.get(
            'participant_ids', [])
        participants_users = User.objects.filter(id__in=participants_data)

        # Add the current user to the conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.participants.add(*participants_users)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or created within a conversation.
    - Pagination is enabled (20 messages per page).
    - Filtering is enabled by sender username and date range.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Returns a list of messages for a specific conversation,
        identified by `conversation_pk` from the URL.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            # Ensure the user has permission to view messages in this conversation
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
                if self.request.user in conversation.participants.all():
                    return conversation.messages.all().order_by('timestamp')
            except Conversation.DoesNotExist:
                return Message.objects.none()
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        Creates a message and assigns the sender and conversation automatically.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(pk=conversation_pk)
        except Conversation.DoesNotExist:
            # This case should ideally not be hit if permissions are checked correctly
            raise serializers.ValidationError("Conversation not found.")

        # The IsParticipantOfConversation permission on the ConversationViewSet
        # already ensures the user is part of the conversation.
        serializer.save(sender=self.request.user, conversation=conversation)

class UserViewSet(viewsets.ModelViewSet):
    """User View Set with account deletion functionality"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_user(self, request):
        """
        Delete the authenticated user's account
        This will trigger the post_delete signal to clean up related data
        """
        user = request.user
        
        # Optional: Add confirmation check
        confirmation = request.data.get('confirm_deletion', False)
        if not confirmation:
            return Response(
                {"error": "Account deletion requires confirmation. Set 'confirm_deletion': true"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Log out the user before deletion
            logout(request)
            
            # Store user info for response
            user_id = user.user_id
            username = getattr(user, 'username', 'User')
            
            # Delete the user - this will trigger the post_delete signal
            user.delete()
            
            return Response(
                {
                    "message": f"User account {username} (ID: {user_id}) has been successfully deleted",
                    "deleted_user_id": user_id
                }, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": f"Failed to delete account: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
