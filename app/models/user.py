from app import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Personal Information
    student_number = db.Column(db.String(10), unique=True, nullable=True)
    id_number = db.Column(db.String(13), unique=True, nullable=True)
    full_names = db.Column(db.String(100), nullable=True)
    surname = db.Column(db.String(100), nullable=True)
    cell_number = db.Column(db.String(15), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    
    # Location & Academic
    home_address = db.Column(db.String(255), nullable=True)
    province = db.Column(db.String(50), nullable=True)
    campus = db.Column(db.String(50), nullable=True)
    faculty = db.Column(db.String(100), nullable=True)
    level_of_study = db.Column(db.String(50), nullable=True)
    qualification = db.Column(db.String(150), nullable=True)
    
    # Next of Kin
    nok_name = db.Column(db.String(100), nullable=True)
    nok_relationship = db.Column(db.String(50), nullable=True)
    nok_cell = db.Column(db.String(15), nullable=True)

    # --- PASSWORD RESET METHODS ---
    def get_reset_token(self):
        """Generates a secure, timed token for password resets."""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """Verifies the token and ensures it hasn't expired (default 30 mins)."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"