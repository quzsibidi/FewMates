import sqlite3
from typing import List
from google.genai import types

DB_PATH = "chat_history.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                title TEXT NOT NULL,
                course TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        conn.commit()

def save_message(session_id: str, role: str, content: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        conn.commit()

def get_session_history(session_id: str) -> List[types.Content]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM history WHERE session_id = ? ORDER BY id ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
        
    history = []
    for role, content in rows:
        history.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=content)]
            )
        )
    return history

def delete_session(session_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM exams WHERE session_id = ?", (session_id,))
        conn.commit()
        return cursor.rowcount > 0

def add_exam(session_id: str, title: str, course: str, date: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO exams (session_id, title, course, date) VALUES (?, ?, ?, ?)",
            (session_id, title, course, date)
        )
        conn.commit()

def get_exams(session_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, course, date FROM exams WHERE session_id = ?", (session_id,))
        return cursor.fetchall()