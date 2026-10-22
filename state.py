# anchor/state.py
import sqlite3
import time
import json

class StateStore:
    def __init__(self, db_path="anchor.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_state (
                    id INTEGER PRIMARY KEY,
                    goal TEXT,
                    created_at REAL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    step INTEGER,
                    content TEXT,
                    timestamp REAL
                )
            """)

    def set_goal(self, goal: str):
        with self.conn:
            self.conn.execute("DELETE FROM agent_state")
            self.conn.execute("INSERT INTO agent_state (goal, created_at) VALUES (?, ?)", (goal, time.time()))
            self.conn.execute("DELETE FROM memories") # Clear old memories for new goal

    def get_goal(self) -> str:
        row = self.conn.execute("SELECT goal FROM agent_state LIMIT 1").fetchone()
        return row["goal"] if row else None

    def add_memory(self, step: int, content: str):
        with self.conn:
            self.conn.execute(
                "INSERT INTO memories (step, content, timestamp) VALUES (?, ?, ?)",
                (step, content, time.time())
            )

    def get_memories(self) -> list:
        rows = self.conn.execute("SELECT * FROM memories ORDER BY step ASC").fetchall()
        return [dict(r) for r in rows]

    def clear_memories(self):
        with self.conn:
            self.conn.execute("DELETE FROM memories")