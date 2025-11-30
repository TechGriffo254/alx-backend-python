# ALX Travel App - API Development

A Django REST Framework-based API for managing property listings and bookings for a travel application.

## Features

- **Listings Management**: Full CRUD operations for property listings
- **Bookings Management**: Complete booking workflow with validation
- **RESTful API**: Follows REST principles with proper HTTP methods
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Filtering & Search**: Advanced filtering, search, and ordering capabilities
- **Data Validation**: Comprehensive validation for dates, capacity, and availability

## Tech Stack

- **Django 4.2+**: Web framework
- **Django REST Framework**: API toolkit
- **drf-yasg**: Swagger/OpenAPI documentation
- **django-filter**: Advanced filtering
- **SQLite**: Database (can be replaced with PostgreSQL/MySQL)

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x01/alx_travel_app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework drf-yasg django-filter
   ```

4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`

## API Documentation

### Access Swagger UI

Visit `http://127.0.0.1:8000/api/docs/` for interactive API documentation.

### API Endpoints

#### Listings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/listings/` | List all listings (with pagination) |
| POST | `/api/listings/` | Create a new listing |
| GET | `/api/listings/{id}/` | Retrieve a specific listing |
| PUT | `/api/listings/{id}/` | Update a listing (full) |
| PATCH | `/api/listings/{id}/` | Update a listing (partial) |
| DELETE | `/api/listings/{id}/` | Delete a listing |
| GET | `/api/listings/available/` | Get only available listings |
| GET | `/api/listings/{id}/bookings/` | Get bookings for a listing |

**Listing Fields:**
```json
{
  "id": 1,
  "title": "Cozy Beach Apartment",
  "description": "Beautiful apartment with ocean view",
  "property_type": "apartment",
  "price_per_night": "150.00",
  "location": "Miami Beach, FL",
  "address": "123 Ocean Drive, Miami Beach, FL 33139",
  "bedrooms": 2,
  "bathrooms": 2,
  "max_guests": 4,
  "amenities": "WiFi, Air Conditioning, Pool, Beach Access",
  "available": true,
  "host": {
    "id": 1,
    "username": "john_host",
    "email": "john@example.com"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Query Parameters:**
- `property_type`: Filter by type (apartment, house, villa, etc.)
- `location`: Filter by location
- `available`: Filter by availability (true/false)
- `search`: Search in title, description, location
- `ordering`: Order by price_per_night, created_at, bedrooms

**Example Requests:**
```bash
# Get all listings
GET /api/listings/

# Search for apartments
GET /api/listings/?property_type=apartment

# Search with text
GET /api/listings/?search=beach

# Order by price
GET /api/listings/?ordering=price_per_night
```

#### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings/` | List all bookings |
| POST | `/api/bookings/` | Create a new booking |
| GET | `/api/bookings/{id}/` | Retrieve a specific booking |
| PUT | `/api/bookings/{id}/` | Update a booking (full) |
| PATCH | `/api/bookings/{id}/` | Update a booking (partial) |
| DELETE | `/api/bookings/{id}/` | Delete a booking |
| POST | `/api/bookings/{id}/confirm/` | Confirm a pending booking |
| POST | `/api/bookings/{id}/cancel/` | Cancel a booking |
| GET | `/api/bookings/my_bookings/?guest_id={id}` | Get bookings for a guest |

**Booking Fields:**
```json
{
  "id": 1,
  "listing": {
    "id": 1,
    "title": "Cozy Beach Apartment",
    "location": "Miami Beach, FL"
  },
  "guest": {
    "id": 2,
    "username": "jane_guest",
    "email": "jane@example.com"
  },
  "check_in_date": "2024-03-01",
  "check_out_date": "2024-03-05",
  "number_of_guests": 2,
  "total_price": "600.00",
  "status": "confirmed",
  "special_requests": "Late check-in please",
  "created_at": "2024-01-15T14:20:00Z",
  "updated_at": "2024-01-16T09:15:00Z"
}
```

**Status Values:**
- `pending`: Newly created booking
- `confirmed`: Host confirmed the booking
- `cancelled`: Booking was cancelled
- `completed`: Guest checked out

**Query Parameters:**
- `status`: Filter by status
- `listing`: Filter by listing ID
- `guest`: Filter by guest ID
- `ordering`: Order by check_in_date, total_price, created_at

## Testing with Postman

### Setup

1. Import the Swagger documentation into Postman (via URL)
2. Set base URL: `http://127.0.0.1:8000`

### Example Test Scenarios

#### 1. Create a Listing

```http
POST /api/listings/
Content-Type: application/json

{
  "title": "Luxury Villa with Pool",
  "description": "Stunning 5-bedroom villa with private pool",
  "property_type": "villa",
  "price_per_night": "450.00",
  "location": "Los Angeles, CA",
  "address": "456 Sunset Blvd, Los Angeles, CA 90028",
  "bedrooms": 5,
  "bathrooms": 4,
  "max_guests": 10,
  "amenities": "Pool, Hot Tub, WiFi, Gym, Garden",
  "available": true,
  "host_id": 1
}
```

#### 2. Create a Booking

```http
POST /api/bookings/
Content-Type: application/json

{
  "listing_id": 1,
  "guest_id": 2,
  "check_in_date": "2024-03-10",
  "check_out_date": "2024-03-15",
  "number_of_guests": 4,
  "special_requests": "Need baby crib"
}
```

#### 3. Confirm a Booking

```http
POST /api/bookings/1/confirm/
```

#### 4. Search Available Listings

```http
GET /api/listings/available/?search=beach&ordering=price_per_night
```

## Project Structure

```
alx_travel_app/
├── alx_travel_app/          # Project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── listings/                # Main app
│   ├── models.py            # Listing & Booking models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # ViewSets
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin configurations
│   └── apps.py
├── manage.py                # Django management script
└── db.sqlite3               # Database (generated)
```

## Models

### Listing Model
- Property details (title, description, type)
- Location information
- Capacity (bedrooms, bathrooms, guests)
- Pricing and availability
- Host relationship

### Booking Model
- Guest and listing relationships
- Check-in/out dates
- Guest count and pricing
- Status tracking
- Special requests

## Advanced Features

### Custom Actions

1. **Listing.bookings()**: Get all bookings for a listing
2. **Booking.confirm()**: Confirm a pending booking
3. **Booking.cancel()**: Cancel a booking
4. **Booking.my_bookings()**: Get user's bookings

### Validation

- Check-out date must be after check-in
- Guest count cannot exceed max_guests
- Cannot book unavailable listings
- Only pending bookings can be confirmed
- Cannot cancel completed bookings

### Optimizations

- `select_related()` and `prefetch_related()` for efficient queries
- Pagination enabled (10 items per page)
- Indexed fields for better performance

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/`

Features:
- Manage listings and bookings
- Filter by multiple criteria
- Search functionality
- Readonly calculated fields

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing packages
   ```bash
   pip install djangorestframework drf-yasg django-filter
   ```

2. **Migration errors**: Reset and reapply migrations
   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Port already in use**: Use different port
   ```bash
   python manage.py runserver 8080
   ```

## Future Enhancements

- JWT authentication
- Image upload for listings
- Payment integration
- Email notifications
- Advanced search with date availability
- Rating and review system
- Real-time notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the ALX Backend Python specialization.

## Author

ALX Backend Python Student

## Support

For issues or questions, please open an issue on the repository.
