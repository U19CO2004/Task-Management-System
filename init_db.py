from app import db, create_app

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created.")
from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Check if the user already exists
    if not User.query.filter_by(email='musa@gmail.com').first():
        # Create a new user
        user = User(
            username='Musa',
            email='musa@gmail.com',
            password=generate_password_hash('yourpassword'),  # change 'yourpassword' to what you want
            role='Employee'  # or 'Admin', 'Manager'
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Test user created.")
    else:
        print("⚠️ User already exists.")
