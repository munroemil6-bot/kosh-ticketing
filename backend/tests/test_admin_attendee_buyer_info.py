import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime

from app import create_app, db
from app.models import (
    User,
    UserRole,
    Event,
    EventCategory,
    EventStatus,
    TicketTier,
    Order,
    OrderItem,
    Attendee,
    OrderStatus,
)
from flask_jwt_extended import create_access_token


def test_admin_dashboard_loads_for_organizer_with_paid_orders():
    app = create_app('testing')
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        organizer = User(
            email='dashboard@example.com',
            password_hash='hash',
            first_name='Dash',
            last_name='User',
            role=UserRole.ORGANIZER,
        )
        db.session.add(organizer)
        db.session.commit()

        event = Event(
            title='Dashboard Launch',
            description='Dashboard test event',
            category=EventCategory.CONCERT,
            status=EventStatus.ON_SALE,
            start_date=datetime.utcnow(),
            venue_name='Main Hall',
            organizer_id=organizer.id,
            organizer_name=organizer.full_name,
        )
        db.session.add(event)
        db.session.commit()

        tier = TicketTier(
            event_id=event.id,
            name='General Admission',
            price=60,
            quantity_total=20,
        )
        db.session.add(tier)
        db.session.commit()

        order = Order(
            order_number='DASH-ORDER-1',
            user_id=organizer.id,
            status=OrderStatus.PAID,
            subtotal=60,
            fees=0,
            tax=0,
            discount=0,
            total=60,
            currency='USD',
        )
        db.session.add(order)
        db.session.commit()

        db.session.add(OrderItem(order_id=order.id, ticket_tier_id=tier.id, quantity=1, unit_price=60, total_price=60))
        db.session.commit()

        token = create_access_token(identity=str(organizer.id))

        client = app.test_client()
        response = client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        payload = response.get_json()
        assert payload['stats']['total_events'] == 1
        assert payload['stats']['total_orders'] == 1
        assert payload['events_performance'][0]['title'] == event.title


def test_admin_attendee_endpoint_includes_buyer_identity():
    app = create_app('testing')
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        organizer = User(
            email='organizer@example.com',
            password_hash='hash',
            first_name='Org',
            last_name='Admin',
            role=UserRole.ORGANIZER,
        )
        customer = User(
            email='customer@example.com',
            password_hash='hash',
            first_name='Cust',
            last_name='User',
            role=UserRole.CUSTOMER,
        )
        db.session.add_all([organizer, customer])
        db.session.commit()

        event = Event(
            title='Launch Night',
            description='A test event',
            category=EventCategory.CONCERT,
            status=EventStatus.ON_SALE,
            start_date=datetime.utcnow(),
            venue_name='Main Hall',
            organizer_id=organizer.id,
            organizer_name=organizer.full_name,
        )
        db.session.add(event)
        db.session.commit()

        tier = TicketTier(
            event_id=event.id,
            name='General Admission',
            price=50,
            quantity_total=100,
        )
        db.session.add(tier)
        db.session.commit()

        order = Order(
            order_number='TEST-ORDER-1',
            user_id=customer.id,
            status=OrderStatus.PAID,
            subtotal=50,
            fees=0,
            tax=0,
            discount=0,
            total=50,
            currency='USD',
        )
        db.session.add(order)
        db.session.commit()

        db.session.add(OrderItem(order_id=order.id, ticket_tier_id=tier.id, quantity=1, unit_price=50, total_price=50))
        attendee = Attendee(
            order_id=order.id,
            ticket_tier_id=tier.id,
            first_name='Test',
            last_name='Buyer',
            email='ticket@example.com',
            ticket_number='TICKET-001',
            qr_code='qr',
        )
        db.session.add(attendee)
        db.session.commit()

        token = create_access_token(identity=str(organizer.id))

        client = app.test_client()
        response = client.get(
            f'/api/admin/events/{event.id}/attendees',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        payload = response.get_json()
        assert payload['attendees'][0]['buyer_email'] == customer.email
        assert payload['attendees'][0]['buyer_name'] == customer.full_name
