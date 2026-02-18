from data import init_feedback_db, init_sentiment_db, init_users_db, init_sessions_db
from login import run_login
from dashboard import run_dashboard

def main_app_loop():
    # Calling all separate original init functions
    init_feedback_db()
    init_sentiment_db()
    init_users_db()
    init_sessions_db() # New session privacy DB
    
    # Start login process
    user_email = run_login()
    
    # If login succeeds, run the dashboard
    if user_email:
        run_dashboard(None, user_email)

if __name__ == "__main__":
    main_app_loop()

