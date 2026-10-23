import sqlite3
import time

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
            self.conn.execute("DELETE FROM memories")

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

    def prune_memories(self, goal_keywords: list, max_memories: int = 3):
        memories = self.get_memories()
        if len(memories) <= max_memories:
            return

        scored_memories = []
        for i, mem in enumerate(memories):
            score = 0
            content_lower = mem["content"].lower()
            for kw in goal_keywords:
                if kw.lower() in content_lower:
                    score += 10
            score += i
            scored_memories.append((score, mem))

        scored_memories.sort(key=lambda x: x[0])
        num_to_delete = len(memories) - max_memories
        for i in range(num_to_delete):
            worst_memory = scored_memories[i][1]
            with self.conn:
                self.conn.execute("DELETE FROM memories WHERE id = ?", (worst_memory["id"],))

    # --- NEW CODE: DRIFT DETECTOR ---
    def detect_drift(self, current_action: str, goal_keywords: list, step: int):
        """Checks if the current action matches the goal. If not, injects a system alert."""
        action_lower = current_action.lower()
        matches = sum(1 for kw in goal_keywords if kw.lower() in action_lower)

        # If the action has 0 keyword matches, it's drifting
        if matches == 0:
            alert = f"⚠️ SYSTEM ALERT: You are drifting from the goal! Refocus on: {self.get_goal()}"
            self.add_memory(step=step, content=alert)
            return True, alert
        
        return False, "On track."
