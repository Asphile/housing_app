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

if __name__ == '__main__':
    # --- AUTOMATIC DATABASE INITIALIZATION ---
    # This part ensures all your SQLAlchemy models are turned into
    # actual database tables in 'site.db' before the app starts.
    with app.app_context():
        try:
            db.create_all()
            print("\n" + "*"*30)
            print("DATABASE SYNCED SUCCESSFULLY")
            print("*"*30 + "\n")
        except Exception as db_err:
            print(f"Database Initialization Error: {db_err}")

    # We use '0.0.0.0' so you can test on local network devices
    # and 'debug=True' to enable the interactive debugger
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        use_reloader=True  # Automatically restarts when you save files
    )