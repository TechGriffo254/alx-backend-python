"""Views for the messaging application."""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model."""
    queryset = Conversation.objects.all().prefetch_related(
        'participants',
        'messages'
    )
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """Add a message to a conversation."""
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model."""
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]

    def perform_create(self, serializer):
        """Set the sender when creating a message."""
        serializer.save()
