"""
Kosh Ticketing - Marshmallow Schemas
Request/response validation and serialization
"""

from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from datetime import datetime

class UserSchema(Schema):
    """User schema for registration and profile"""
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=6))
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.String(validate=validate.Length(max=20))
    role = fields.String(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        if not value or '@' not in value:
            raise ValidationError('Invalid email address')

class UserLoginSchema(Schema):
    """User login schema"""
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

class TicketTierSchema(Schema):
    """Ticket tier schema"""
    id = fields.Integer(dump_only=True)
    event_id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    price = fields.Float(required=True)
    original_price = fields.Float()
    currency = fields.String()
    quantity_total = fields.Integer(required=True)
    quantity_sold = fields.Integer(dump_only=True)
    quantity_reserved = fields.Integer(dump_only=True)
    tickets_available = fields.Integer(dump_only=True)
    is_sold_out = fields.Boolean(dump_only=True)
    is_on_sale = fields.Boolean(dump_only=True)
    min_per_order = fields.Integer()
    max_per_order = fields.Integer()
    sale_start = fields.DateTime()
    sale_end = fields.DateTime()
    benefits = fields.List(fields.String())
    percent_sold = fields.Float(dump_only=True)

class EventSchema(Schema):
    """Event schema"""
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    subtitle = fields.String()
    description = fields.String(required=True)
    rich_description = fields.String()
    category = fields.String(required=True)
    status = fields.String(dump_only=True)

    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime()
    doors_open = fields.DateTime()

    venue_name = fields.String(required=True)
    venue_address = fields.String()
    venue_city = fields.String()
    venue_country = fields.String()
    venue_latitude = fields.Float()
    venue_longitude = fields.Float()

    banner_image = fields.String()
    thumbnail_image = fields.String()
    gallery_images = fields.List(fields.String())

    organizer_id = fields.Integer(dump_only=True)
    organizer_name = fields.String()

    is_featured = fields.Boolean()
    is_public = fields.Boolean()
    age_restriction = fields.String()
    slug = fields.String()
    tags = fields.List(fields.String())

    total_tickets_sold = fields.Integer(dump_only=True)
    total_capacity = fields.Integer(dump_only=True)
    is_sold_out = fields.Boolean(dump_only=True)
    lowest_price = fields.Float(dump_only=True)

    ticket_tiers = fields.List(fields.Nested(TicketTierSchema), dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    published_at = fields.DateTime(dump_only=True)

class EventCreateSchema(Schema):
    """Schema for creating events"""
    title = fields.String(required=True)
    subtitle = fields.String()
    description = fields.String(required=True)
    rich_description = fields.String()
    category = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime()
    doors_open = fields.DateTime()
    venue_name = fields.String(required=True)
    venue_address = fields.String()
    venue_city = fields.String()
    venue_country = fields.String()
    banner_image = fields.String()
    thumbnail_image = fields.String()
    gallery_images = fields.List(fields.String())
    organizer_name = fields.String()
    is_public = fields.Boolean()
    age_restriction = fields.String()
    tags = fields.List(fields.String())
    ticket_tiers = fields.List(fields.Dict(), required=True)

class EventFilterSchema(Schema):
    """Schema for event filtering query parameters"""
    category = fields.String()
    city = fields.String()
    date_from = fields.DateTime()
    date_to = fields.DateTime()
    search = fields.String()
    featured = fields.Boolean()
    status = fields.String()
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=12)
    sort_by = fields.String(missing='start_date')
    sort_order = fields.String(missing='asc')

class TicketSelectionSchema(Schema):
    """Schema for ticket selection"""
    ticket_tier_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))

class OrderCreateSchema(Schema):
    """Schema for creating orders"""
    event_id = fields.Integer(required=True)
    tickets = fields.List(fields.Nested(TicketSelectionSchema), required=True)
    guest_email = fields.Email()
    guest_phone = fields.String()

    @validates('tickets')
    def validate_tickets(self, value):
        if not value:
            raise ValidationError('At least one ticket must be selected')

class OrderItemSchema(Schema):
    """Order item schema"""
    id = fields.Integer(dump_only=True)
    ticket_tier_id = fields.Integer()
    ticket_tier_name = fields.String()
    event_id = fields.Integer()
    event_title = fields.String()
    quantity = fields.Integer()
    unit_price = fields.Float()
    total_price = fields.Float()

class AttendeeSchema(Schema):
    """Attendee schema"""
    id = fields.Integer(dump_only=True)
    order_id = fields.Integer()
    ticket_tier_id = fields.Integer()
    ticket_tier_name = fields.String()
    event_title = fields.String()
    event_date = fields.DateTime()
    venue_name = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String()
    phone = fields.String()
    ticket_number = fields.String()
    qr_code = fields.String()
    is_checked_in = fields.Boolean()
    checked_in_at = fields.DateTime()
    created_at = fields.DateTime()

class OrderSchema(Schema):
    """Order schema"""
    id = fields.Integer(dump_only=True)
    order_number = fields.String(dump_only=True)
    user_id = fields.Integer()
    guest_email = fields.String()
    status = fields.String()
    subtotal = fields.Float()
    fees = fields.Float()
    tax = fields.Float()
    discount = fields.Float()
    total = fields.Float()
    currency = fields.String()
    payment_status = fields.String()
    paid_at = fields.DateTime()
    created_at = fields.DateTime()
    expires_at = fields.DateTime()
    total_tickets = fields.Integer(dump_only=True)
    items = fields.List(fields.Nested(OrderItemSchema), dump_only=True)
    attendees = fields.List(fields.Nested(AttendeeSchema), dump_only=True)

class AttendeeCreateSchema(Schema):
    """Schema for creating attendee details"""
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String()

class PaymentSchema(Schema):
    """Mock payment schema"""
    order_id = fields.Integer(required=True)
    payment_method = fields.String(required=True)
    card_number = fields.String(load_only=True)
    card_expiry = fields.String(load_only=True)
    card_cvc = fields.String(load_only=True)
    billing_name = fields.String()
    billing_address = fields.String()

class DashboardStatsSchema(Schema):
    """Admin dashboard stats"""
    total_events = fields.Integer()
    total_orders = fields.Integer()
    total_revenue = fields.Float()
    total_tickets_sold = fields.Integer()
    recent_orders = fields.List(fields.Nested(OrderSchema))
    events_performance = fields.List(fields.Dict())
