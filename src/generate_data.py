import csv
import random
from pathlib import Path

random.seed(20261102)

output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

headers = [
    "Borrower_ID",
    "Annual_Income_INR",
    "Existing_Monthly_Debt_INR",
    "Loan_Amount_INR",
    "Annual_Interest_Rate",
    "Tenure_Months",
    "Credit_Score",
    "Annual_Cash_Available_INR",
    "Existing_Annual_Debt_Service_INR",
    "Collateral_Value_INR",
    "New_Loan_EMI_INR",
    "Post_Loan_DTI",
    "DSCR",
    "Assumed_PD",
    "Assumed_LGD",
    "One_Year_ECL_INR",
    "Risk_Grade",
]

rows = []

for i in range(1, 501):
    # Generate synthetic borrower details.
    credit_score = random.randint(540, 835)
    annual_income = random.randrange(360000, 2400001, 12000)
    principal = random.randrange(100000, 1600001, 10000)
    annual_rate = round(random.uniform(0.085, 0.185), 4)
    tenure_months = random.choice([24, 36, 48, 60, 72])

    monthly_income = annual_income / 12
    existing_monthly_debt = round(
        monthly_income * random.uniform(0.05, 0.36), 2
    )
    annual_cash_available = round(
        annual_income * random.uniform(0.32, 0.65), 2
    )
    existing_annual_debt_service = round(existing_monthly_debt * 12, 2)
    collateral_value = round(principal * random.uniform(0.65, 1.4), 2)

    # Calculate EMI and repayment ratios.
    monthly_rate = annual_rate / 12
    growth_factor = (1 + monthly_rate) ** tenure_months

    monthly_emi = (
        principal * monthly_rate * growth_factor / (growth_factor - 1)
    )
    dti = (existing_monthly_debt + monthly_emi) / monthly_income
    dscr = annual_cash_available / (
        existing_annual_debt_service + monthly_emi * 12
    )

    # Calculate assumed risk measures.
    pd = min(
        0.40,
        max(
            0.008,
            0.035
            + (700 - credit_score) * 0.00032
            + max(dti - 0.40, 0) * 0.15,
        ),
    )
    lgd = max(
        0.15,
        min(0.85, 1 - 0.70 * collateral_value / principal),
    )
    ecl = principal * pd * lgd

    if pd >= 0.09 or dscr < 1:
        risk_grade = "High"
    elif pd >= 0.045 or dscr < 1.25:
        risk_grade = "Moderate"
    else:
        risk_grade = "Low"

    rows.append([
        f"B{i:04d}",
        annual_income,
        existing_monthly_debt,
        principal,
        annual_rate,
        tenure_months,
        credit_score,
        annual_cash_available,
        existing_annual_debt_service,
        collateral_value,
        round(monthly_emi, 2),
        round(dti, 4),
        round(dscr, 3),
        round(pd, 4),
        round(lgd, 4),
        round(ecl, 2),
        risk_grade,
    ])

# Export the dataset.
output_file = output_dir / "synthetic_borrowers.csv"

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)
