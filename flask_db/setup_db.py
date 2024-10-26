from app import create_app
from app.connectors.db import db, create_tables
from app.models.user import User
from app.models.review import Review
from werkzeug.security import generate_password_hash

def setup_database():
    app = create_app()
    
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create all tables
        db.create_all()
        print("Created all tables")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@admin.com',
            password=generate_password_hash('admin123'),
            role='Admin'
        )
        
        # Create test user
        test_user = User(
            username='test',
            email='test@test.com',
            password=generate_password_hash('test123'),
            role='User'
        )
        
        # Add users to database
        db.session.add(admin)
        db.session.add(test_user)
        db.session.commit()
        print("Created admin and test users")
        
        # Create some test reviews
        reviews = [
            Review(
                product_id=1,
                rating=5,
                description="Great product!",
                user_id=test_user.id
            ),
            Review(
                product_id=2,
                rating=4,
                description="Pretty good",
                user_id=test_user.id
            )
        ]
        
        # Add reviews to database
        for review in reviews:
            db.session.add(review)
        db.session.commit()
        print("Created test reviews")
        
        print("Database setup complete!")

if __name__ == "__main__":
    setup_database()