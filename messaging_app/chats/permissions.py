from rest_framework.permissions import BasePermission

class IsChatParticipant(BasePermission):
    """
    Custom permission to only allow participants of a chat to access it.
    """

    def has_permission(self, request, view):
        chat = view.get_object()
        return request.user in chat.participants.all()
