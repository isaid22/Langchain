"""
Visualize the LangGraph workflow
This script shows the state graph structure and saves it as an image
"""

from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# Set dummy keys if not available (just for visualization)
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-visualization"
if not os.getenv("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = "tvly-dummy-key-for-visualization"

# Define the state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize tools
tavily_tool = TavilySearchResults(max_results=3)
tools = [tavily_tool]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Define nodes
def agent(state: AgentState):
    """The agent decides what to do based on the current state."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """Determine if we should continue to tools or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
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

print("=" * 70)
print("LangGraph Workflow Visualization")
print("=" * 70)

# Try to display the graph using different methods
try:
    # Method 1: Save as PNG (requires pygraphviz or graphviz)
    print("\n📊 Attempting to generate graph visualization...\n")
    
    # Get the Mermaid diagram representation
    mermaid_diagram = app.get_graph().draw_mermaid()
    
    print("✅ Mermaid Diagram (copy this to https://mermaid.live):")
    print("-" * 70)
    print(mermaid_diagram)
    print("-" * 70)
    
    # Try to save as PNG
    try:
        png_data = app.get_graph().draw_mermaid_png()
        with open("langgraph_workflow.png", "wb") as f:
            f.write(png_data)
        print("\n✅ Graph saved as 'langgraph_workflow.png'")
    except Exception as e:
        print(f"\n⚠️  Could not save PNG (install graphviz): {e}")
    
except Exception as e:
    print(f"❌ Error generating visualization: {e}")
    print("\nFalling back to text representation...")

# Text-based visualization
print("\n" + "=" * 70)
print("TEXT REPRESENTATION OF THE WORKFLOW")
print("=" * 70)

print("""
┌──────────────────────────────────────────────────────────────┐
│                        START                                  │
│                          │                                    │
│                          ▼                                    │
│                   ┌─────────────┐                            │
│                   │   AGENT     │                            │
│                   │   (LLM)     │                            │
│                   │             │                            │
│                   │ Decides:    │                            │
│                   │ - Use tool? │                            │
│                   │ - Or answer?│                            │
│                   └──────┬──────┘                            │
│                          │                                    │
│                   should_continue()                          │
│                     (conditional)                            │
│                          │                                    │
│              ┌───────────┴───────────┐                       │
│              │                       │                       │
│         tool_calls?              no tool_calls               │
│              │                       │                       │
│              ▼                       ▼                       │
│      ┌──────────────┐           ┌────────┐                  │
│      │    TOOLS     │           │  END   │                  │
│      │   (Tavily)   │           │        │                  │
│      │              │           └────────┘                  │
│      │ - Search web │                                        │
│      │ - Return     │                                        │
│      │   results    │                                        │
│      └──────┬───────┘                                        │
│             │                                                 │
│             │ (always)                                        │
│             │                                                 │
│             └─────────────┐                                   │
│                           │                                   │
│                           ▼                                   │
│                   ┌─────────────┐                            │
│                   │   AGENT     │◄───┐                       │
│                   │   (LLM)     │    │                       │
│                   └─────────────┘    │                       │
│                                      │                       │
│                     Loop continues until agent                │
│                     decides it has enough info                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
""")

print("\n" + "=" * 70)
print("DETAILED FLOW EXPLANATION")
print("=" * 70)

print("""
1️⃣  START → AGENT
    • User provides a query/question
    • Enters the graph at the 'agent' node

2️⃣  AGENT (LLM Decision)
    • LLM receives the messages
    • Decides if it needs to use tools (Tavily search)
    • Options:
      a) Has enough info → Generate final answer
      b) Needs more info → Call Tavily tool

3️⃣  CONDITIONAL EDGE (should_continue)
    • Checks if agent made tool_calls
    • Routes to one of two paths:
      
      Path A: tool_calls exist → "continue" → TOOLS node
      Path B: no tool_calls → "end" → END

4️⃣  TOOLS (Tavily Search)
    • Executes the Tavily search
    • Gets web search results
    • Adds results to message history
    • ALWAYS goes back to AGENT

5️⃣  LOOP BACK TO AGENT
    • Agent sees the search results
    • Can decide to:
      a) Search again (different query)
      b) Answer with the info it has
    
6️⃣  END
    • Final answer is ready
    • Returns to user
""")

print("\n" + "=" * 70)
print("NODE DETAILS")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────┐
│ NODE: agent                                             │
├─────────────────────────────────────────────────────────┤
│ Type: Function                                          │
│ Purpose: LLM decision-making                           │
│ Input: AgentState (contains messages)                  │
│ Output: Updated state with LLM response                │
│ LLM Tools: Tavily search bound to model                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ NODE: tools                                             │
├─────────────────────────────────────────────────────────┤
│ Type: ToolNode (built-in)                              │
│ Purpose: Execute tool calls                            │
│ Input: Messages with tool_calls                        │
│ Output: Tool results added to messages                 │
│ Tools: [TavilySearchResults]                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ CONDITIONAL: should_continue                            │
├─────────────────────────────────────────────────────────┤
│ Type: Decision function                                │
│ Logic: Check if last message has tool_calls            │
│ Routes:                                                 │
│   • "continue" → tools node                            │
│   • "end" → END                                        │
└─────────────────────────────────────────────────────────┘
""")

print("\n" + "=" * 70)
print("STATE STRUCTURE")
print("=" * 70)

print("""
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    
• messages: List of all messages in the conversation
  - User messages
  - AI responses
  - Tool calls
  - Tool results
  
• add_messages: Special reducer that appends new messages
  instead of replacing the entire list
""")

print("\n" + "=" * 70)
print("EXAMPLE EXECUTION TRACE")
print("=" * 70)

print("""
User Query: "What are the latest AI developments in 2024?"

Step 1: START → agent
  State: {messages: [HumanMessage("What are the latest AI...")]}

Step 2: agent processes
  LLM thinks: "I need current info, I'll search"
  State: {messages: [..., AIMessage(tool_calls=[TavilySearch])]}

Step 3: should_continue → "continue" → tools
  
Step 4: tools executes Tavily search
  Searches web for "AI developments 2024"
  State: {messages: [..., ToolMessage(results="...")]}

Step 5: tools → agent (automatic edge)

Step 6: agent processes results
  LLM thinks: "Good info, I can answer now"
  State: {messages: [..., AIMessage("Based on recent...")]}

Step 7: should_continue → "end" → END

Result: Final answer delivered to user
""")

print("\n" + "=" * 70)
print("VISUALIZATION OPTIONS")
print("=" * 70)

print("""
1. Copy the Mermaid diagram above and paste it at:
   🔗 https://mermaid.live
   
2. If PNG was generated, open:
   📁 langgraph_workflow.png
   
3. Install graphviz for automatic PNG generation:
   pip install pygraphviz
   # or
   sudo apt-get install graphviz
   pip install graphviz
""")

print("\n✅ Visualization complete!\n")
