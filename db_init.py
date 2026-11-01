import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

def _is_postgres():
    return DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg://"))

@contextmanager
def get_connection():
    if _is_postgres():
        import psycopg
        from psycopg.rows import dict_row
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        import sqlite3
        path = os.getenv("SQLITE_PATH", "career_assistance.db")
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

def _sql(statement):
    return statement.replace("?", "%s") if _is_postgres() else statement

def execute(sql, params=()):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(_sql(sql), params)
        return cur

def init_db():
    statements = [
        """CREATE TABLE IF NOT EXISTS careers (
            id SERIAL PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL, skills TEXT NOT NULL
        )""" if _is_postgres() else """CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, skills TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS saved_profiles (
            id SERIAL PRIMARY KEY, name TEXT, interests TEXT, skills TEXT, education TEXT, goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""" if _is_postgres() else """CREATE TABLE IF NOT EXISTS saved_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, interests TEXT, skills TEXT, education TEXT, goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY, question TEXT, answer TEXT, rating INTEGER, comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""" if _is_postgres() else """CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, rating INTEGER, comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    ]
    with get_connection() as conn:
        cur = conn.cursor()
        for statement in statements:
            cur.execute(statement)
        # Seed a small catalogue only when empty.
        cur.execute("SELECT COUNT(*) AS n FROM careers")
        row = cur.fetchone()
        count = row["n"] if isinstance(row, dict) else row[0]
        if count == 0:
            seed = [
                ("Data Analyst", "Turn data into insights for business decisions.", "SQL, spreadsheets, Python, statistics"),
                ("Software Developer", "Build and maintain applications and software systems.", "Programming, debugging, Git, problem-solving"),
                ("UX/UI Designer", "Design usable, accessible digital experiences.", "Figma, research, prototyping, visual design"),
                ("Cybersecurity Analyst", "Help protect systems, networks, and information.", "Networking, security basics, Linux, analysis"),
                ("Digital Marketer", "Plan campaigns and measure online marketing results.", "Content, analytics, SEO, communication"),
                ("Healthcare Administrator", "Support the operations of healthcare services.", "Organization, communication, planning"),
                ("Project Coordinator", "Help teams plan tasks, timelines, and delivery.", "Planning, collaboration, documentation"),
                ("Teacher / Trainer", "Help people learn knowledge and practical skills.", "Communication, subject knowledge, patience"),
            ]
            for item in seed:
                cur.execute(_sql("INSERT INTO careers (title, description, skills) VALUES (?, ?, ?)"), item)
