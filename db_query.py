from db_init import get_connection, _sql
#from metrics import LLMCallRecord

def get_career_suggestions(query=""):
    search = f"%{query.strip()}%"
    sql = """SELECT id, title, description, skills FROM careers
             WHERE title LIKE ? OR description LIKE ? OR skills LIKE ?
             ORDER BY title LIMIT 50"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(_sql(sql), (search, search, search))
        rows = cur.fetchall()
        return [dict(row) if not isinstance(row, dict) else row for row in rows]

def get_profile_count():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) AS n FROM saved_profiles")
        row = cur.fetchone()
        return row["n"] if isinstance(row, dict) else row[0]
