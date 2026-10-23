from anchor.state import StateStore

store = StateStore()
store.set_goal("Research 3 AI companies and write a summary.")
print(f"🎯 Current Goal: {store.get_goal()}\n")

keywords = ["research", "ai", "companies", "summary", "openai", "anthropic"]

# Step 1: On track
action_1 = "Searching for AI companies..."
store.add_memory(step=1, content=action_1)
drift, msg = store.detect_drift(action_1, keywords, step=1)
print(f"Action 1: {action_1} -> Drift? {drift}")

# Step 2: On track
action_2 = "Found OpenAI and Anthropic."
store.add_memory(step=2, content=action_2)
drift, msg = store.detect_drift(action_2, keywords, step=2)
print(f"Action 2: {action_2} -> Drift? {drift}")

# Step 3: THE AGENT GETS DISTRACTED (Drift!)
action_3 = "Let me write a poem about a cat."
store.add_memory(step=3, content=action_3)
drift, msg = store.detect_drift(action_3, keywords, step=3)
print(f"Action 3: {action_3} -> Drift? {drift}")
print(f"   {msg}")

print("\n--- Current Memory State ---")
for mem in store.get_memories():
    print(f"  [Step {mem['step']}] {mem['content']}")
