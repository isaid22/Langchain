# Tavily + LangGraph Examples

This directory contains examples of using **Tavily API** with **LangGraph** for intelligent web search and research.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Tavily API Key

1. Sign up at [https://tavily.com](https://tavily.com)
2. Get your API key from the dashboard
3. Add it to your `.env` file:

```bash
TAVILY_API_KEY=tvly-your-api-key-here
OPENAI_API_KEY=sk-your-openai-key-here
```

## Examples

### 🚀 Simple Example: `tavily_simple_example.py`

**Best for:** Quick start, simple searches

This uses LangGraph's built-in `create_react_agent` which automatically handles the agent loop.

```bash
python tavily_simple_example.py
```

**Features:**
- Minimal code (~70 lines)
- Easy to understand
- Perfect for getting started
- Uses ReAct pattern automatically

**Code snippet:**
```python
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

search = TavilySearchResults(max_results=5)
agent = create_react_agent(model=llm, tools=[search])
result = agent.invoke({"messages": [("user", query)]})
```

---

### 🔧 Advanced Example: `tavily_langgraph_example.py`

**Best for:** Learning LangGraph internals, custom workflows

This builds a custom LangGraph workflow from scratch, showing you exactly how the agent works.

```bash
python tavily_langgraph_example.py
```

**Features:**
- Full control over the agent loop
- Shows StateGraph construction
- Demonstrates conditional edges
- Streaming support
- Educational - see how LangGraph works under the hood

**What it demonstrates:**
1. Custom state definition with `TypedDict`
2. Creating nodes (agent, tools)
3. Adding conditional edges
4. Tool invocation
5. Message handling

---

## Tavily Configuration Options

```python
TavilySearchResults(
    max_results=5,              # Number of results (1-10)
    search_depth="advanced",    # "basic" or "advanced"
    include_answer=True,        # Include AI-generated answer
    include_raw_content=False,  # Include raw HTML
    include_images=True,        # Include relevant images
    include_domains=[],         # Specific domains to search
    exclude_domains=[],         # Domains to exclude
)
```

### Search Depth Comparison

- **basic**: Faster, cheaper, good for simple queries
- **advanced**: Slower, more thorough, better for research

---

## Example Queries

Great queries for testing Tavily:

1. **Current Events**
   - "What are the latest developments in AI regulation?"
   - "Recent breakthroughs in quantum computing"
   - "Current status of climate change negotiations"

2. **Research**
   - "Compare the top 3 programming languages for data science in 2024"
   - "What are the pros and cons of different renewable energy sources?"
   - "Latest findings on the health benefits of Mediterranean diet"

3. **Fact-Finding**
   - "Who are the current leaders of G7 countries?"
   - "What are the most popular electric vehicles in 2024?"
   - "Timeline of major space exploration missions this year"

---

## How It Works

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Agent     │ ◄─┐
│  (LLM)      │   │
└──────┬──────┘   │
       │          │
       │ Decides  │
       │          │
       ▼          │
┌─────────────┐   │
│   Tools     │   │
│  (Tavily)   │   │
└──────┬──────┘   │
       │          │
       └──────────┘
       
Final Answer
```

1. **User** asks a question
2. **Agent** (LLM) decides if it needs to search
3. **Tavily** performs web search
4. **Agent** processes results and may search again
5. Loop continues until agent has enough info
6. **Final answer** is provided

---

## Tips

### Getting Better Results

1. **Be Specific**: "Latest AI breakthroughs in healthcare 2024" > "AI news"
2. **Use Keywords**: Include relevant technical terms
3. **Ask for Comparisons**: "Compare X vs Y" works well
4. **Request Recent Info**: Tavily excels at current information

### When to Use Tavily

✅ **Good for:**
- Current events and news
- Recent research and papers
- Product comparisons
- Fact-checking
- Market research

❌ **Not ideal for:**
- Historical facts (before 2020)
- Personal data
- Behind paywalls
- Mathematical calculations
- Code generation (without context)

---

## Troubleshooting

### "Missing TAVILY_API_KEY"
Add your key to `.env`:
```bash
TAVILY_API_KEY=tvly-xxxxx
```

### "Rate limit exceeded"
- Free tier: 1,000 searches/month
- Upgrade at [tavily.com/pricing](https://tavily.com/pricing)

### "No results found"
- Try rephrasing your query
- Use more common terms
- Check if domain restrictions are too narrow

---

## Next Steps

1. **Customize**: Modify the examples for your use case
2. **Add Tools**: Combine Tavily with other LangChain tools
3. **Memory**: Add conversation memory to track context
4. **Agents**: Build multi-agent systems with LangGraph
5. **UI**: Add a frontend with Streamlit or Gradio

---

## Resources

- [Tavily API Docs](https://docs.tavily.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools/)

---

Happy researching! 🔍✨
