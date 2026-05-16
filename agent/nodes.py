import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from .state import ResearchState
from .tools import research_tools

# We will initialize the LLM. 
# It will use the GEMINI_API_KEY from your .env file automatically.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Bind the tools to our LLM so it knows it can search and scrape
llm_with_tools = llm.bind_tools(research_tools)

def planner_node(state: ResearchState):
    """
    Looks at the user's task and decides what to search for.
    """
    task = state["task"]
    
    system_prompt = (
        "You are a web research planner. The user will give you a task. "
        "Your job is to break it down into 1-3 clear, actionable web search queries. "
        "Return the queries as a simple numbered list."
    )
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=task)
    ])
    
    # Simple parsing: split by newlines to get the plan
    plan_steps = [line.strip() for line in response.content.split('\n') if line.strip()]
    
    return {"research_plan": plan_steps}

def researcher_node(state: ResearchState):
    """
    Executes the research plan using the LLM equipped with tools.
    """
    messages = state.get("messages", [])
    
    if not messages:
        # First time entering the researcher node
        plan_str = "\n".join(state.get("research_plan", []))
        instructions = (
            f"You are an expert researcher. Your task is: {state['task']}\n"
            f"Here is your research plan:\n{plan_str}\n\n"
            "Use the web_search tool to find information. "
            "If you need to read a specific article in depth, use the scrape_webpage tool. "
            "Gather as much factual information as possible."
        )
        messages.append(SystemMessage(content=instructions))
        messages.append(HumanMessage(content="Begin your research."))

    # The LLM decides what to do next (call a tool, or if it has enough info, respond)
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response]}

def writer_node(state: ResearchState):
    """
    Takes all the gathered messages and tools outputs and writes a final report.
    """
    task = state["task"]
    messages = state["messages"]
    
    # We pass the entire conversation history so the writer knows what was found
    system_prompt = (
        "You are an expert technical writer. You will be provided with a research task and "
        "the raw history of a research agent that gathered information from the web.\n"
        "Your goal is to synthesize this information into a clean, comprehensive, and "
        "well-formatted final report using Markdown. Do not include the internal steps, "
        "just the final knowledge."
    )
    
    # Convert messages to text to avoid Gemini's strict alternating message role constraints
    history_text = "\n".join([f"{msg.type}: {str(msg.content)[:2000]}" for msg in messages if hasattr(msg, 'content')])
    
    # Ask the LLM to write the report
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Task: {task}\n\nResearch History:\n{history_text}\n\nNow, write the final report:")
    ])
    
    return {"final_report": response.content}

# The ToolNode automatically runs the tools when the LLM requests them
tool_node = ToolNode(research_tools)
