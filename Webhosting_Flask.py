import sqlite3


from flask import Flask, render_template
from db import close_db, get_db

app = Flask(__name__)


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