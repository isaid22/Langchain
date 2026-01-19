"""
Simple example of using Tavily with LangGraph
This is a minimal implementation to get you started quickly.
"""

from dotenv import load_dotenv
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Verify API keys
if not os.getenv("TAVILY_API_KEY"):
    print("Missing TAVILY_API_KEY. Add it to your .env file.")
    exit(1)

if not os.getenv("OPENAI_API_KEY"):
    print("Missing OPENAI_API_KEY. Add it to your .env file.")
    exit(1)

# Initialize Tavily search tool
search = TavilySearchResults(
    max_results=5,  # Number of search results to return
    search_depth="advanced",  # Options: "basic" or "advanced"
    include_answer=True,  # Include a short answer in the response
    include_raw_content=False,  # Don't include raw HTML
    include_images=False,  # Don't include images
)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create the agent with tools
# This is the simplest way to use LangGraph with tools
agent = create_react_agent(
    model=llm,
    tools=[search],
)

def research(query: str):
    """Run a research query using Tavily."""
    print(f"\n🔍 Researching: {query}\n")
    
    # Invoke the agent
    result = agent.invoke({"messages": [("user", query)]})
    
    # Get the final answer
    final_message = result["messages"][-1]
    
    print(f"\n📝 Answer:\n{final_message.content}\n")
    return final_message.content

if __name__ == "__main__":
    print("=" * 70)
    print("Tavily Search + LangGraph - Simple Example")
    print("=" * 70)
    
    # Example queries
    examples = [
        "What are the latest breakthroughs in AI in 2024?",
        "What is the weather forecast for major cities this week?",
        "Recent developments in renewable energy technology",
    ]
    
    print("\nExample queries:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")
    
    print("\nType 'quit' to exit\n")
    
    while True:
        query = input("Your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        try:
            research(query)
        except Exception as e:
            print(f"❌ Error: {e}\n")
