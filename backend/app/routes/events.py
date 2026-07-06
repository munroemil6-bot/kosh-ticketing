"""
Kosh Ticketing - Events Routes
Handles event listing, filtering, and details
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta
from app import db
from app.models import Event, EventCategory, EventStatus, TicketTier, User, UserRole
from app.schemas import EventSchema, EventFilterSchema, EventCreateSchema, TicketTierSchema
from app.utils import paginate, slugify

events_bp = Blueprint('events', __name__)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
filter_schema = EventFilterSchema()
create_schema = EventCreateSchema()

@events_bp.route('', methods=['GET'])
def get_events():
    """Get events with filtering, sorting, and pagination"""
    try:
        # Parse query parameters
        args = request.args.to_dict()

        # Handle boolean params
        if 'featured' in args:
            args['featured'] = args['featured'].lower() == 'true'

        # Build query
        query = Event.query.filter(Event.status.in_([EventStatus.PUBLISHED, EventStatus.ON_SALE, EventStatus.SOLD_OUT]))

        # Category filter
        if 'category' in args and args['category']:
            try:
                category = EventCategory(args['category'].lower())
                query = query.filter(Event.category == category)
            except ValueError:
                pass

        # City filter
        if 'city' in args and args['city']:
            query = query.filter(func.lower(Event.venue_city) == args['city'].lower())

        # Date range filter
        if 'date_from' in args and args['date_from']:
            try:
                date_from = datetime.fromisoformat(args['date_from'].replace('Z', '+00:00'))
                query = query.filter(Event.start_date >= date_from)
            except:
                pass

        if 'date_to' in args and args['date_to']:
            try:
                date_to = datetime.fromisoformat(args['date_to'].replace('Z', '+00:00'))
                query = query.filter(Event.start_date <= date_to)
            except:
                pass

        # Search filter (title, description, venue)
        if 'search' in args and args['search']:
            search_term = f"%{args['search']}%"
            query = query.filter(
                or_(
                    Event.title.ilike(search_term),
                    Event.description.ilike(search_term),
                    Event.venue_name.ilike(search_term),
                    Event.venue_city.ilike(search_term)
                )
            )

        # Featured filter
        if 'featured' in args and args['featured']:
            query = query.filter(Event.is_featured == True)

        # Status filter (for admin/organizer)
        if 'status' in args and args['status']:
            try:
                status = EventStatus(args['status'].lower())
                query = query.filter(Event.status == status)
            except ValueError:
                pass

        # Default: only show future or currently running events
        query = query.filter(Event.start_date >= datetime.utcnow() - timedelta(hours=24))

        # Sorting
        sort_by = args.get('sort_by', 'start_date')
        sort_order = args.get('sort_order', 'asc')

        if sort_by == 'start_date':
            query = query.order_by(Event.start_date.asc() if sort_order == 'asc' else Event.start_date.desc())
        elif sort_by == 'price':
            # Sort by lowest price (requires subquery)
            query = query.order_by(Event.start_date.asc())
        elif sort_by == 'popularity':
            query = query.order_by(Event.total_tickets_sold.desc())
        else:
            query = query.order_by(Event.start_date.asc())

        # Pagination
        page = int(args.get('page', 1))
        per_page = min(int(args.get('per_page', 12)), 50)

        result = paginate(query, page=page, per_page=per_page)

        return jsonify({
            'events': [event.to_dict(include_tiers=False) for event in result['items']],
            'pagination': {
                'total': result['total'],
                'pages': result['pages'],
                'page': result['page'],
                'per_page': result['per_page'],
                'has_next': result['has_next'],
                'has_prev': result['has_prev']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch events', 'details': str(e)}), 500


@events_bp.route('/featured', methods=['GET'])
def get_featured_events():
    """Get featured events for homepage"""
    try:
        events = Event.query.filter(
            Event.is_featured == True,
            Event.status.in_([EventStatus.PUBLISHED, EventStatus.ON_SALE]),
            Event.start_date >= datetime.utcnow() - timedelta(hours=24)
        ).order_by(Event.start_date.asc()).limit(6).all()

        return jsonify({
            'events': [event.to_dict(include_tiers=True) for event in events]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch featured events', 'details': str(e)}), 500


@events_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all event categories with counts"""
    try:
        categories = []
        for category in EventCategory:
            count = Event.query.filter(
                Event.category == category,
                Event.status.in_([EventStatus.PUBLISHED, EventStatus.ON_SALE]),
                Event.start_date >= datetime.utcnow() - timedelta(hours=24)
            ).count()

            categories.append({
                'id': category.value,
                'name': category.value.title(),
                'count': count
            })

        return jsonify({'categories': categories}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories', 'details': str(e)}), 500


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get single event with ticket tiers"""
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if event.status == EventStatus.DRAFT:
            return jsonify({'error': 'Event not available'}), 403

        return jsonify({'event': event.to_dict(include_tiers=True)}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch event', 'details': str(e)}), 500


@events_bp.route('', methods=['POST'])
@jwt_required()
def create_event():
    """Create a new event (organizer/admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            return jsonify({'error': 'Unauthorized - Organizer access required'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate
        errors = create_schema.validate(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Create event
        event = Event(
            title=data['title'],
            subtitle=data.get('subtitle'),
            description=data['description'],
            rich_description=data.get('rich_description'),
            category=EventCategory(data['category'].lower()),
            status=EventStatus.PUBLISHED,
            start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
            end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data.get('end_date') else None,
            doors_open=datetime.fromisoformat(data['doors_open'].replace('Z', '+00:00')) if data.get('doors_open') else None,
            venue_name=data['venue_name'],
            venue_address=data.get('venue_address'),
            venue_city=data.get('venue_city'),
            venue_country=data.get('venue_country'),
            banner_image=data.get('banner_image'),
            thumbnail_image=data.get('thumbnail_image'),
            gallery_images=data.get('gallery_images'),
            organizer_id=user.id,
            organizer_name=data.get('organizer_name', user.full_name),
            is_public=data.get('is_public', True),
            age_restriction=data.get('age_restriction'),
            slug=slugify(data['title']),
            tags=data.get('tags', []),
            published_at=datetime.utcnow()
        )

        db.session.add(event)
        db.session.flush()  # Get event.id

        # Create ticket tiers
        for tier_data in data['ticket_tiers']:
            tier = TicketTier(
                event_id=event.id,
                name=tier_data['name'],
                description=tier_data.get('description'),
                price=tier_data['price'],
                original_price=tier_data.get('original_price'),
                quantity_total=tier_data['quantity_total'],
                min_per_order=tier_data.get('min_per_order', 1),
                max_per_order=tier_data.get('max_per_order', 10),
                sale_start=datetime.fromisoformat(tier_data['sale_start'].replace('Z', '+00:00')) if tier_data.get('sale_start') else datetime.utcnow(),
                sale_end=datetime.fromisoformat(tier_data['sale_end'].replace('Z', '+00:00')) if tier_data.get('sale_end') else None,
                benefits=tier_data.get('benefits', [])
            )
            db.session.add(tier)

        db.session.commit()

        return jsonify({
            'message': 'Event created successfully',
            'event': event.to_dict(include_tiers=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create event', 'details': str(e)}), 500


@events_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    """Update an event (organizer/admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if not user or (user.role != UserRole.ADMIN and event.organizer_id != user_id):
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        # Update fields
        if 'title' in data:
            event.title = data['title']
            event.slug = slugify(data['title'])
        if 'description' in data:
            event.description = data['description']
        if 'status' in data:
            event.status = EventStatus(data['status'].lower())

        db.session.commit()

        return jsonify({
            'message': 'Event updated',
            'event': event.to_dict(include_tiers=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Update failed', 'details': str(e)}), 500


@events_bp.route('/<int:event_id>/related', methods=['GET'])
def get_related_events(event_id):
    """Get related events (same category or city)"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        related = Event.query.filter(
            Event.id != event_id,
            Event.status.in_([EventStatus.PUBLISHED, EventStatus.ON_SALE]),
            or_(
                Event.category == event.category,
                Event.venue_city == event.venue_city
            )
        ).order_by(Event.start_date.asc()).limit(4).all()

        return jsonify({
            'events': [e.to_dict(include_tiers=False) for e in related]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch related events', 'details': str(e)}), 500
