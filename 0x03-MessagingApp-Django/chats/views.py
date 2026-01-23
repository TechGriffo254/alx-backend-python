"""Views for the messaging application."""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer
)
from .permissions import (
    IsParticipantOfConversation,
    IsMessageSender,
    IsAdminOrOwner
)
from .pagination import MessagePagination, ConversationPagination
from .filters import MessageFilter, ConversationFilter


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Set permissions based on action.
        Allow anyone to create (register), but require authentication for other actions.
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrOwner()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        Filter queryset based on user role.
        Regular users can only see themselves, admins can see all.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'admin' or user.is_staff:
                return User.objects.all()
            return User.objects.filter(user_id=user.user_id)
        return User.objects.none()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current authenticated user."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = ConversationPagination
    filterset_class = ConversationFilter
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return only conversations where the user is a participant.
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(
                participants=user
            ).prefetch_related('participants', 'messages').distinct()
        return Conversation.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a conversation and automatically add the creator as a participant.
        """
        conversation = serializer.save()
        # Add the creator as a participant if not already added
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsParticipantOfConversation])
    def add_message(self, request, pk=None):
        """
        Add a message to a conversation.
        Only participants can send messages.
        """
        conversation = self.get_object()
        
        # Verify user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {'error': 'You must be a participant to send messages'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create message data with sender and conversation
        message_data = request.data.copy()
        message_data['sender_id'] = request.user.user_id
        message_data['conversation'] = conversation.conversation_id
        
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsParticipantOfConversation])
    def messages(self, request, pk=None):
        """
        Get all messages in a conversation with pagination.
        """
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('-sent_at')
        
        # Apply pagination
        paginator = MessagePagination()
        paginated_messages = paginator.paginate_queryset(messages, request)
        
        serializer = MessageSerializer(paginated_messages, many=True)
        return paginator.get_paginated_response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filterset_class = MessageFilter
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """
        Return only messages from conversations where the user is a participant.
        """
        user = self.request.user
        if user.is_authenticated:
            return Message.objects.filter(
                conversation__participants=user
            ).select_related('sender', 'conversation').distinct()
        return Message.objects.none()
    
    def get_permissions(self):
        """
        Set permissions based on action.
        Only the sender can update or delete their messages.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsParticipantOfConversation(), IsMessageSender()]
        return [IsAuthenticated(), IsParticipantOfConversation()]
    
    def perform_create(self, serializer):
        """
        Set the sender when creating a message.
        Verify the user is a participant of the conversation.
        """
        conversation = serializer.validated_data.get('conversation')
        
        # Verify user is a participant
        if self.request.user not in conversation.participants.all():
            raise serializers.ValidationError(
                'You must be a participant of the conversation to send messages'
            )
        
        serializer.save(sender=self.request.user)
