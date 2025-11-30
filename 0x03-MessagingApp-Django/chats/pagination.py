"""Custom pagination classes for the messaging application."""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages.
    Returns 20 messages per page by default.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """Return paginated response with page.paginator.count."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class ConversationPagination(PageNumberPagination):
    """
    Custom pagination for conversations.
    Returns 10 conversations per page by default.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """Return paginated response with page.paginator.count."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
