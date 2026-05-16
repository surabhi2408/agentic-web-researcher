from typing import TypedDict, List, Annotated
import operator
from langchain_core.messages import BaseMessage

class ResearchState(TypedDict):
    """
    Represents the state of our Web Research Agent.
    """
    # The initial research task given by the user
    task: str
    
    # Message history for LLM interactions (allows conversational flow and tool calling)
    messages: Annotated[List[BaseMessage], operator.add]
    
    # A list of steps or queries the agent plans to execute
    research_plan: List[str]
    
    # Extracted data from the web searches and scrapes
    research_context: List[str]
    
    # The final synthesized report
    final_report: str
