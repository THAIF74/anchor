from anchor.state import StateStore

# 1. Initialize the State Store
store = StateStore()
goal = "Research 3 AI companies and write a summary."
store.set_goal(goal)
keywords = ["research", "ai", "companies", "summary", "openai", "anthropic"]

print(f"🎯 GOAL: {goal}\n")

# 2. This is our Mock Agent's brain. 
# It generates fake actions to simulate an AI trying to solve the task.
agent_actions = [
    "Searching for AI companies...",
    "Found OpenAI.",
    "Let me write a poem about a cat.", # <- Drift!
    "Found Anthropic.",
    "I am tired, let me sleep.",       # <- Drift!
    "Drafting the final summary now."
]

# 3. The Agent Loop
for step, action in enumerate(agent_actions, start=1):
    print(f"🤖 Agent Action {step}: {action}")
    
    # --- THE INTERCEPTOR ---
    # Before we let the agent move forward, we run our State Checks
    
    # A. Add the action to memory
    store.add_memory(step=step, content=action)
    
    # B. Check for Goal Drift
    is_drifting, alert = store.detect_drift(action, keywords, step)
    if is_drifting:
        print(f"   [INTERCEPTOR] 🛑 {alert}")
        # The agent "sees" the alert and immediately corrects itself
        # (In a real agent, the LLM would read this alert and change its next action)
        continue 
        
    # C. Prune memories if we have too many (Garbage Collector)
    # We will set a strict limit of 4 memories to show it working fast
    store.prune_memories(goal_keywords=keywords, max_memories=4)
    
    print(f"   [INTERCEPTOR] ✅ On track. Memory saved.")

# 4. Show the final state
print("\n--- FINAL AGENT MEMORY ---")
for mem in store.get_memories():
    print(f"  [Step {mem['step']}] {mem['content']}")
