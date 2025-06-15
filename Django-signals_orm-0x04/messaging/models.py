# config/chats/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Added a 'role' field for implementing role-based access control.
    """
    class Role(models.TextChoices):
        USER = 'USER', 'User'
        MODERATOR = 'MODERATOR', 'Moderator'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.USER)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    The 'participants' field is a ManyToMany relationship with the User model.
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation ({self.id}) between: {', '.join([user.username for user in self.participants.all()])}"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    It has a foreign key to the Conversation it belongs to and the User who sent it.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.BooleanField(default=False)
    # conversation = models.ForeignKey(
    #     Conversation, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"


class MessageHistory(models.Model):
    """
    Abstract model to track message history.
    It can be extended by other models to keep a history of changes.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    content = models.TextField()
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_history')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} about message {self.message.id}"
