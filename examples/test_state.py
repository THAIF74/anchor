from anchor.state import StateStore

store = StateStore()
store.set_goal("Research 3 AI companies and write a summary.")
print(f"🎯 Current Goal: {store.get_goal()}\n")

store.add_memory(step=1, content="Searching for AI companies...")
store.add_memory(step=2, content="Found OpenAI.")
store.add_memory(step=3, content="Found Anthropic.")
store.add_memory(step=4, content="Got distracted and looked up cat videos.")

print("🧠 Agent Memories:")
for mem in store.get_memories():
    print(f"  [Step {mem['step']}] {mem['content']}")