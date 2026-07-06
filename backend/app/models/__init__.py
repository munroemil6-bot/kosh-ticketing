"""
Kosh Ticketing - Database Models
SQLAlchemy ORM models for Users, Events, Ticket Tiers, Orders, and Attendees
"""

from app import db
from datetime import datetime, timedelta
import enum

class UserRole(enum.Enum):
    """User role enumeration for RBAC"""
    CUSTOMER = "customer"
    ORGANIZER = "organizer"
    ADMIN = "admin"

class EventCategory(enum.Enum):
    """Event category enumeration"""
    CONCERT = "concert"
    THEATRE = "theatre"
    FESTIVAL = "festival"
    SPORTS = "sports"
    COMEDY = "comedy"
    EXHIBITION = "exhibition"
    WORKSHOP = "workshop"
    OTHER = "other"

class EventStatus(enum.Enum):
    """Event status lifecycle"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ON_SALE = "on_sale"
    SOLD_OUT = "sold_out"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class OrderStatus(enum.Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class User(db.Model):
    """User model - supports customers, organizers, and admins"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    organized_events = db.relationship('Event', backref='organizer', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Event(db.Model):
    """Event model - the core entity for ticketing"""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    description = db.Column(db.Text, nullable=False)
    rich_description = db.Column(db.Text)  # HTML formatted description

    # Event details
    category = db.Column(db.Enum(EventCategory), nullable=False)
    status = db.Column(db.Enum(EventStatus), default=EventStatus.DRAFT, nullable=False)

    # Date and time
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    doors_open = db.Column(db.DateTime)

    # Venue
    venue_name = db.Column(db.String(200), nullable=False)
    venue_address = db.Column(db.String(300))
    venue_city = db.Column(db.String(100))
    venue_country = db.Column(db.String(100))
    venue_latitude = db.Column(db.Float)
    venue_longitude = db.Column(db.Float)

    # Media
    banner_image = db.Column(db.String(500))  # URL to banner image
    thumbnail_image = db.Column(db.String(500))
    gallery_images = db.Column(db.JSON)  # Array of image URLs

    # Organizer
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organizer_name = db.Column(db.String(100))

    # Settings
    is_featured = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    age_restriction = db.Column(db.String(20))  # "18+", "21+", "All Ages"

    # SEO & Metadata
    slug = db.Column(db.String(200), unique=True, index=True)
    tags = db.Column(db.JSON)  # Array of tags

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    # Relationships
    ticket_tiers = db.relationship('TicketTier', backref='event', lazy='dynamic', 
                                   cascade='all, delete-orphan', order_by='TicketTier.price')

    @property
    def total_tickets_sold(self):
        """Calculate total tickets sold across all tiers"""
        return sum(tier.tickets_sold for tier in self.ticket_tiers)

    @property
    def total_capacity(self):
        """Calculate total capacity across all tiers"""
        return sum(tier.quantity_total for tier in self.ticket_tiers)

    @property
    def is_sold_out(self):
        """Check if all tiers are sold out"""
        return all(tier.is_sold_out for tier in self.ticket_tiers)

    @property
    def lowest_price(self):
        """Get the lowest active ticket price"""
        active_tiers = [t for t in self.ticket_tiers if t.is_active and not t.is_sold_out]
        if not active_tiers:
            return None
        return min(t.price for t in active_tiers)

    def to_dict(self, include_tiers=False):
        data = {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'description': self.description,
            'rich_description': self.rich_description,
            'category': self.category.value,
            'status': self.status.value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'doors_open': self.doors_open.isoformat() if self.doors_open else None,
            'venue_name': self.venue_name,
            'venue_address': self.venue_address,
            'venue_city': self.venue_city,
            'venue_country': self.venue_country,
            'banner_image': self.banner_image,
            'thumbnail_image': self.thumbnail_image,
            'gallery_images': self.gallery_images or [],
            'organizer_id': self.organizer_id,
            'organizer_name': self.organizer_name,
            'is_featured': self.is_featured,
            'is_public': self.is_public,
            'age_restriction': self.age_restriction,
            'slug': self.slug,
            'tags': self.tags or [],
            'total_tickets_sold': self.total_tickets_sold,
            'total_capacity': self.total_capacity,
            'is_sold_out': self.is_sold_out,
            'lowest_price': self.lowest_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }

        if include_tiers:
            data['ticket_tiers'] = [tier.to_dict() for tier in self.ticket_tiers]

        return data

