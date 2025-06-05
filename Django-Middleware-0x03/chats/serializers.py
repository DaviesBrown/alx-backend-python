# chats/serializers.py

from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the CustomUser model.
    Only exposes fields we want the client to see.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'status_message']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializes individual Message instances.
    - Uses an explicit CharField for 'content' so we can validate it.
    - Adds a SerializerMethodField to format the timestamp.
    """
    sender = UserSerializer(read_only=True)
    content = serializers.CharField(
        max_length=2000,
        write_only=False,      # Clients can both read and write this field
        help_text="The body of the message"
    )
    custom_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'custom_timestamp']

    def get_custom_timestamp(self, obj):
        """
        Returns the timestamp formatted as 'YYYY-MM-DD HH:MM:SS'
        """
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def validate_content(self, value):
        """
        Ensure the message content is not empty or just whitespace.
        Raise a ValidationError if it is.
        """
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be blank.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializes Conversation instances.
    - Nests UserSerializer for participants.
    - Nests MessageSerializer for all messages in this conversation.
    - Adds a SerializerMethodField to return a summary of the last message.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message_summary = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'last_message_summary', 'messages']

    def get_last_message_summary(self, obj):
        """
        Returns the first 50 characters of the most recent message in this conversation,
        or an empty string if there are no messages yet.
        """
        last = obj.messages.order_by('-timestamp').first()
        if last:
            # Truncate to 50 chars with ellipsis if needed
            snippet = last.content[:50]
            return snippet + ('...' if len(last.content) > 50 else '')
        return ""

