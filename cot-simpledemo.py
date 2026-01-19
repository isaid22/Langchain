from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)
print("##### PROMPT TEMPLATE FORMATED:", '\n' , prompt, '\n')
chain = prompt | llm
print("##### CHAIN FORMATED:", '\n' , chain, '\n')
# Example usage
question = "If I have 30 apples, use 20 for lunch, and buy 6 more, how many apples do I have?"
print(chain.invoke({"question": question}).content)