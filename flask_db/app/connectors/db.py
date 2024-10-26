from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    try:
        DB_HOST = "localhost"      
        DB_USER = "root"            
        DB_PASSWORD = "satria"          
        DB_NAME = "flask_db"  
        
        DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

def create_tables(app):
    try:
        with app.app_context():
            # Import models here to ensure they're registered
            from ..models.user import User
            from ..models.review import Review
            
            # Create tables
            db.create_all()
            
            # Create admin user if not exists
            admin = User.query.filter_by(email='admin@admin.com').first()
            if not admin:
                from werkzeug.security import generate_password_hash
                admin = User(
                    username='admin',
                    email='admin@admin.com',
                    password=generate_password_hash('admin123'),
                    role='Admin'
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created!")
                
            print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")