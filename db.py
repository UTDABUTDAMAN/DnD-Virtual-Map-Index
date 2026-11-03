import sqlite3
import os
from flask import g, current_app

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'local.db')

def get_db():
    # Store connection in Flask's application context 'g'
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Returns rows as dictionary-like objects instead of tuples
        g.db.row_factory = sqlite3.Row 
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # Create tables from an external schema file if needed
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))