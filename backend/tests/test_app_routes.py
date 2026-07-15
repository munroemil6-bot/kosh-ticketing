import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app


def test_auth_and_admin_routes_are_registered():
    app = create_app('testing')
    client = app.test_client()

    assert any(rule.rule == '/api/auth/login' for rule in app.url_map.iter_rules())
    assert any(rule.rule == '/api/admin/dashboard' for rule in app.url_map.iter_rules())

    response = client.post('/api/auth/login', json={})
    assert response.status_code == 400


def test_login_returns_plain_role_string():
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        from app import db
        from app.models import User, UserRole
        from werkzeug.security import generate_password_hash

        user = User(
            email='customer-role-example@example.com',
            password_hash=generate_password_hash('password123'),
            first_name='Customer',
            last_name='User',
            role=UserRole.CUSTOMER,
        )
        db.session.add(user)
        db.session.commit()

    response = client.post('/api/auth/login', json={
        'email': 'customer-role-example@example.com',
        'password': 'password123',
    })

    assert response.status_code == 200
    assert response.get_json()['user']['role'] == 'customer'
