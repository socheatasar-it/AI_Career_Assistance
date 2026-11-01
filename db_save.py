from db_init import get_connection, _sql

def save_profile(name, interests, skills, education, goal):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(_sql("""INSERT INTO saved_profiles
            (name, interests, skills, education, goal) VALUES (?, ?, ?, ?, ?)"""),
            (name, interests, skills, education, goal))
