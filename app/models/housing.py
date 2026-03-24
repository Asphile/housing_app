from app import db
from datetime import datetime

class RoommatePreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cleanliness_level = db.Column(db.String(50))
    noise_tolerance = db.Column(db.String(50))
    sleep_schedule = db.Column(db.String(50))
    study_habits = db.Column(db.String(50))

class HousingListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)      
    region = db.Column(db.String(100), nullable=False)    
    gender_type = db.Column(db.String(50), nullable=False) 
    address = db.Column(db.String(200), nullable=False)   
    capacity = db.Column(db.Integer, nullable=False)     
    available_rooms = db.Column(db.Integer, default=0)    
    image_file = db.Column(db.String(100), default='default_res.jpg') 
    description = db.Column(db.Text)
    
    # Relationships
    apps = db.relationship('RoomApplication', backref='residence', lazy=True)
    allocations = db.relationship('Allocation', backref='listing', lazy=True)

class RoomApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('housing_listing.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending') 
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

class Allocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('housing_listing.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False) 
    status = db.Column(db.String(20), default='Pending') 
    allocated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Use 'student' instead of 'user' to avoid naming conflicts with the 'user' table
    student = db.relationship('User', backref='assigned_allocation', lazy=True)