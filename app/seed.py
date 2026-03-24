# seed.py
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(email='studenthousing@dut4life.ac.za').first()
    if not admin:
        hashed_pw = generate_password_hash('admin123') # Change this!
        new_admin = User(
            username='Admin',
            email='studenthousing@dut4life.ac.za',
            password=hashed_pw
        )
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin already exists.")