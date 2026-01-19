def calculate_affordability(annual_income, monthly_debt, home_price, rate, year= 30, dti_limit=0.43):
    """
    Calculate if a user can afford a home based on their financial details.

    Parameters:
    - annual_income (float): The user's annual income.
    - monthly_debt (float): The user's total monthly debt payments.
    - home_price (float): The price of the home the user wants to buy.
    - rate (float): The annual interest rate (as a decimal).
    - year (int): The loan term in years (default is 30 years).
    - dti_limit (float): The maximum debt-to-income ratio allowed (default is 0.43).

    Returns:
    - bool: True if the user can afford the home, False otherwise.
    - float: The estimated total monthly mortgage payment.
    - float: The maximum monthly mortgage budget based on DTI limit.
    """

    monthly_gross = annual_income / 12
    max_total_debt = monthly_gross * dti_limit
    max_monthly_mortgage_budget = max_total_debt - monthly_debt

    #Amortize for P&I
    r = (rate / 100) / 12
    n = year* 12
    p_and_i = home_price * (r * (1 + r) ** n) / ((1 + r) ** n - 1)  

    # Estimate Taxes and Insurance (Assuming 1.5% annually )
    taxes_and_insurance = (home_price * 0.015) / 12
    total_monthly_payment = p_and_i + taxes_and_insurance

    is_affordable = total_monthly_payment <= max_monthly_mortgage_budget
    return is_affordable, total_monthly_payment, max_monthly_mortgage_budget