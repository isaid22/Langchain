from dotenv import load_dotenv
try:
    from langchain_core.pydantic_v1 import BaseModel  # Prefer LC's vendored v1 for parser compatibility
except Exception:  # fallback if not available
    from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
import os
import sys


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Guard: ensure we have an API key to avoid confusing runtime errors
if not openai_key:
    print("Missing OPENAI_API_KEY. Add it to your .env file and re-run.")
    sys.exit(1)


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# OpenAI (default)
openai_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=openai_key,
    # base_url="https://api.openai.com/v1"  # default, no need to specify
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = []
agent_executor = create_agent(
    model=openai_llm,
    tools=tools
)

query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"messages": [("user", query)]})

try:
    # Get the last message from the agent
    last_message = raw_response["messages"][-1].content
    structured_response = parser.parse(last_message)
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e)
    print("Raw Response:", raw_response)