from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy import text
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_url = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL from .env: {db_url}")

if db_url is None:
    raise ValueError("DATABASE_URL environment variable is not set correctly.")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Connected to {app.config['SQLALCHEMY_DATABASE_URI']}")

assert 'postgresql' in db_url, "Not connected to PostgreSQL"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    print("Dropping all tables...")
    with db.engine.begin() as connection:
        connection.execute(text('DROP TABLE IF EXISTS "compliance_alert" CASCADE'))
        connection.execute(text('DROP TABLE IF EXISTS "document" CASCADE'))
        connection.execute(text('DROP TABLE IF EXISTS "vehicle" CASCADE'))
        connection.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
        connection.execute(text('DROP TABLE IF EXISTS "log" CASCADE'))
    
    print("Creating new tables...")
    db.create_all()

    print("Applying migrations...")
    upgrade()

    print("Database has been reset and tables created successfully!")