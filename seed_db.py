from main import app, db
from models import Club

def seed_db():
    with app.app_context():
        # Check if there are any existing clubs
        if Club.query.count() == 0:
            clubs = [
                Club(name="BJJ Masters", location="123 Main St", description="Expert instruction in Brazilian Jiu-Jitsu"),
                Club(name="Grappling Grounds", location="456 Oak Ave", description="Open mat sessions for all skill levels"),
                Club(name="Submission Central", location="789 Pine Rd", description="Focus on submission techniques"),
            ]
            for club in clubs:
                existing_club = Club.query.filter_by(name=club.name).first()
                if not existing_club:
                    db.session.add(club)
            db.session.commit()
            print("Database seeded with sample clubs.")
        else:
            print("Database already contains clubs. Skipping seeding.")

if __name__ == '__main__':
    seed_db()
