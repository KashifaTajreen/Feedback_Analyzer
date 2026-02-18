import sqlite3
import bcrypt

def init_feedback_db():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        reviewer_name TEXT, reviewer_ID TEXT, score INTEGER, 
        comment TEXT, session_id TEXT)""")
    conn.commit()
    conn.close()

def init_sentiment_db():
    conn = sqlite3.connect("sentiment.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        session_name TEXT, session_id TEXT, overall_sentiment REAL)""")
    conn.commit()
    conn.close()

def init_users_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

def email_exists(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def create_account(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw.decode('utf-8')))
    conn.commit()
    conn.close()

def validate_login(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_hash = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    return False

def insert_feedback(reviewer_name, reviewer_ID, score, comment, session_id):
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback VALUES (?, ?, ?, ?, ?)", (reviewer_name, reviewer_ID, score, comment, session_id))
    conn.commit()
    conn.close()

def insert_sentiment(session_name, session_id, overall_sentiment):
    conn = sqlite3.connect("sentiment.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback VALUES (?, ?, ?)", (session_name, session_id, overall_sentiment))
    conn.commit()
    conn.close()

def get_session_summary(session_id):
    conn_f = sqlite3.connect("feedback.db")
    avg_score = conn_f.execute("SELECT AVG(score) FROM feedback WHERE session_id=?", (session_id,)).fetchone()[0]
    conn_f.close()
    conn_s = sqlite3.connect("sentiment.db")
    avg_sent = conn_s.execute("SELECT AVG(overall_sentiment) FROM feedback WHERE session_id=?", (session_id,)).fetchone()[0]
    conn_s.close()
    return {'avg_score': avg_score or 0.0, 'avg_sentiment': avg_sent or 0.0}

def get_comments_for_session(session_id):
    conn = sqlite3.connect("feedback.db")
    res = conn.execute("SELECT score, comment FROM feedback WHERE session_id=?", (session_id,)).fetchall()
    conn.close()
    return res

def get_score_distribution(session_id):
    conn = sqlite3.connect("feedback.db")
    rows = conn.execute("SELECT score, COUNT(*) FROM feedback WHERE session_id=? GROUP BY score", (session_id,)).fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

# --- NEW SESSION FUNCTIONS ---
def init_sessions_db():
    conn = sqlite3.connect("sessions.db")
    conn.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, name TEXT, date TEXT, password TEXT, host TEXT)")
    try:
        conn.execute("ALTER TABLE sessions ADD COLUMN host TEXT")
    except:
        pass
    conn.commit()
    conn.close()

def insert_new_session(s_id, s_name, s_date, s_pass,s_host):
    conn = sqlite3.connect("sessions.db")
    conn.execute("INSERT INTO sessions VALUES (?, ?, ?, ?,?)", (s_id, s_name, s_date, s_pass,s_host))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect("sessions.db")
    cursor = conn.execute("SELECT id, name, date, password, host FROM sessions")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "date": r[2], "password": r[3], "host":r[4] if r[4] else "N/A"} for r in rows]

def delete_session(session_id):
    """Permanently removes session from sessions.db and feedback from feedback.db."""
    try:
        # 1. Delete from sessions.db
        conn_s = sqlite3.connect('sessions.db')
        conn_s.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn_s.commit()
        conn_s.close()

        # 2. Delete from feedback.db
        conn_f = sqlite3.connect('feedback.db')
        conn_f.execute("DELETE FROM feedback WHERE session_id = ?", (session_id,))
        conn_f.commit()
        conn_f.close()
        
        return True
    except Exception as e:
        print(f"SQL Error: {e}")
        return False