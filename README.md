# DnD-Virtual-Map-Index
Way to present and store information for any map (places of interest, NPCs, story threads, etc.) using interactive PDF rendering, SQLite database persistence, and role-based access control.

---

## Features

- **Interactive Map Viewer**: Renders high-resolution PDF maps using PDF.js with clickable interactive text markers (e.g. `V1`, `V2`, etc.).
- **Location Database**: Displays and edits location lore, descriptions, and notes stored in SQLite with SQLAlchemy and Flask-Migrate.
- **Dual-Role Authentication Flow**:
  - 🛡️ **Game Master**: Full access to inspect markers, edit public lore, and manage confidential **DM Notes / Secrets**.
  - ⚔️ **Player**: Explore the village, inspect markers, and edit public names and descriptions. DM Notes are completely hidden from players and protected against overwriting.
- **Protected PDF Serving**: Raw map PDFs are served exclusively to authenticated sessions through protected Flask endpoints, preventing unauthenticated static file leaks.
- **Werkzeug Security**: Password hashes stored securely in `.env` using Werkzeug cryptographic hashing (`check_password_hash`).

---

## Quick Start

### 1. Prerequisites & Virtual Environment
Ensure Python 3.12+ is installed and activate your virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)
Copy the example environment configuration:
```bash
cp .env.example .env
```

Your `.env` file contains:
- `SECRET_KEY`: Cryptographic signing key for Flask session cookies.
- `GM_PASSWORD_HASH`: Werkzeug password hash for the Game Master role.
- `PLAYER_PASSWORD_HASH`: Werkzeug password hash for the Player role.

### 3. Run the Application
```bash
python app.py
```
Visit **`http://127.0.0.1:5000/`** in your browser. Unauthenticated visitors are automatically directed to the role selection login page.

---

## Helper Scripts

### Generate Password Hashes (`scripts/hash_password.py`)
Generate secure Werkzeug password hashes to store in `.env`:
```bash
python scripts/hash_password.py
# Or pass arguments directly:
python scripts/hash_password.py gamemaster <your_password>
python scripts/hash_password.py player <your_password>
```

### Generate Secret Key (`scripts/gen_secret_key.py`)
Generate a strong 256-bit cryptographic `SECRET_KEY` for Flask session signing:
```bash
python scripts/gen_secret_key.py
```

---

## Project Structure

```
DnD-Virtual-Map-Index/
├── app.py                      # Application entry point
├── project/
│   ├── __init__.py             # Flask application factory & .env loader
│   ├── auth/                   # Authentication blueprint
│   │   ├── routes.py           # /login and /logout endpoints
│   │   ├── utils.py            # @login_required & @role_required decorators
│   │   └── templates/auth/     # Dark fantasy role selection & login page
│   ├── documents/              # Protected documents (Wickermoor PDF map)
│   ├── main/                   # Core application blueprint
│   │   ├── models.py           # SQLAlchemy Location model
│   │   ├── routes.py           # Map viewer & location card CRUD endpoints
│   │   └── templates/          # Wickermoor interactive viewer & partials
│   └── static/                 # Public web assets (CSS, icons)
├── scripts/
│   ├── gen_secret_key.py       # Flask SECRET_KEY generator
│   └── hash_password.py        # Werkzeug password hash generator
├── .env.example                # Example environment variables
└── requirements.txt            # Python dependencies
```
