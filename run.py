import os
import sys
import logging
from app import create_app, db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CRITICAL ERROR WRAPPER ---
# This tries to build the app. If it fails, it prints the exact
# error to your terminal so you don't just see "500 Internal Error"
try:
    logger.info("Creating Flask application...")
    app = create_app()
    logger.info("Flask application created successfully")
except Exception as e:
    logger.error(f"CRITICAL BOOT ERROR DETECTED: {e}")
    print("\n" + "="*50)
    print("CRITICAL BOOT ERROR DETECTED:")
    print(f"Details: {e}")
    print("="*50 + "\n")
    # This ensures the process exits so you can see the traceback
    sys.exit(1)

# --- DATABASE INITIALIZATION ---
# Only initialize database when running in production (with Gunicorn)
# or when explicitly running the script directly
is_production = 'gunicorn' in os.environ.get('_', '') or os.environ.get('RENDER') == 'true'
logger.info(f"Environment check - Production mode: {is_production}")

if __name__ == '__main__' or is_production:
    logger.info("Initializing database...")
    with app.app_context():
        try:
            # Import all models to ensure they're registered
            from app.models.user import User
            from app.models.housing import RoommatePreferences, HousingListing, RoomApplication, Allocation
            
            db.create_all()
            logger.info("Database tables created successfully")
            print("\n" + "*"*30)
            print("DATABASE SYNCED SUCCESSFULLY")
            print("*"*30 + "\n")
        except Exception as db_err:
            logger.error(f"Database Initialization Error: {db_err}")
            print(f"Database Initialization Error: {db_err}")
            # Don't exit on DB errors in production - let the app try to start
            if __name__ == '__main__':
                sys.exit(1)

if __name__ == '__main__':
    # We use '0.0.0.0' so you can test on local network devices
    # and 'debug=True' to enable the interactive debugger
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting development server on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        use_reloader=True  # Automatically restarts when you save files
    )