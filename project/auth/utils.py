from functools import wraps
from flask import session, redirect, url_for, request, abort


def is_authenticated():
    """Check if a user session is active and authenticated."""
    return bool(session.get('authenticated') and session.get('role'))


def get_current_role():
    """Return the current user's role ('gamemaster' or 'player'), or None."""
    if is_authenticated():
        return session.get('role')
    return None


def login_required(f):
    """
    Decorator to ensure user has authenticated as either Gamemaster or Player.
    Redirects to the login page if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to restrict route to specific roles (e.g. 'gamemaster').
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_authenticated():
                return redirect(url_for('auth.login', next=request.path))
            if session.get('role') not in allowed_roles:
                abort(403, description="You do not have permission to perform this action.")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
