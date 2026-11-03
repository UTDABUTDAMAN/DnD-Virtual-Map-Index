import sqlite3

import jsonify

from flask import Flask, render_template, request
from db import close_db, get_db

app = Flask(__name__)

notes = {'location_id': 1,
           'notes': 'Something else that is not whatever'}

@app.route('/')
def index():
    db = get_db()
    # Execute raw SQL directly
    user = db.execute('SELECT * FROM user').fetchall()
    print(len(user))
    return render_template('index.html')

@app.route('/Wickermoor_Village_Map')
def Wickermoor_Village_Map():
    return render_template('Wickermoor_Village_Map.html')

# Add notes
@app.route('/notes', methods=['POST'])
def add_notes():
    new_note = request.json
    location = new_note['location_id']
    updated_notes = new_note['notes']
    notes['location_id'] = updated_notes



    with sqlite3.connect("local.db") as users:
            cursor = users.cursor()
            cursor.execute("UPDATE locations SET notes_ = ? WHERE id = ?;",
                           (notes['location_id'],location))
            users.commit()

    print("Hey, it worked!!!")
    return jsonify(new_note), 201

# Register teardown function to close connections when requests finish
app.teardown_appcontext(close_db)


if __name__ == '__main__':
    # Optional CLI command to initialize database tables manually

    from db import init_db
    # with app.app_context():
    #     init_db()
    #     print('Initialized the database.')


# 1. Connect to the database file (creates it if it doesn't exist)
    conn = sqlite3.connect("local.db")

    try:
        # 2. Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        
        # 3. Execute the SELECT query
        # cursor.execute( """ INSERT INTO locations (name_, description_, notes_) VALUES (?, ?, ?) """, ('big Mike fat shack', 'home of big Mike, has a deep fear of abandonment', 'secretly is super gay'), )
        # conn.commit()
        cursor.execute("SELECT * FROM locations")
        
        
        # 4. Fetch the data (returns a list of tuples)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        # 5. Always close the connection when done
        conn.close()


    app.run(debug=True)