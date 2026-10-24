# ⚓ Anchor: Cognitive State Manager for AI Agents
![Anchor Dashboard](c:\Users\dell\OneDrive\Pictures\Screenshots\anchor.png)
Current AI agents suffer from "amnesia" and "goal drift." They get distracted, lose track of their objective, and fill their context window with irrelevant junk. 

Anchor is a runtime state manager that sits between your agent's brain and its actions. It actively manages the agent's memory, prunes irrelevant thoughts, and forces the agent back on track if it starts drifting.

## Features
- **State Store:** Saves the agent's goal and step-by-step memories in SQLite.
- **Garbage Collector:** Automatically scores and deletes irrelevant memories to save context window tokens.
- **Goal Drift Detector:** Injects system alerts if the agent starts doing something unrelated to the main goal.
- **Live Dashboard:** A FastAPI web UI to watch the agent's memory mutate in real-time.

## Quick Start
1. Install dependencies:
   `pip install -r requirements.txt`
2. Run the dashboard:
   `python -m uvicorn anchor.server:app --reload`
3. Open `http://127.0.0.1:8000` in your browser.
4. Click **"Run Next Agent Step"** and watch the interceptor block bad memories.

## Docker
`docker build -t anchor .`
`docker run -p 8000:8000 anchor`