from db_init import get_connection

def save_feedback(question, answer, rating, comments=""):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO feedback (question, answer, rating, comments) VALUES (?, ?, ?, ?)",
            (question, answer, int(rating), comments),
        )
