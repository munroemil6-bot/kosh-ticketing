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
    OrderStatus,
)
from flask_jwt_extended import create_access_token


def test_organizer_cannot_create_purchase_order():
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
        db.session.add(organizer)
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

        token = create_access_token(identity=str(organizer.id))

        client = app.test_client()
        response = client.post(
            '/api/orders',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'event_id': event.id,
                'tickets': [{'ticket_tier_id': tier.id, 'quantity': 1}],
            },
        )

        assert response.status_code == 403


def test_organizer_can_cancel_their_event():
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
        db.session.add(organizer)
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

        token = create_access_token(identity=str(organizer.id))

        client = app.test_client()
        response = client.delete(
            f'/api/admin/events/{event.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        payload = response.get_json()
        assert payload['event']['status'] == EventStatus.CANCELLED.value
