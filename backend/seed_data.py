"""
Kosh Ticketing - Seed Data
Populates the database with sample events and ticket tiers
"""

from datetime import datetime, timedelta
from app import db, create_app
from app.models import (
    User, Event, TicketTier, EventCategory, EventStatus, UserRole
)
from werkzeug.security import generate_password_hash

def seed_database():
    """Seed the database with sample data"""
    app = create_app()

    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("🌱 Seeding database...")

        # Create users
        admin = User(
            email="admin@gmail.com",
            password_hash=generate_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN
        )

        organizer = User(
            email="organizer@gmail.com",
            password_hash=generate_password_hash("organizer123"),
            first_name="Event",
            last_name="Organizer",
            role=UserRole.ORGANIZER
        )

        customer = User(
            email="customer@gmail.com",
            password_hash=generate_password_hash("customer123"),
            first_name="John",
            last_name="Doe",
            phone="+1-555-0123"
        )

        db.session.add_all([admin, organizer, customer])
        db.session.commit()

        # Sample events data
        events_data = [
            {
                "title": "Neon Nights Music Festival",
                "subtitle": "The biggest electronic music festival of the year",
                "description": "Experience three days of non-stop electronic music across five stages featuring world-renowned DJs and emerging artists. Immerse yourself in stunning visual productions, interactive art installations, and a vibrant community of music lovers.",
                "rich_description": "<h2>About the Festival</h2><p>Neon Nights brings together the best in electronic music for an unforgettable weekend. From house and techno to drum & bass and trance, our carefully curated lineup spans the full spectrum of electronic music.</p><h3>What's Included</h3><ul><li>Access to all 5 stages</li><li>Camping facilities</li><li>Food vendors from around the world</li><li>Art installations and workshops</li></ul>",
                "category": EventCategory.FESTIVAL,
                "start_date": datetime.utcnow() + timedelta(days=45),
                "end_date": datetime.utcnow() + timedelta(days=47),
                "doors_open": datetime.utcnow() + timedelta(days=45, hours=10),
                "venue_name": "Sunset Valley Grounds",
                "venue_address": "1234 Festival Way",
                "venue_city": "Austin",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=600",
                "organizer_name": "Neon Events LLC",
                "is_featured": True,
                "is_public": True,
                "age_restriction": "18+",
                "slug": "neon-nights-music-festival",
                "tags": ["electronic", "music", "festival", "edm", "outdoor"],
                "tiers": [
                    {"name": "Early Bird", "price": 149.00, "quantity_total": 500, "description": "Limited early bird pricing", "benefits": ["General Admission", "Festival Entry"]},
                    {"name": "General Admission", "price": 199.00, "quantity_total": 2000, "description": "Standard festival access", "benefits": ["General Admission", "Festival Entry", "Access to all stages"]},
                    {"name": "VIP Pass", "price": 349.00, "quantity_total": 300, "description": "Premium festival experience", "benefits": ["VIP Viewing Areas", "Express Entry", "VIP Bar Access", "Complimentary Drinks", "Backstage Tours"]},
                    {"name": "Backstage VIP", "price": 599.00, "quantity_total": 50, "description": "Ultimate backstage access", "benefits": ["All VIP Benefits", "Backstage Access", "Artist Meet & Greets", "Private Camping", "Gourmet Catering"]}
                ]
            },
            {
                "title": "Broadway in the Park: Hamilton",
                "subtitle": "The revolutionary musical comes to an outdoor amphitheater",
                "description": "Don't miss this once-in-a-lifetime opportunity to see Hamilton performed under the stars in our beautiful outdoor amphitheater. This special production brings the revolutionary story to life with a full orchestra and stunning set design.",
                "rich_description": "<h2>The Show</h2><p>Hamilton is the story of America's Founding Father Alexander Hamilton, an immigrant from the West Indies who became George Washington's right-hand man during the Revolutionary War and was the new nation's first Treasury Secretary.</p><h3>Cast & Crew</h3><p>Featuring a talented ensemble cast with choreography inspired by the original Broadway production.</p>",
                "category": EventCategory.THEATRE,
                "start_date": datetime.utcnow() + timedelta(days=14),
                "end_date": datetime.utcnow() + timedelta(days=14, hours=3),
                "doors_open": datetime.utcnow() + timedelta(days=14, hours=-1),
                "venue_name": "Central Park Amphitheater",
                "venue_address": "500 Park Avenue",
                "venue_city": "New York",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=600",
                "organizer_name": "Broadway Touring Co.",
                "is_featured": True,
                "is_public": True,
                "age_restriction": "All Ages",
                "slug": "broadway-hamilton-park",
                "tags": ["theatre", "broadway", "musical", "outdoor", "family"],
                "tiers": [
                    {"name": "Lawn Seating", "price": 45.00, "quantity_total": 800, "description": "Bring your own blanket or chair", "benefits": ["Lawn Access", "Bring your own seating"]},
                    {"name": "Reserved Seating", "price": 85.00, "quantity_total": 400, "description": "Comfortable reserved seats", "benefits": ["Reserved Seat", "Program Booklet"]},
                    {"name": "Premium Box", "price": 150.00, "quantity_total": 60, "description": "Private box with best views", "benefits": ["Private Box", "Best Views", "Complimentary Wine", "VIP Parking"]}
                ]
            },
            {
                "title": "The Weeknd: After Hours Tour",
                "subtitle": "The global superstar brings his chart-topping hits live",
                "description": "The Weeknd brings his critically acclaimed After Hours Tour to town for one unforgettable night. Experience his biggest hits live with state-of-the-art production, stunning visuals, and special guest performances.",
                "rich_description": "<h2>Tour Highlights</h2><p>The After Hours Tour features tracks from the Grammy-nominated album 'After Hours' plus all of The Weeknd's biggest hits including 'Blinding Lights', 'Starboy', 'Can't Feel My Face', and many more.</p><h3>Special Guests</h3><p>Featuring performances by top supporting artists. Full lineup to be announced.</p>",
                "category": EventCategory.CONCERT,
                "start_date": datetime.utcnow() + timedelta(days=30),
                "end_date": datetime.utcnow() + timedelta(days=30, hours=3),
                "doors_open": datetime.utcnow() + timedelta(days=30, hours=-1, minutes=30),
                "venue_name": "Madison Square Garden",
                "venue_address": "4 Pennsylvania Plaza",
                "venue_city": "New York",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600",
                "organizer_name": "Live Nation",
                "is_featured": True,
                "is_public": True,
                "age_restriction": "16+",
                "slug": "weeknd-after-hours-tour",
                "tags": ["concert", "pop", "r&b", "live music", "arena"],
                "tiers": [
                    {"name": "General Admission", "price": 89.00, "quantity_total": 3000, "description": "Standing floor access", "benefits": ["Floor Standing", "General Entry"]},
                    {"name": "Lower Bowl", "price": 129.00, "quantity_total": 4000, "description": "Great seats in the lower bowl", "benefits": ["Reserved Seat", "Lower Bowl Views"]},
                    {"name": "VIP Package", "price": 299.00, "quantity_total": 200, "description": "Premium experience with merchandise", "benefits": ["Premium Seat", "Exclusive Merch Bundle", "Early Entry", "VIP Lounge Access"]},
                    {"name": "Ultimate VIP", "price": 599.00, "quantity_total": 30, "description": "Meet & Greet experience", "benefits": ["Meet & Greet", "Photo Opportunity", "Signed Merchandise", "Premium Seating", "Pre-Show Soundcheck Access"]}
                ]
            },
            {
                "title": "NBA Finals: Game 3",
                "subtitle": "The championship series comes to your city",
                "description": "Witness history as the NBA Finals come to town for Game 3. Experience the intensity of championship basketball with the best players in the world competing for the ultimate prize.",
                "rich_description": "<h2>Game Day Experience</h2><p>Arrive early for pre-game festivities including live music, food trucks, and interactive basketball experiences. The arena will be buzzing with energy as two legendary teams battle for the championship.</p>",
                "category": EventCategory.SPORTS,
                "start_date": datetime.utcnow() + timedelta(days=21),
                "end_date": datetime.utcnow() + timedelta(days=21, hours=3),
                "doors_open": datetime.utcnow() + timedelta(days=21, hours=-2),
                "venue_name": "Staples Center",
                "venue_address": "1111 S Figueroa St",
                "venue_city": "Los Angeles",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1504450758481-7338eba7524a?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1504450758481-7338eba7524a?w=600",
                "organizer_name": "NBA Events",
                "is_featured": True,
                "is_public": True,
                "age_restriction": "All Ages",
                "slug": "nba-finals-game-3",
                "tags": ["sports", "basketball", "nba", "finals", "championship"],
                "tiers": [
                    {"name": "Upper Level", "price": 199.00, "quantity_total": 5000, "description": "Upper level seating", "benefits": ["Upper Level Seat"]},
                    {"name": "Club Level", "price": 399.00, "quantity_total": 1500, "description": "Premium club seating with amenities", "benefits": ["Club Level Seat", "Access to Club Lounge", "In-Seat Service"]},
                    {"name": "Courtside", "price": 2500.00, "quantity_total": 50, "description": "The best seats in the house", "benefits": ["Courtside Seat", "VIP Parking", "Private Entrance", "Championship Merch Package"]}
                ]
            },
            {
                "title": "Comedy Central Live",
                "subtitle": "An evening of stand-up comedy with top comedians",
                "description": "Laugh until you cry with an incredible lineup of Comedy Central's finest comedians. This special live recording features both established stars and rising talents in an intimate venue setting.",
                "rich_description": "<h2>The Lineup</h2><p>Featuring a rotating cast of Comedy Central's best comedians. Each show is unique with surprise guest appearances and unscripted moments you won't see on TV.</p><h3>Venue</h3><p>The Laugh Factory provides an intimate setting perfect for comedy, with great sightlines and acoustics from every seat.</p>",
                "category": EventCategory.COMEDY,
                "start_date": datetime.utcnow() + timedelta(days=10),
                "end_date": datetime.utcnow() + timedelta(days=10, hours=2, minutes=30),
                "doors_open": datetime.utcnow() + timedelta(days=10, hours=-1),
                "venue_name": "The Laugh Factory",
                "venue_address": "8001 Sunset Blvd",
                "venue_city": "Los Angeles",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=600",
                "organizer_name": "Comedy Central Live",
                "is_featured": False,
                "is_public": True,
                "age_restriction": "18+",
                "slug": "comedy-central-live",
                "tags": ["comedy", "stand-up", "live", "entertainment"],
                "tiers": [
                    {"name": "General Admission", "price": 35.00, "quantity_total": 200, "description": "General seating", "benefits": ["General Seating"]},
                    {"name": "Premium", "price": 55.00, "quantity_total": 50, "description": "Front section seating", "benefits": ["Front Section", "Priority Entry", "Show Poster"]}
                ]
            },
            {
                "title": "Modern Art Exhibition: Visions of Tomorrow",
                "subtitle": "A groundbreaking exhibition featuring 50+ contemporary artists",
                "description": "Explore the future of art at this massive exhibition showcasing works from over 50 contemporary artists from around the world. Featuring immersive installations, digital art, sculpture, and interactive pieces.",
                "rich_description": "<h2>About the Exhibition</h2><p>Visions of Tomorrow brings together artists exploring themes of technology, sustainability, identity, and the human experience in the 21st century. The exhibition spans three floors of the museum with works ranging from traditional mediums to cutting-edge digital installations.</p><h3>Featured Artists</h3><p>Works by internationally acclaimed artists alongside emerging talents from diverse backgrounds.</p>",
                "category": EventCategory.EXHIBITION,
                "start_date": datetime.utcnow() + timedelta(days=5),
                "end_date": datetime.utcnow() + timedelta(days=35),
                "doors_open": datetime.utcnow() + timedelta(days=5, hours=9),
                "venue_name": "Metropolitan Museum of Art",
                "venue_address": "1000 5th Ave",
                "venue_city": "New York",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5?w=600",
                "organizer_name": "Metropolitan Museum",
                "is_featured": False,
                "is_public": True,
                "age_restriction": "All Ages",
                "slug": "modern-art-exhibition",
                "tags": ["art", "exhibition", "museum", "contemporary", "culture"],
                "tiers": [
                    {"name": "General Admission", "price": 25.00, "quantity_total": 5000, "description": "Full day access", "benefits": ["Full Day Access", "Audio Guide"]},
                    {"name": "Member", "price": 0.00, "quantity_total": 2000, "description": "Free for museum members", "benefits": ["Member Access", "Priority Entry", "Exclusive Member Events"]},
                    {"name": "Guided Tour", "price": 45.00, "quantity_total": 200, "description": "Small group guided tour", "benefits": ["Guided Tour", "Expert Commentary", "Behind the Scenes Access", "Catalogue Book"]}
                ]
            },
            {
                "title": "Jazz Under the Stars",
                "subtitle": "An intimate evening of jazz at the botanical gardens",
                "description": "Enjoy an enchanting evening of live jazz music surrounded by the beauty of the botanical gardens. Bring a picnic, relax on the lawn, and let the smooth sounds of world-class jazz musicians wash over you.",
                "rich_description": "<h2>The Experience</h2><p>Jazz Under the Stars combines world-class music with the natural beauty of our botanical gardens. As the sun sets and the stars emerge, the garden transforms into an intimate concert venue unlike any other.</p><h3>What to Bring</h3><ul><li>Blanket or low-profile chair</li><li>Picnic (food and beverages allowed)</li><li>Warm layers for evening</li></ul>",
                "category": EventCategory.CONCERT,
                "start_date": datetime.utcnow() + timedelta(days=18),
                "end_date": datetime.utcnow() + timedelta(days=18, hours=3),
                "doors_open": datetime.utcnow() + timedelta(days=18, hours=-1),
                "venue_name": "Botanical Gardens",
                "venue_address": "2000 Botanical Way",
                "venue_city": "San Francisco",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=600",
                "organizer_name": "SF Jazz Society",
                "is_featured": False,
                "is_public": True,
                "age_restriction": "All Ages",
                "slug": "jazz-under-stars",
                "tags": ["jazz", "concert", "outdoor", "botanical", "music"],
                "tiers": [
                    {"name": "General Lawn", "price": 30.00, "quantity_total": 500, "description": "Lawn seating, bring your own chair", "benefits": ["Lawn Access", "BYO Seating"]},
                    {"name": "Reserved Seating", "price": 55.00, "quantity_total": 200, "description": "Reserved chair seating", "benefits": ["Reserved Chair", "Covered Area"]},
                    {"name": "VIP Garden", "price": 95.00, "quantity_total": 40, "description": "Private garden section with catering", "benefits": ["Private Garden Section", "Gourmet Catering", "Premium Wine Selection", "Meet the Artists"]}
                ]
            },
            {
                "title": "Tech Summit 2024",
                "subtitle": "The premier technology conference for innovators",
                "description": "Join 5,000+ tech professionals, entrepreneurs, and innovators at the Tech Summit 2024. Featuring keynote speeches from industry leaders, hands-on workshops, networking sessions, and a startup pitch competition.",
                "rich_description": "<h2>Conference Tracks</h2><ul><li>AI & Machine Learning</li><li>Web3 & Blockchain</li><li>Sustainability Tech</li><li>Health Tech</li><li>Future of Work</li></ul><h3>Networking</h3><p>Connect with fellow attendees through our AI-powered matchmaking system. Find collaborators, mentors, and investors.</p>",
                "category": EventCategory.WORKSHOP,
                "start_date": datetime.utcnow() + timedelta(days=60),
                "end_date": datetime.utcnow() + timedelta(days=62),
                "doors_open": datetime.utcnow() + timedelta(days=60, hours=7),
                "venue_name": "Moscone Center",
                "venue_address": "747 Howard St",
                "venue_city": "San Francisco",
                "venue_country": "USA",
                "banner_image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600",
                "organizer_name": "Tech Summit Inc.",
                "is_featured": True,
                "is_public": True,
                "age_restriction": "All Ages",
                "slug": "tech-summit-2024",
                "tags": ["technology", "conference", "networking", "innovation", "startup"],
                "tiers": [
                    {"name": "Student", "price": 99.00, "quantity_total": 500, "description": "Valid student ID required", "benefits": ["Full Conference Access", "Student Networking"]},
                    {"name": "General Admission", "price": 299.00, "quantity_total": 2000, "description": "Full conference access", "benefits": ["Full Conference Access", "Networking App", "Conference Materials"]},
                    {"name": "Pro Pass", "price": 599.00, "quantity_total": 300, "description": "Premium conference experience", "benefits": ["Priority Seating", "VIP Networking Events", "Workshop Access", "Recording Access", "Lunch Included"]},
                    {"name": "Executive", "price": 1299.00, "quantity_total": 50, "description": "Exclusive executive package", "benefits": ["All Pro Pass Benefits", "Private Executive Lounge", "1-on-1 Mentor Sessions", "Speaker Dinner Invitation", "Premium Hotel Accommodation"]}
                ]
            },
            {
                "title": "Sotet First Edition",
                "subtitle": "The inaugural Sotet festival with live entertainment",
                "description": "Experience the inaugural Sotet festival with live entertainment, cultural activations, and guided experience moments across the campsite. Featuring performances by Luckyboy Kenya, Elvis Hertz, and Reagan Travels.",
                "rich_description": "<h2>About Sotet</h2><p>The inaugural Sotet festival includes live entertainment, cultural activations, and guided experience moments across the campsite.</p><h3>What's Included</h3><ul><li>Artist Performances</li><li>Good Vibes</li><li>New Friends</li><li>Photography</li><li>Dance</li></ul><h3>Lineup</h3><ul><li>Luckyboy Kenya</li><li>Elvis Hertz</li><li>Reagan Travels</li></ul>",
                "category": EventCategory.FESTIVAL,
                "start_date": datetime(2026, 8, 8, 18, 0, 0),
                "end_date": datetime(2026, 8, 8, 23, 59, 59),
                "doors_open": datetime(2026, 8, 8, 17, 0, 0),
                "venue_name": "Tirinya Resort",
                "venue_address": "Tirinya Resort Grounds",
                "venue_city": "Tirinya",
                "venue_country": "Kenya",
                "banner_image": "https://images.unsplash.com/photo-1511379938547-c1f69b13d835?w=1200",
                "thumbnail_image": "https://images.unsplash.com/photo-1511379938547-c1f69b13d835?w=600",
                "organizer_name": "Sotet Events",
                "is_featured": True,
                "is_public": True,
                "age_restriction": "All Ages",
                "slug": "sotet-first-edition",
                "tags": ["festival", "music", "entertainment", "cultural", "outdoor"],
                "tiers": [
                    {"name": "Early Bird", "price": 850.00, "quantity_total": 100, "description": "Limited early bird pricing", "benefits": ["Festival Entry", "Limited Slots Available"]},
                    {"name": "General Entry", "price": 1000.00, "quantity_total": 300, "description": "Standard festival access", "benefits": ["Festival Entry", "Access to all performances"]},
                    {"name": "VIP Pass", "price": 1500.00, "quantity_total": 50, "description": "Premium festival experience", "benefits": ["VIP Viewing Areas", "Express Entry", "VIP Bar Access", "Exclusive Merchandise"]}
                ]
            }
        ]

        # Create events and ticket tiers
        for event_data in events_data:
            tiers_data = event_data.pop('tiers')

            event = Event(
                organizer_id=organizer.id,
                status=EventStatus.ON_SALE,
                published_at=datetime.utcnow(),
                **{k: v for k, v in event_data.items() if k not in ['tiers']}
            )
            db.session.add(event)
            db.session.flush()

            for tier_data in tiers_data:
                tier = TicketTier(
                    event_id=event.id,
                    **tier_data
                )
                db.session.add(tier)

        db.session.commit()

        print(f"✅ Seeded {len(events_data)} events with ticket tiers")
        print(f"✅ Created users: admin, organizer, customer")
        print("\n🔑 Login credentials:")
        print("   Admin: admin@gmail.com / admin123")
        print("   Organizer: organizer@gmail.com / organizer123")
        print("   Customer: customer@gmail.com / customer123")

if __name__ == '__main__':
    seed_database()
