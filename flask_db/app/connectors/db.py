from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    DB_HOST = "localhost"      
    DB_USER = "root"            
    DB_PASSWORD = "satria"          
    DB_NAME = "flask_db"  
    
    DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

def create_tables(app):
    with app.app_context():
        db.create_all()
        print("All tables created successfully!")

def drop_tables(app):
    with app.app_context():
        db.drop_all()
        print("All tables dropped successfully!")