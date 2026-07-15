"""
Kosh Ticketing - Orders Routes
Handles ticket reservation, checkout, and payment processing
"""

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime, timedelta
from app import db
from app.models import (
    Order, OrderItem, Attendee, TicketTier, Event, User,
    OrderStatus, EventStatus, UserRole
)
from app.schemas import OrderCreateSchema, OrderSchema, PaymentSchema, AttendeeCreateSchema
from app.utils import (
    generate_order_number, generate_ticket_number, generate_qr_code,
    calculate_order_fees, reserve_tickets, confirm_tickets, release_tickets
)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
create_schema = OrderCreateSchema()
payment_schema = PaymentSchema()


def _get_current_user_id():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    try:
        identity = get_jwt_identity()
    except Exception:
        return None

    try:
        return int(identity)
    except (TypeError, ValueError):
        return None


@jwt_required()
def create_order():
    """Create a new order (reserves tickets)"""
    try:
        current_user_id = _get_current_user_id()
        if current_user_id is None:
            return jsonify({'error': 'Authentication required'}), 401

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.role != UserRole.CUSTOMER:
            return jsonify({'error': 'Only customers can purchase tickets'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate
        errors = create_schema.validate(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Check event exists and is on sale
        event = Event.query.get(data['event_id'])
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if event.status == EventStatus.CANCELLED:
            return jsonify({'error': 'This event has been cancelled'}), 400

        if event.status == EventStatus.COMPLETED:
            return jsonify({'error': 'This event has already taken place'}), 400

        # Calculate totals
        subtotal = 0
        order_items_data = []

        for ticket_selection in data['tickets']:
            tier = TicketTier.query.get(ticket_selection['ticket_tier_id'])
            if not tier or tier.event_id != event.id:
                return jsonify({'error': 'Invalid ticket tier for this event'}), 400

            if not tier.is_on_sale:
                return jsonify({'error': f'Tickets for "{tier.name}" are not available for purchase'}), 400

            quantity = ticket_selection['quantity']
            unit_price = float(tier.price)
            total_price = unit_price * quantity
            subtotal += total_price

            order_items_data.append({
                'ticket_tier_id': tier.id,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price
            })

        # Calculate fees
        fees = calculate_order_fees(subtotal)
        total = subtotal + fees

        # Create order
        order = Order(
            order_number=generate_order_number(),
            user_id=user.id,
            guest_email=data.get('guest_email'),
            guest_phone=data.get('guest_phone'),
            status=OrderStatus.PENDING,
            subtotal=subtotal,
            fees=fees,
            tax=0,
            discount=0,
            total=total,
            currency='USD',
            expires_at=datetime.utcnow() + timedelta(minutes=15)
        )

        db.session.add(order)
        db.session.flush()

        # Create order items
        for item_data in order_items_data:
            item = OrderItem(
                order_id=order.id,
                ticket_tier_id=item_data['ticket_tier_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price']
            )
            db.session.add(item)

        # Reserve tickets
        success, message = reserve_tickets(order.id, data['tickets'])
        if not success:
            db.session.rollback()
            return jsonify({'error': message}), 409

        db.session.commit()

        return jsonify({
            'message': 'Order created - tickets reserved for 15 minutes',
            'order': order.to_dict(include_items=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order', 'details': str(e)}), 500


def get_order(order_id):
    """Get order details"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        return jsonify({
            'order': order.to_dict(include_items=True, include_attendees=True)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch order', 'details': str(e)}), 500


def add_attendees(order_id):
    """Add attendee details to order"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if order.status != OrderStatus.PENDING:
            return jsonify({'error': 'Cannot modify attendees for this order'}), 400

        if order.expires_at and order.expires_at < datetime.utcnow():
            return jsonify({'error': 'Order reservation has expired'}), 410

        data = request.get_json()
        if not data or 'attendees' not in data:
            return jsonify({'error': 'Attendee data required'}), 400

        attendees_data = data['attendees']

        # Validate attendee count matches ticket count
        total_tickets = sum(item.quantity for item in order.items)
        if len(attendees_data) != total_tickets:
            return jsonify({
                'error': f'Expected {total_tickets} attendees, got {len(attendees_data)}'
            }), 400

        # Create attendees
        attendee_idx = 0
        for item in order.items:
            tier = TicketTier.query.get(item.ticket_tier_id)
            for _ in range(item.quantity):
                attendee_info = attendees_data[attendee_idx]

                # Generate QR code
                ticket_num = generate_ticket_number()
                qr_data = f"KOSH:{ticket_num}:{order.order_number}"
                qr_code = generate_qr_code(qr_data)

                attendee = Attendee(
                    order_id=order.id,
                    ticket_tier_id=item.ticket_tier_id,
                    first_name=attendee_info['first_name'],
                    last_name=attendee_info['last_name'],
                    email=attendee_info['email'],
                    phone=attendee_info.get('phone'),
                    ticket_number=ticket_num,
                    qr_code=qr_code
                )
                db.session.add(attendee)
                attendee_idx += 1

        db.session.commit()

        return jsonify({
            'message': 'Attendee details added',
            'order': order.to_dict(include_items=True, include_attendees=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add attendees', 'details': str(e)}), 500


def process_payment(order_id):
    """Process mock payment and confirm order"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if order.status != OrderStatus.PENDING:
            return jsonify({'error': 'Order cannot be paid'}), 400

        if order.expires_at and order.expires_at < datetime.utcnow():
            release_tickets(order.id)
            order.status = OrderStatus.CANCELLED
            db.session.commit()
            return jsonify({'error': 'Order reservation has expired'}), 410

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Payment data required'}), 400

        # Validate payment data
        errors = payment_schema.validate(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        payment_success = True

        if payment_success:
            success, message = confirm_tickets(order.id)
            if not success:
                return jsonify({'error': message}), 500

            order.status = OrderStatus.PAID
            order.payment_status = 'completed'
            order.payment_method = data.get('payment_method')
            order.payment_reference = f"MOCK-{generate_order_number()}"
            order.paid_at = datetime.utcnow()

            event = Event.query.get(order.items[0].ticket_tier.event_id)
            if event and event.is_sold_out:
                event.status = EventStatus.SOLD_OUT

            db.session.commit()

            return jsonify({
                'message': 'Payment successful - order confirmed',
                'order': order.to_dict(include_items=True, include_attendees=True)
            }), 200
        else:
            return jsonify({'error': 'Payment failed'}), 402

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Payment processing failed', 'details': str(e)}), 500


def cancel_order(order_id):
    """Cancel order and release tickets"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            return jsonify({'error': 'Order cannot be cancelled'}), 400

        release_tickets(order.id)

        order.status = OrderStatus.CANCELLED
        db.session.commit()

        return jsonify({
            'message': 'Order cancelled',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel order', 'details': str(e)}), 500


def register_orders_routes(app):
    app.add_url_rule('/api/orders', view_func=create_order, methods=['POST'])
    app.add_url_rule('/api/orders/<int:order_id>', view_func=get_order, methods=['GET'])
    app.add_url_rule('/api/orders/<int:order_id>/attendees', view_func=add_attendees, methods=['POST'])
    app.add_url_rule('/api/orders/<int:order_id>/pay', view_func=process_payment, methods=['POST'])
    app.add_url_rule('/api/orders/<int:order_id>/cancel', view_func=cancel_order, methods=['POST'])
