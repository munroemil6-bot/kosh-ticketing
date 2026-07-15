"""
Kosh Ticketing - Tickets Routes
Handles user ticket viewing, downloading, and check-in
"""

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Order, Attendee, User, OrderStatus, UserRole
from app.schemas import AttendeeSchema
from app.utils import generate_qr_code

attendee_schema = AttendeeSchema()
attendees_schema = AttendeeSchema(many=True)


@jwt_required()
def get_my_tickets():
    """Get all tickets for logged-in user"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.role != UserRole.CUSTOMER:
            return jsonify({'error': 'Only customer accounts can view tickets'}), 403

        orders = Order.query.filter_by(
            user_id=user_id,
            status=OrderStatus.PAID
        ).all()

        tickets = []
        for order in orders:
            for attendee in order.attendees:
                tickets.append(attendee.to_dict())

        return jsonify({
            'tickets': tickets,
            'total': len(tickets)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch tickets', 'details': str(e)}), 500


@jwt_required()
def get_ticket(ticket_id):
    """Get single ticket details"""
    try:
        user_id = int(get_jwt_identity())
        attendee = Attendee.query.get(ticket_id)

        if not attendee:
            return jsonify({'error': 'Ticket not found'}), 404

        if attendee.order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        if attendee.order.user and attendee.order.user.role != UserRole.CUSTOMER:
            return jsonify({'error': 'Only customer accounts can view tickets'}), 403

        return jsonify({
            'ticket': attendee.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch ticket', 'details': str(e)}), 500


@jwt_required()
def get_ticket_qr(ticket_id):
    """Get QR code for ticket"""
    try:
        user_id = int(get_jwt_identity())
        attendee = Attendee.query.get(ticket_id)

        if not attendee:
            return jsonify({'error': 'Ticket not found'}), 404

        if attendee.order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        if attendee.order.user and attendee.order.user.role != UserRole.CUSTOMER:
            return jsonify({'error': 'Only customer accounts can view tickets'}), 403

        qr_data = f"KOSH:{attendee.ticket_number}:{attendee.order.order_number}"
        qr_code = generate_qr_code(qr_data, size=15, border=3)

        return jsonify({
            'ticket_number': attendee.ticket_number,
            'qr_code': qr_code
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to generate QR', 'details': str(e)}), 500


def get_guest_tickets(order_number):
    """Get tickets by order number (for guest checkout)"""
    try:
        order = Order.query.filter_by(order_number=order_number).first()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if order.status != OrderStatus.PAID:
            return jsonify({'error': 'Order not paid'}), 400

        tickets = [attendee.to_dict() for attendee in order.attendees]

        return jsonify({
            'order_number': order_number,
            'tickets': tickets
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch tickets', 'details': str(e)}), 500


def register_tickets_routes(app):
    app.add_url_rule('/api/tickets/my-tickets', view_func=get_my_tickets, methods=['GET'])
    app.add_url_rule('/api/tickets/<int:ticket_id>', view_func=get_ticket, methods=['GET'])
    app.add_url_rule('/api/tickets/<int:ticket_id>/qr', view_func=get_ticket_qr, methods=['GET'])
    app.add_url_rule('/api/tickets/guest/<string:order_number>', view_func=get_guest_tickets, methods=['GET'])
