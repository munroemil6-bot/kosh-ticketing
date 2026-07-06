"""
Kosh Ticketing - Utility Functions
Helper functions for QR codes, order numbers, and common operations
"""

import qrcode
import io
import base64
import random
import string
from datetime import datetime, timedelta
from flask import current_app
from app import db
from app.models import Order, TicketTier


def generate_order_number():
    """Generate unique order number: KOSH-YYYYMMDD-XXXXX"""
    date_str = datetime.utcnow().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"KOSH-{date_str}-{random_str}"


def generate_ticket_number():
    """Generate unique ticket number: TKT-XXXXX-XXXXX"""
    return f"TKT-{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}"


def generate_qr_code(data, size=10, border=2):
    """Generate QR code as base64 encoded PNG"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"


def calculate_order_fees(subtotal, fee_percentage=0.05, fixed_fee=0.99):
    """Calculate order fees (service fee + processing fee)"""
    percentage_fee = float(subtotal) * fee_percentage
    return round(percentage_fee + fixed_fee, 2)


def reserve_tickets(order_id, ticket_selections):
    """
    Reserve tickets by incrementing reserved count.
    Returns True if successful, False if insufficient inventory.
    """
    try:
        for selection in ticket_selections:
            tier_id = selection['ticket_tier_id']
            quantity = selection['quantity']

            tier = TicketTier.query.get(tier_id)
            if not tier:
                return False, f"Ticket tier {tier_id} not found"

            if tier.tickets_available < quantity:
                return False, f"Only {tier.tickets_available} tickets available for {tier.name}"

            # Check per-order limits
            if quantity < tier.min_per_order:
                return False, f"Minimum {tier.min_per_order} tickets required for {tier.name}"
            if quantity > tier.max_per_order:
                return False, f"Maximum {tier.max_per_order} tickets allowed for {tier.name}"

            # Reserve tickets
            tier.quantity_reserved += quantity

        db.session.commit()
        return True, "Tickets reserved successfully"

    except Exception as e:
        db.session.rollback()
        return False, str(e)


def release_tickets(order_id):
    """Release reserved tickets when order expires or is cancelled"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return False, "Order not found"

        for item in order.items:
            tier = TicketTier.query.get(item.ticket_tier_id)
            if tier:
                tier.quantity_reserved -= item.quantity
                if tier.quantity_reserved < 0:
                    tier.quantity_reserved = 0

        db.session.commit()
        return True, "Tickets released"

    except Exception as e:
        db.session.rollback()
        return False, str(e)


def confirm_tickets(order_id):
    """Move reserved tickets to sold when payment is confirmed"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return False, "Order not found"

        for item in order.items:
            tier = TicketTier.query.get(item.ticket_tier_id)
            if tier:
                tier.quantity_reserved -= item.quantity
                tier.quantity_sold += item.quantity

        db.session.commit()
        return True, "Tickets confirmed"

    except Exception as e:
        db.session.rollback()
        return False, str(e)


def slugify(text):
    """Create URL-friendly slug from text"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text[:200]


def format_currency(amount, currency='USD'):
    """Format amount as currency string"""
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    symbol = symbols.get(currency, '$')
    return f"{symbol}{float(amount):,.2f}"


def paginate(query, page=1, per_page=12):
    """Helper for pagination"""
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }
