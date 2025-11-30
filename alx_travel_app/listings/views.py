from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing property listings.
    
    Provides full CRUD operations:
    - list: GET /api/listings/
    - create: POST /api/listings/
    - retrieve: GET /api/listings/{id}/
    - update: PUT /api/listings/{id}/
    - partial_update: PATCH /api/listings/{id}/
    - destroy: DELETE /api/listings/{id}/
    
    Additional filters:
    - Search by title, description, location
    - Filter by property_type, available
    - Order by price_per_night, created_at
    """
    
    queryset = Listing.objects.select_related('host').all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'available', 'location']
    search_fields = ['title', 'description', 'location', 'address']
    ordering_fields = ['price_per_night', 'created_at', 'bedrooms']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific listing."""
        listing = self.get_object()
        bookings = listing.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get only available listings."""
        available_listings = self.queryset.filter(available=True)
        serializer = self.get_serializer(available_listings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing bookings.
    
    Provides full CRUD operations:
    - list: GET /api/bookings/
    - create: POST /api/bookings/
    - retrieve: GET /api/bookings/{id}/
    - update: PUT /api/bookings/{id}/
    - partial_update: PATCH /api/bookings/{id}/
    - destroy: DELETE /api/bookings/{id}/
    
    Additional filters:
    - Filter by status, listing, guest
    - Order by check_in_date, total_price
    """
    
    queryset = Booking.objects.select_related('listing', 'guest').all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'listing', 'guest']
    ordering_fields = ['check_in_date', 'check_out_date', 'total_price', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a pending booking."""
        booking = self.get_object()
        if booking.status != 'pending':
            return Response(
                {'error': 'Only pending bookings can be confirmed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'confirmed'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()
        if booking.status in ['cancelled', 'completed']:
            return Response(
                {'error': f'Cannot cancel a {booking.status} booking.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'cancelled'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get bookings for the authenticated user (if authentication is enabled)."""
        # Note: This would work with authentication enabled
        # For now, requires guest_id parameter
        guest_id = request.query_params.get('guest_id')
        if guest_id:
            my_bookings = self.queryset.filter(guest_id=guest_id)
            serializer = self.get_serializer(my_bookings, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'guest_id parameter required'},
            status=status.HTTP_400_BAD_REQUEST
        )
