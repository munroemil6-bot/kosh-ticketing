"""
Update Sotet First Edition event with correct date and venue
"""

from datetime import datetime
from app import db, create_app
from app.models import Event

def update_sotet_event():
    """Update Sotet First Edition event details"""
    app = create_app()

    with app.app_context():
        # Find the Sotet event
        event = Event.query.filter_by(title="Sotet First Edition").first()
        
        if event:
            # Update date to August 8, 2026
            event.start_date = datetime(2026, 8, 8, 18, 0, 0)  # 6 PM
            event.end_date = datetime(2026, 8, 8, 23, 59, 59)
            event.doors_open = datetime(2026, 8, 8, 17, 0, 0)  # 5 PM
            
            # Update venue to Tirinya Resort
            event.venue_name = "Tirinya Resort"
            event.venue_city = "Tirinya"
            event.venue_address = "Tirinya Resort Grounds"
            event.venue_country = "Kenya"
            
            event.updated_at = datetime.utcnow()
            
            db.session.commit()
            print("✅ Sotet First Edition event updated successfully!")
            print(f"   Date: August 8, 2026")
            print(f"   Venue: {event.venue_name}, {event.venue_city}")
        else:
            print("❌ Sotet First Edition event not found in database")
            print("   Available events:")
            events = Event.query.all()
            for e in events:
                print(f"   - {e.title}")

if __name__ == "__main__":
    update_sotet_event()