class TicketTier(db.Model):
    """Ticket Tier model - different pricing levels for an event"""
    __tablename__ = 'ticket_tiers'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    # Tier details
    name = db.Column(db.String(100), nullable=False)  # "Early Bird", "VIP", "General Admission"
    description = db.Column(db.Text)

    # Pricing
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2))  # For showing discounts
    currency = db.Column(db.String(3), default='USD')

    # Inventory
    quantity_total = db.Column(db.Integer, nullable=False)
    quantity_sold = db.Column(db.Integer, default=0)
    quantity_reserved = db.Column(db.Integer, default=0)  # Reserved but not paid

    # Limits
    min_per_order = db.Column(db.Integer, default=1)
    max_per_order = db.Column(db.Integer, default=10)

    # Availability
    sale_start = db.Column(db.DateTime)
    sale_end = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Benefits (for VIP tiers)
    benefits = db.Column(db.JSON)  # Array of benefit strings

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order_items = db.relationship('OrderItem', backref='ticket_tier', lazy='dynamic')

    @property
    def tickets_sold(self):
        """Total tickets sold (paid + reserved)"""
        return self.quantity_sold + self.quantity_reserved

    @property
    def tickets_available(self):
        """Remaining available tickets"""
        return max(0, self.quantity_total - self.tickets_sold)

    @property
    def is_sold_out(self):
        """Check if tier is sold out"""
        return self.tickets_available <= 0

    @property
    def is_on_sale(self):
        """Check if tier is currently on sale"""
        now = datetime.utcnow()
        if self.sale_start and now < self.sale_start:
            return False
        if self.sale_end and now > self.sale_end:
            return False
        return self.is_active and not self.is_sold_out

    @property
    def percent_sold(self):
        """Percentage of tickets sold"""
        if self.quantity_total == 0:
            return 0
        return (self.tickets_sold / self.quantity_total) * 100

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'original_price': float(self.original_price) if self.original_price else None,
            'currency': self.currency,
            'quantity_total': self.quantity_total,
            'quantity_sold': self.quantity_sold,
            'quantity_reserved': self.quantity_reserved,
            'tickets_available': self.tickets_available,
            'is_sold_out': self.is_sold_out,
            'is_on_sale': self.is_on_sale,
            'min_per_order': self.min_per_order,
            'max_per_order': self.max_per_order,
            'sale_start': self.sale_start.isoformat() if self.sale_start else None,
            'sale_end': self.sale_end.isoformat() if self.sale_end else None,
            'benefits': self.benefits or [],
            'percent_sold': round(self.percent_sold, 1)
        }

class Order(db.Model):
    """Order model - represents a ticket purchase transaction"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)

    # User info (supports guest checkout)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    guest_email = db.Column(db.String(120))
    guest_phone = db.Column(db.String(20))

    # Order status
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    # Financials
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    fees = db.Column(db.Numeric(10, 2), default=0)
    tax = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')

    # Payment (mock)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
    payment_reference = db.Column(db.String(100))
    paid_at = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # Reservation expiry

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', 
                           cascade='all, delete-orphan')
    attendees = db.relationship('Attendee', backref='order', lazy='dynamic',
                               cascade='all, delete-orphan')

    @property
    def total_tickets(self):
        """Total number of tickets in order"""
        return sum(item.quantity for item in self.items)

    def to_dict(self, include_items=False, include_attendees=False):
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'guest_email': self.guest_email,
            'status': self.status.value,
            'subtotal': float(self.subtotal),
            'fees': float(self.fees),
            'tax': float(self.tax),
            'discount': float(self.discount),
            'total': float(self.total),
            'currency': self.currency,
            'payment_status': self.payment_status,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'total_tickets': self.total_tickets
        }

        if include_items:
            data['items'] = [item.to_dict() for item in self.items]

        if include_attendees:
            data['attendees'] = [attendee.to_dict() for attendee in self.attendees]

        return data

class OrderItem(db.Model):
    """Order Item model - individual line items in an order"""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    ticket_tier_id = db.Column(db.Integer, db.ForeignKey('ticket_tiers.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_tier_id': self.ticket_tier_id,
            'ticket_tier_name': self.ticket_tier.name if self.ticket_tier else None,
            'event_id': self.ticket_tier.event_id if self.ticket_tier else None,
            'event_title': self.ticket_tier.event.title if self.ticket_tier and self.ticket_tier.event else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price)
        }

class Attendee(db.Model):
    """Attendee model - ticket holder details for each ticket"""
    __tablename__ = 'attendees'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    ticket_tier_id = db.Column(db.Integer, db.ForeignKey('ticket_tiers.id'), nullable=False)

    # Attendee details
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))

    # Ticket info
    ticket_number = db.Column(db.String(50), unique=True, nullable=False)
    qr_code = db.Column(db.String(500))  # QR code data/URL
    is_checked_in = db.Column(db.Boolean, default=False)
    checked_in_at = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    ticket_tier = db.relationship('TicketTier')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'ticket_tier_id': self.ticket_tier_id,
            'ticket_tier_name': self.ticket_tier.name if self.ticket_tier else None,
            'event_title': self.ticket_tier.event.title if self.ticket_tier and self.ticket_tier.event else None,
            'event_date': self.ticket_tier.event.start_date.isoformat() if self.ticket_tier and self.ticket_tier.event else None,
            'venue_name': self.ticket_tier.event.venue_name if self.ticket_tier and self.ticket_tier.event else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'ticket_number': self.ticket_number,
            'qr_code': self.qr_code,
            'is_checked_in': self.is_checked_in,
            'checked_in_at': self.checked_in_at.isoformat() if self.checked_in_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
