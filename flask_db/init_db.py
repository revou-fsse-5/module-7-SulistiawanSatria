from app import create_app, db
from app.models.user import User
from app.models.review import Review
# Import model lainnya jika ada

app = create_app()

def init_database():
    with app.app_context():
        # Membuat semua tabel
        db.create_all()
        print("Database initialized!")

if __name__ == "__main__":
    init_database()