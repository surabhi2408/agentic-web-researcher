from langgraph.graph import StateGraph, END
from typing import Literal
from .state import ResearchState
from .nodes import planner_node, researcher_node, writer_node, tool_node

def should_continue(state: ResearchState) -> Literal["tools", "writer"]:
    """
    Determines whether the researcher needs to use more tools or is ready to write the report.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM made a tool call, we must route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    
    # Otherwise, it has finished gathering info and we can route to the "writer" node
    return "writer"

# Initialize the state graph
workflow = StateGraph(ResearchState)

# Add our nodes to the graph
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("tools", tool_node)
workflow.add_node("writer", writer_node)

# Set the entry point (the graph starts at the planner)
workflow.set_entry_point("planner")

# Planner goes straight to the researcher
workflow.add_edge("planner", "researcher")

# The researcher has a conditional edge:
# It either calls tools OR goes to the writer
workflow.add_conditional_edges("researcher", should_continue, {
    "tools": "tools",
    "writer": "writer"
})

# After tools run, they ALWAYS return their output back to the researcher
workflow.add_edge("tools", "researcher")

# The writer is the final step, then the graph ends
workflow.add_edge("writer", END)

# Compile the graph into an executable application
app = workflow.compile()
