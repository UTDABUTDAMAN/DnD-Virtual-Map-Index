from flask import Blueprint, render_template, request
from sqlalchemy import select, func
from project import db
from project.main.models import Location
from . import main_bp


@main_bp.route('/')
def index():
    stmt = select(Location)
    results = db.session.execute(stmt).scalars().all()
    print(results)
    for location in results:
        print(location.name, location.description, location.notes)
    
    return render_template('index.html')

@main_bp.route('/Wickermoor_Village_Map')
def Wickermoor_Village_Map():
    return render_template('Wickermoor_Village_Map.html')

@main_bp.route('/locations/<name>')
def get_location(name):
    clean_name = name.strip()
    stmt = select(Location).where(func.lower(Location.name) == func.lower(clean_name))
    location = db.session.execute(stmt).scalar_one_or_none()
    return render_template('partials/location_card.html', location=location, label=clean_name)

@main_bp.route('/locations/<name>/save', methods=['POST'])
def save_location(name):
    clean_name = name.strip()
    description = request.form.get('description', '').strip()
    notes = request.form.get('notes', '').strip()

    stmt = select(Location).where(func.lower(Location.name) == func.lower(clean_name))
    location = db.session.execute(stmt).scalar_one_or_none()

    if location:
        location.description = description
        location.notes = notes
    else:
        location = Location(name=clean_name, description=description, notes=notes)
        db.session.add(location)

    db.session.commit()
    return render_template('partials/location_card.html', location=location, label=clean_name)
