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
            print("✅ Memory limit not reached. No pruning needed.")
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
        print(f"🧹 Pruning {num_to_delete} irrelevant memories...")

        for i in range(num_to_delete):
            worst_memory = scored_memories[i][1]
            print(f"   🗑️ Deleting: '{worst_memory['content']}' (Score: {scored_memories[i][0]})")
            with self.conn:
                self.conn.execute("DELETE FROM memories WHERE id = ?", (worst_memory["id"],))
