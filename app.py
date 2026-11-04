from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from sqlalchemy import select
from app.models import Location
from database import db_session


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"
db = SQLAlchemy(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

notes = {'location_id': 1,
           'notes': 'Something else that is not whatever'}

@app.route('/')
def index():
    stmt = select(Location)
    results = db.session.execute(stmt).scalars().all()
    print(results)
    for location in results:
        print(location.name, location.description, location.notes)
    
    return render_template('index.html')

@app.route('/Wickermoor_Village_Map')
def Wickermoor_Village_Map():
    return render_template('Wickermoor_Village_Map.html')

if __name__ == '__main__':
    from app.models import Location
    with app.app_context():
        db.create_all()
    app.run(debug=True)