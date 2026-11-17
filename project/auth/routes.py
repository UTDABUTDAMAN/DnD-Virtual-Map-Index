import os
from urllib.parse import urlparse, urljoin
from flask import render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import check_password_hash
from . import auth_bp
from .utils import is_authenticated


def is_safe_url(target):
    """Ensure redirect URL points to the same host."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and is_authenticated():
        return redirect(url_for('main.Wickermoor_Village_Map'))

    selected_role = request.args.get('role', 'player').lower()
    if selected_role not in ('gamemaster', 'player'):
        selected_role = 'player'

    if request.method == 'POST':
        role = request.form.get('role', '').strip().lower()
        password = request.form.get('password', '')
        next_page = request.form.get('next') or request.args.get('next')

        if role not in ('gamemaster', 'player'):
            flash('Invalid role selected.', 'error')
            return render_template('auth/login.html', selected_role='player')

        selected_role = role

        # Retrieve stored password hash for the role
        if role == 'gamemaster':
            stored_hash = current_app.config.get('GM_PASSWORD_HASH') or os.environ.get('GM_PASSWORD_HASH')
            display_name = 'Game Master'
        else:
            stored_hash = current_app.config.get('PLAYER_PASSWORD_HASH') or os.environ.get('PLAYER_PASSWORD_HASH')
            display_name = 'Player'

        if not stored_hash:
            flash(f'Password hash for {display_name} is not configured in .env.', 'error')
            return render_template('auth/login.html', selected_role=selected_role)

        if check_password_hash(stored_hash, password):
            session.clear()
            session['role'] = role
            session['authenticated'] = True
            flash(f'Welcome, {display_name}!', 'success')

            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('main.Wickermoor_Village_Map'))
        else:
            flash(f'Incorrect password for {display_name}. Please try again.', 'error')

    return render_template('auth/login.html', selected_role=selected_role)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
