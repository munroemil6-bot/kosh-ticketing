"""
Kosh Ticketing - Admin Routes
Dashboard and management endpoints for organizers and admins
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db
from app.models import User, Event, Order, TicketTier, Attendee, UserRole, EventStatus, OrderStatus
from app.schemas import DashboardStatsSchema, EventSchema, OrderSchema
from app.utils import paginate

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get admin dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            return jsonify({'error': 'Unauthorized'}), 403

        # Base query for user's events
        events_query = Event.query
        if user.role == UserRole.ORGANIZER:
            events_query = events_query.filter_by(organizer_id=user_id)

        # Statistics
        total_events = events_query.count()

        # Get event IDs for this organizer
        event_ids = [e.id for e in events_query.all()]

        # Orders and revenue
        orders_query = Order.query.filter(
            Order.status == OrderStatus.PAID
        )
        if event_ids:
            orders_query = orders_query.join(OrderItem).join(TicketTier).filter(
                TicketTier.event_id.in_(event_ids)
            )

        total_orders = orders_query.count()
        total_revenue = db.session.query(func.sum(Order.total)).filter(
            Order.status == OrderStatus.PAID
        ).scalar() or 0

        total_tickets_sold = db.session.query(func.sum(OrderItem.quantity)).join(Order).filter(
            Order.status == OrderStatus.PAID
        ).scalar() or 0

        # Recent orders
        recent_orders = orders_query.order_by(Order.created_at.desc()).limit(5).all()

        # Events performance
        events_performance = []
        for event in events_query.order_by(Event.created_at.desc()).limit(10).all():
            events_performance.append({
                'id': event.id,
                'title': event.title,
                'tickets_sold': event.total_tickets_sold,
                'capacity': event.total_capacity,
                'revenue': sum(
                    float(item.total_price) for order in event.orders 
                    for item in order.items if order.status == OrderStatus.PAID
                ),
                'status': event.status.value
            })

        return jsonify({
            'stats': {
                'total_events': total_events,
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'total_tickets_sold': total_tickets_sold
            },
            'recent_orders': [order.to_dict() for order in recent_orders],
            'events_performance': events_performance
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard', 'details': str(e)}), 500


@admin_bp.route('/events', methods=['GET'])
@jwt_required()
def get_admin_events():
    """Get events for admin/organizer management"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            return jsonify({'error': 'Unauthorized'}), 403

        query = Event.query
        if user.role == UserRole.ORGANIZER:
            query = query.filter_by(organizer_id=user_id)

        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 50)

        result = paginate(query.order_by(Event.created_at.desc()), page=page, per_page=per_page)

        return jsonify({
            'events': [event.to_dict(include_tiers=True) for event in result['items']],
            'pagination': {
                'total': result['total'],
                'pages': result['pages'],
                'page': result['page'],
                'per_page': result['per_page']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch events', 'details': str(e)}), 500


@admin_bp.route('/events/<int:event_id>/stats', methods=['GET'])
@jwt_required()
def get_event_stats(event_id):
    """Get detailed statistics for a specific event"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if not user or (user.role != UserRole.ADMIN and event.organizer_id != user_id):
            return jsonify({'error': 'Unauthorized'}), 403

        # Tier breakdown
        tier_stats = []
        for tier in event.ticket_tiers:
            tier_stats.append({
                'id': tier.id,
                'name': tier.name,
                'price': float(tier.price),
                'total': tier.quantity_total,
                'sold': tier.quantity_sold,
                'available': tier.tickets_available,
                'revenue': float(tier.price) * tier.quantity_sold
            })

        # Sales over time (last 30 days)
        sales_data = []
        for i in range(30):
            date = datetime.utcnow() - timedelta(days=i)
            day_orders = Order.query.join(OrderItem).filter(
                OrderItem.ticket_tier_id.in_([t.id for t in event.ticket_tiers]),
                Order.status == OrderStatus.PAID,
                func.date(Order.created_at) == date.date()
            ).all()

            day_revenue = sum(
                float(item.total_price) for order in day_orders for item in order.items
            )
            day_tickets = sum(
                item.quantity for order in day_orders for item in order.items
            )

            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'revenue': day_revenue,
                'tickets': day_tickets
            })

        sales_data.reverse()

        return jsonify({
            'event': event.to_dict(include_tiers=False),
            'tier_stats': tier_stats,
            'sales_over_time': sales_data,
            'total_revenue': sum(t['revenue'] for t in tier_stats),
            'total_sold': sum(t['sold'] for t in tier_stats)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch event stats', 'details': str(e)}), 500


@admin_bp.route('/events/<int:event_id>/attendees', methods=['GET'])
@jwt_required()
def get_event_attendees(event_id):
    """Get attendee list for event check-in"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if not user or (user.role != UserRole.ADMIN and event.organizer_id != user_id):
            return jsonify({'error': 'Unauthorized'}), 403

        # Get all attendees for this event
        attendees = Attendee.query.join(TicketTier).filter(
            TicketTier.event_id == event_id
        ).order_by(Attendee.created_at.desc()).all()

        return jsonify({
            'attendees': [attendee.to_dict() for attendee in attendees],
            'total': len(attendees),
            'checked_in': sum(1 for a in attendees if a.is_checked_in)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch attendees', 'details': str(e)}), 500
