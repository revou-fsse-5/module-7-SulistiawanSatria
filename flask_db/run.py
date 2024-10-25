from app import create_app
from app.connectors.db import create_tables

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        create_tables(app)
    app.run(debug=True)