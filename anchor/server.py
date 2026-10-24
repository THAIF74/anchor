from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from anchor.state import StateStore

app = FastAPI()
store = StateStore()

# Set up the initial state for the demo
goal = "Research 3 AI companies and write a summary."
store.set_goal(goal)
keywords = ["research", "ai", "companies", "summary", "openai", "anthropic"]

agent_actions = [
    "Searching for AI companies...",
    "Found OpenAI.",
    "Let me write a poem about a cat.", 
    "Found Anthropic.",
    "I am tired, let me sleep.",       
    "Drafting the final summary now."
]
current_step = 0

@app.get("/")
def index():
    return HTMLResponse(Path("ui/index.html").read_text(encoding="utf-8"))

@app.get("/api/state")
def get_state():
    return {
        "goal": store.get_goal(),
        "memories": store.get_memories(),
        "step": current_step
    }

@app.post("/api/step")
def take_step():
    global current_step
    if current_step >= len(agent_actions):
        return {"status": "done"}
    
    action = agent_actions[current_step]
    current_step += 1
    
    # 1. Add memory
    store.add_memory(step=current_step, content=action)
    
    # 2. Check Drift
    is_drifting, alert = store.detect_drift(action, keywords, current_step)
    
    # 3. Prune (limit to 4 to see it visually delete)
    store.prune_memories(goal_keywords=keywords, max_memories=4)
    
    return {"action": action, "drifted": is_drifting}

@app.post("/api/reset")
def reset():
    global current_step
    current_step = 0
    store.set_goal(goal)
    return {"status": "reset"}
