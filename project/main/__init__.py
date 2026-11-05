# project/main/__init__.py
from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='templates')

# Import routes at the bottom to avoid circular imports
from . import routes
