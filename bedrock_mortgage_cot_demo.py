from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_aws import ChatBedrock

from basic_calculations import calculate_affordability

load_dotenv()

# Ensure your AWS credentials are set in environment variables or ~/.aws/credentials
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME

# Switching to Amazon Titan which has easier access requirements than Claude 3
llm = ChatBedrock(
    model_id="amazon.nova-micro-v1:0",
    model_kwargs={"temperature": 0.1},
    # You can optionally pass a boto3 client if you need custom config
    # client=boto3_client 
)

prompt = PromptTemplate.from_template(
    """You are a mortgage affordability assistant. 

User inputs:
- Annual income: ${annual_income}
- Monthly debt: ${monthly_debt}
- Home price: ${home_price}
- Interest rate: {rate}%
- Term: {years} years
- DTI limit: {dti_limit}

The system has pre-calculated the following:
- Estimated Monthly Payment: ${monthly_payment:.2f}
- Max Monthly Budget: ${max_monthly_budget:.2f}
- Affordability: {is_affordable}

Instructions:
Walk through the math step-by-step to explain *why* the system determined it is {is_affordable}.
IMPORTANT: Use plain text only for calculations. Do NOT use LaTeX formatting (e.g., no \[ or \frac).
1. Calculate monthly gross income.
2. Verify the max total debt allowed.
3. Explain the remaining budget for a mortgage.
4. Compare the estimated payment to the budget.

Answer: Let's think step by step.
"""
)


def run_demo():
    annual_income = float(input("Annual income (e.g., 120000): "))
    monthly_debt = float(input("Monthly debt (e.g., 600): "))
    home_price = float(input("Home price of interest (e.g., 420000): "))
    rate = float(input("Interest rate (e.g., 6.5): "))
    years = int(input("Mortgage term in years (e.g., 30): "))
    dti_limit = 0.43

    # Calculate metrics using the python function
    is_affordable, monthly_payment, max_monthly_budget = calculate_affordability(
        annual_income=annual_income,
        monthly_debt=monthly_debt,
        home_price=home_price,
        rate=rate,
        year=years,
        dti_limit=dti_limit,
    )

    formatted_prompt = prompt.format(
        annual_income=annual_income,
        monthly_debt=monthly_debt,
        home_price=home_price,
        rate=rate,
        years=years,
        dti_limit=dti_limit,
        # Pass the calculated values to the prompt so the LLM can use them in its reasoning
        monthly_payment=monthly_payment,
        max_monthly_budget=max_monthly_budget,
        is_affordable=is_affordable 
    )

    print("\n--- Sending request to LLM (Bedrock) ---\n")
    response = llm.invoke(formatted_prompt)
    
    print("\n[DEBUG] Full Response Object:", response)
    print("\n[DEBUG] Response Metadata:", response.response_metadata)
    
    print("\n" + response.content)


if __name__ == "__main__":
    run_demo()
