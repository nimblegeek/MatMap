import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
from models import db, Club, Booking, OpenMatSession
from sqlalchemy import func

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def index():
    clubs = Club.query.options(db.joinedload(Club.open_mat_sessions)).all()
    for club in clubs:
        club.open_mat_sessions.sort(key=lambda x: x.date)
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

@app.route('/remove_duplicates', methods=['POST'])
def remove_duplicates():
    with db.session.begin():
        # Get all club names
        club_names = db.session.query(Club.name).distinct().all()
        
        for name in club_names:
            # Keep the first entry for each name and delete the rest
            clubs = Club.query.filter_by(name=name[0]).all()
            for club in clubs[1:]:
                db.session.delete(club)
    
    return jsonify({"message": "Duplicate entries removed"}), 200

def is_valid_organization_number(org_number):
    # Check if the organization number is 9 digits
    if not re.match(r'^\d{9}$', org_number):
        return False
    
    # Calculate the checksum
    weights = [3, 2, 7, 6, 5, 4, 3, 2]
    checksum = sum(int(digit) * weight for digit, weight in zip(org_number[:-1], weights))
    remainder = checksum % 11
    check_digit = (11 - remainder) % 11
    
    return int(org_number[-1]) == check_digit

@app.route('/add_club', methods=['GET', 'POST'])
def add_club():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']
        organization_number = request.form['organization_number']

        if not is_valid_organization_number(organization_number):
            return render_template('add_club.html', error="Invalid organization number")

        existing_club = Club.query.filter_by(organization_number=organization_number).first()
        if existing_club:
            return render_template('add_club.html', error="Organization number already exists")

        new_club = Club(name=name, location=location, description=description, organization_number=organization_number)
        db.session.add(new_club)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_club.html')

def init_db():
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create all tables
        print("Database tables dropped and recreated.")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
