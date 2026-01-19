from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# Verify API keys
tavily_key = os.getenv("TAVILY_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if not tavily_key:
    print("Missing TAVILY_API_KEY. Add it to your .env file and re-run.")
    exit(1)

if not openai_key:
    print("Missing OPENAI_API_KEY. Add it to your .env file and re-run.")
    exit(1)

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the Tavily search tool
# max_results: number of search results to return
tavily_tool = TavilySearchResults(max_results=3)

# Create a list of tools
tools = [tavily_tool]

# Initialize the LLM with tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Define the agent node - decides whether to use tools or respond
def agent(state: AgentState):
    """The agent decides what to do based on the current state."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Define whether to continue or end
def should_continue(state: AgentState):
    """Determine if we should continue to tools or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If there are no tool calls, we're done
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools))

# Set the entry point
workflow.set_entry_point("agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

# Add edge from tools back to agent
workflow.add_edge("tools", "agent")

# Compile the graph
app = workflow.compile()

# Run the agent
def run_research_query(query: str):
    """Run a research query using the Tavily-powered agent."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")
    
    inputs = {"messages": [("user", query)]}
    
    # Stream the results
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"\n--- {key.upper()} ---")
            if "messages" in value:
                for msg in value["messages"]:
                    if hasattr(msg, 'content') and msg.content:
                        print(f"Content: {msg.content}")
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        print(f"Tool Calls: {msg.tool_calls}")
        print("\n")
    
    # Get the final response
    final_state = app.invoke(inputs)
    final_message = final_state["messages"][-1]
    
    print(f"\n{'='*60}")
    print("FINAL ANSWER:")
    print(f"{'='*60}")
    print(final_message.content)
    print(f"{'='*60}\n")
    
    return final_message.content

if __name__ == "__main__":
    # Example queries that will trigger Tavily search
    queries = [
        "What are the latest developments in quantum computing in 2024?",
        "Who won the most recent Nobel Prize in Physics and what was it for?",
        "What is the current situation with AI regulation in the European Union?"
    ]
    
    # Interactive mode
    print("\nTavily + LangGraph Research Assistant")
    print("=" * 60)
    print("\nExample queries:")
    for i, q in enumerate(queries, 1):
        print(f"{i}. {q}")
    print("\nType 'quit' to exit\n")
    
    while True:
        query = input("\nWhat would you like to research? ")
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not query.strip():
            print("Please enter a valid query.")
            continue
        
        try:
            run_research_query(query)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
