import os

class Config:
    # ... other settings ...
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads/profile_pics')