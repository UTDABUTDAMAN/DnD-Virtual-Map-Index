import os
from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, current_app
from sqlalchemy import select, func, or_
from project import db
from project.main.models import Location
from project.auth.utils import login_required
from . import main_bp


def parse_marker_id(name):
    """If name represents a marker like 'V1', 'v24', extract the integer id."""
    clean = name.strip()
    if clean.upper().startswith('V') and clean[1:].isdigit():
        return int(clean[1:])
    return None


@main_bp.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.Wickermoor_Village_Map'))


@main_bp.route('/Wickermoor_Village_Map')
@login_required
def Wickermoor_Village_Map():
    return render_template('Wickermoor_Village_Map.html')


@main_bp.route('/documents/Wickermoor_Village_Map.pdf')
@login_required
def get_wickermoor_pdf():
    docs_dir = os.path.join(current_app.root_path, 'documents')
    return send_from_directory(docs_dir, 'Wickermoor_Village_Map.pdf')


@main_bp.route('/locations/<name>')
@login_required
def get_location(name):
    clean_name = name.strip()
    marker_id = parse_marker_id(clean_name)

    if marker_id is not None:
        stmt = select(Location).where(
            or_(
                func.lower(Location.name) == func.lower(clean_name),
                Location.location_id == marker_id
            )
        )
    else:
        stmt = select(Location).where(func.lower(Location.name) == func.lower(clean_name))

    location = db.session.execute(stmt).scalar_one_or_none()
    return render_template('partials/location_card.html', location=location, label=clean_name)


@main_bp.route('/locations/<name>/save', methods=['POST'])
@login_required
def save_location(name):
    clean_name = name.strip()
    new_name = request.form.get('name', '').strip() or clean_name
    description = request.form.get('description', '').strip()
    role = session.get('role')
    marker_id = parse_marker_id(clean_name)

    # Locate existing location by marker_id or by clean_name
    if marker_id is not None:
        stmt = select(Location).where(
            or_(
                func.lower(Location.name) == func.lower(clean_name),
                Location.location_id == marker_id
            )
        )
    else:
        stmt = select(Location).where(func.lower(Location.name) == func.lower(clean_name))

    location = db.session.execute(stmt).scalar_one_or_none()

    if location:
        location.name = new_name
        location.description = description
        # Only Gamemasters can update notes. Players preserve existing notes untouched.
        if role == 'gamemaster' and 'notes' in request.form:
            location.notes = request.form.get('notes', '').strip()
    else:
        # Determine unique location_id for new records
        if marker_id is not None:
            assigned_id = marker_id
        else:
            max_id_stmt = select(func.max(Location.location_id))
            max_id = db.session.execute(max_id_stmt).scalar() or 0
            assigned_id = max_id + 1

        notes = request.form.get('notes', '').strip() if role == 'gamemaster' else None

        location = Location(
            location_id=assigned_id,
            name=new_name,
            description=description,
            notes=notes
        )
        db.session.add(location)

    db.session.commit()
    return render_template('partials/location_card.html', location=location, label=clean_name)
