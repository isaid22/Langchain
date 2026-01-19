from dotenv import load_dotenv
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


examples = [
    {
        "question": "If I have 10 tennis balls and I lost 3, how many balls do I have left?",
        "answer": "Let's think step by step. You start with 10 tennis balls and lose 3. So, 10 - 3 = 7. Therefore, you have 7 tennis balls left."
    }
]

example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="Question: {question}\nAnswer: {answer}",
)

fewshot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Answer the following questions as best you can.",
    example_separator="\n\n",
    suffix="Question: {question}\nAnswer: Let's think step by step.",
    input_variables=["question"],
)
print("##### PROMPT TEMPLATE FORMATTED:\n", fewshot_prompt.format(question="If I have 30 apples, use 20 for lunch, and buy 6 more, how many apples do I have?"), "\n")

chain = fewshot_prompt | llm
print("##### CHAIN FORMATTED:\n", chain, "\n")

# Example usage
question = "If I have 30 apples, use 20 for lunch, and buy 6 more, how many apples do I have?"
print(chain.invoke({"question": question}).content)