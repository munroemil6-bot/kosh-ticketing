"""
Kosh Ticketing - Application Factory
A modern event ticketing platform inspired by Madfun
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Initialize extensions without app (for factory pattern)
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()


def create_app(config_name=None):
    """Application factory pattern for creating Flask app instances."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///kosh_ticketing.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS configuration
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": cors_origins.split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Register routes directly on the app instance
    from app.routes.auth import register_auth_routes
    from app.routes.events import register_events_routes
    from app.routes.orders import register_orders_routes
    from app.routes.tickets import register_tickets_routes
    from app.routes.admin import register_admin_routes
    from app.routes.uploads import register_uploads_routes

    register_auth_routes(app)
    register_events_routes(app)
    register_orders_routes(app)
    register_tickets_routes(app)
    register_admin_routes(app)
    register_uploads_routes(app)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found", "status": 404}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error", "status": 500}, 500

    # Health check
    @app.route('/api/health')
    def health_check():
        return {"status": "healthy", "service": "kosh-ticketing-api"}

    # Create tables if they don't exist (for SQLite dev)
    with app.app_context():
        db.create_all()

    return app
