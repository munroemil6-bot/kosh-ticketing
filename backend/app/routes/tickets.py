"""
Kosh Ticketing - Tickets Routes
Handles user ticket viewing, downloading, and check-in
"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from io import BytesIO
from app import db
from app.models import Order, Attendee, User, OrderStatus
from app.schemas import AttendeeSchema
from app.utils import generate_qr_code

tickets_bp = Blueprint('tickets', __name__)
attendee_schema = AttendeeSchema()
attendees_schema = AttendeeSchema(many=True)

@tickets_bp.route('/my-tickets', methods=['GET'])
@jwt_required()
def get_my_tickets():
    """Get all tickets for logged-in user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get all paid orders for user
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


@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    """Get single ticket details"""
    try:
        user_id = get_jwt_identity()
        attendee = Attendee.query.get(ticket_id)

        if not attendee:
            return jsonify({'error': 'Ticket not found'}), 404

        # Verify ownership
        if attendee.order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify({
            'ticket': attendee.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch ticket', 'details': str(e)}), 500


@tickets_bp.route('/<int:ticket_id>/qr', methods=['GET'])
@jwt_required()
def get_ticket_qr(ticket_id):
    """Get QR code for ticket"""
    try:
        user_id = get_jwt_identity()
        attendee = Attendee.query.get(ticket_id)

        if not attendee:
            return jsonify({'error': 'Ticket not found'}), 404

        if attendee.order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Regenerate QR code
        qr_data = f"KOSH:{attendee.ticket_number}:{attendee.order.order_number}"
        qr_code = generate_qr_code(qr_data, size=15, border=3)

        return jsonify({
            'ticket_number': attendee.ticket_number,
            'qr_code': qr_code
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to generate QR', 'details': str(e)}), 500


@tickets_bp.route('/guest/<string:order_number>', methods=['GET'])
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
