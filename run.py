import os
import sys
from app import create_app, db

# --- CRITICAL ERROR WRAPPER ---
# This tries to build the app. If it fails, it prints the exact 
# error to your terminal so you don't just see "500 Internal Error"
try:
    app = create_app()
except Exception as e:
    print("\n" + "="*50)
    print("CRITICAL BOOT ERROR DETECTED:")
    print(f"Details: {e}")
    print("="*50 + "\n")
    # This ensures the process exits so you can see the traceback
    sys.exit(1)

# --- DATABASE INITIALIZATION ---
# Only initialize database when running in production (with Gunicorn)
# or when explicitly running the script directly
if __name__ == '__main__' or 'gunicorn' in os.environ.get('_', ''):
    with app.app_context():
        try:
            db.create_all()
            print("\n" + "*"*30)
            print("DATABASE SYNCED SUCCESSFULLY")
            print("*"*30 + "\n")
        except Exception as db_err:
            print(f"Database Initialization Error: {db_err}")
            # Don't exit on DB errors in production - let the app try to start
            if __name__ == '__main__':
                sys.exit(1)

if __name__ == '__main__':
    # We use '0.0.0.0' so you can test on local network devices
    # and 'debug=True' to enable the interactive debugger
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=True,
        use_reloader=True  # Automatically restarts when you save files
    )