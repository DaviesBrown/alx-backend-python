from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

class MessagingModelTests(TestCase):
    """
    Tests for the messaging models.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password123', email='user2@example.com')

    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello there!"
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, "Hello there!")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, this is a test message.'
        )
        notification = Notification.objects.filter(user=self.user2, message=msg)
        self.assertTrue(notification.exists())

    def test_message_editing(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Initial content"
        )
        original_content = message.content
        message.content = "Edited content"
        message.save()

        # Check if the content was updated
        self.assertNotEqual(message.content, original_content)
        self.assertTrue(message.is_edited)

        # Check if a history entry was created
        history_entry = MessageHistory.objects.filter(message=message)
        self.assertTrue(history_entry.exists())
        self.assertEqual(history_entry.first().content, original_content)
