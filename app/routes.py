from flask import Blueprint, render_template
from sqlalchemy import select
from app import db
from app.models import Location

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    stmt = select(Location)
    results = db.session.execute(stmt).scalars().all()
    for location in results:
        print(location.name, location.description, location.notes)
    
    return render_template('index.html')

@main_bp.route('/Wickermoor_Village_Map')
def Wickermoor_Village_Map():
    return render_template('Wickermoor_Village_Map.html')