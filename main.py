import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from agent.graph import app

async def main():
    print("System: Welcome to the Autonomous Web Research Agent!")
    print("-----------------------------------------------")
    
    # Prompt the user for a task
    user_task = input("Enter a research topic or question: ")
    if not user_task.strip():
        print("No task provided. Exiting.")
        return

    print("\n[System] Starting research process... This may take a few minutes depending on the complexity.\n")

    # Initial state
    inputs = {"task": user_task, "messages": []}

    # Stream the graph execution
    try:
        # We use stream so we can see what node is currently running
        async for event in app.astream(inputs, stream_mode="updates"):
            for node_name, state_update in event.items():
                print(f"-> [Node Executed]: {node_name}")
                
                # If planner just finished, let's print the plan
                if node_name == "planner":
                    print("   - Research Plan:")
                    for step in state_update.get("research_plan", []):
                        print(f"      - {step}")
                
                # If writer just finished, print the final report!
                if node_name == "writer":
                    final_report_text = state_update.get("final_report", "")
                    
                    # Save it to a file
                    with open("research_report.md", "w", encoding="utf-8") as f:
                        f.write(final_report_text)
                        
                    print("\n" + "="*50)
                    print("FINAL REPORT HAS BEEN SAVED TO: research_report.md")
                    print("="*50)
                    print(final_report_text)
                    print("="*50)
                    
    except Exception as e:
        print(f"\n[Error] An error occurred during execution: {e}")
        print("Note: If you are seeing an Insufficient Quota error, it means your API key does not have billing credits.")

if __name__ == "__main__":
    asyncio.run(main())
