import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
from models import db, Club, Booking

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def index():
    clubs = Club.query.all()
    return render_template('index.html', clubs=clubs)

@app.route('/club/<int:club_id>')
def club_details(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('club_details.html', club=club)

@app.route('/book', methods=['POST'])
def book_session():
    data = request.json
    club_id = data.get('club_id')
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')

    if not all([club_id, name, email, date]):
        return jsonify({"error": "Missing required fields"}), 400

    club = Club.query.get(club_id)
    if not club:
        return jsonify({"error": "Club not found"}), 404

    booking = Booking(club_id=club_id, name=name, email=email, date=date)
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking successful"}), 201

def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

def seed_db():
    with app.app_context():
        clubs = [
            Club(name="BJJ Masters", location="123 Main St", description="Expert instruction in Brazilian Jiu-Jitsu"),
            Club(name="Grappling Grounds", location="456 Oak Ave", description="Open mat sessions for all skill levels"),
            Club(name="Submission Central", location="789 Pine Rd", description="Focus on submission techniques"),
        ]
        db.session.add_all(clubs)
        db.session.commit()
        print("Database seeded with sample clubs.")

if __name__ == '__main__':
    init_db()
    seed_db()
    app.run(host='0.0.0.0', port=5000)
