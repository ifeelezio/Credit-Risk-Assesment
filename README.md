# Credit Risk Assessment & Financial Modelling

**A reproducible portfolio case study using Microsoft Excel, SQL Server, and Python**

Assessing repayment capacity, segmenting borrower risk, and estimating illustrative credit losses across **500 synthetic borrowers**.

[Portfolio snapshot](#portfolio-snapshot) · [Getting started](#getting-started) · [Methodology](#methodology) · [Stress testing](#stress-testing)

---

## Project overview

This project combines a formula-driven Excel model with SQL analysis to evaluate borrower repayment capacity and portfolio-level credit risk. It uses debt-to-income and debt-service coverage ratios alongside illustrative probability of default (PD), loss given default (LGD), and one-year expected credit loss (ECL).

The case study demonstrates analytical skills relevant to entry-level credit risk roles and provides a foundation for further work in structured finance.

> **Model scope:** All borrower data are synthetic. PD and LGD are based on illustrative rules, not observed defaults or recoveries. This is an educational portfolio project, not a validated underwriting, regulatory capital, or IFRS 9 impairment model.

## Portfolio snapshot

| Borrowers | Principal exposure | Illustrative one-year ECL | ECL / exposure |
| :---: | ---: | ---: | ---: |
| **500** | **INR 435,060,000** | **INR 8,977,559** | **2.06%** |

### Borrower risk distribution

| Risk grade | Borrowers | Share of borrowers |
| --- | ---: | ---: |
| Low | 103 | 20.6% |
| Moderate | 175 | 35.0% |
| High | 222 | 44.4% |
| **Total** | **500** | **100.0%** |

Risk grades reflect the project's assumed PD and repayment-capacity thresholds; they are not external credit ratings.

## Analysis included

- **Repayment capacity:** Monthly loan payments, post-loan debt-to-income (DTI), and debt-service coverage ratio (DSCR).
- **Risk segmentation:** Borrower grouping by risk grade and credit-score band.
- **Loss estimation:** Borrower-level and aggregate illustrative one-year ECL.
- **Portfolio monitoring:** Exposure concentration, manual-review flags, and data quality checks.
- **Scenario analysis:** Base, adverse, and severe assumptions for PD and LGD.

## Repository structure

| File | Purpose |
| --- | --- |
| [`data/synthetic_borrowers.csv`](data/synthetic_borrowers.csv) | Synthetic dataset containing 500 borrowers |
| [`sql/credit_risk_analysis.sql`](sql/credit_risk_analysis.sql) | T-SQL queries for portfolio analysis and data quality checks |
| [`models/Credit_Risk_Financial_Model.xlsx`](models/Credit_Risk_Financial_Model.xlsx) | Formula-driven Excel model, dashboard, and stress scenarios |
| [`reports/Credit_Risk_Report.pdf`](reports/Credit_Risk_Report.pdf) | Project findings, interpretation, and limitations |
| [`src/generate_data.py`](src/generate_data.py) | Deterministic Python dataset generator |
| [`README.md`](README.md) | Setup instructions, methodology, and assumptions |

## Getting started

### 1. Explore the Excel model

Open `models/Credit_Risk_Financial_Model.xlsx` in desktop Microsoft Excel and allow the formulas to calculate. Review these worksheets:

| Worksheet | Focus |
| --- | --- |
| **Dashboard** | Portfolio metrics and risk distribution |
| **Borrower Model** | Individual borrower inputs and calculations |
| **Stress Testing** | Scenario-based changes in illustrative losses |
| **Methodology** | Definitions, assumptions, and model limitations |

### 2. Run the SQL analysis

Import `data/synthetic_borrowers.csv` into SQL Server as **`dbo.Borrowers`**. Preserve the CSV headers as column names and use appropriate numeric types for amounts, ratios, rates, and probabilities.

Run `sql/credit_risk_analysis.sql` in SQL Server Management Studio (SSMS) to review portfolio totals, risk-grade summaries, manual-review candidates, credit-score segments, and data quality checks.

### 3. Regenerate the dataset

From the repository root, run:

```bash
python src/generate_data.py
```

The generator uses the fixed random seed **`20261102`**. The prebuilt Excel model references the same deterministic 500-borrower dataset. If you change the generator logic or borrower count, regenerate the workbook separately to keep the outputs aligned.

### 4. Review the findings

Read `reports/Credit_Risk_Report.pdf` for the project summary, interpretation, and limitations.

## Methodology

Rates and probabilities are stored as decimals: **`0.05` represents `5%`**. Monetary values are in **Indian rupees (INR)**.

### Core calculations

| Measure | Definition |
| --- | --- |
| **Monthly EMI** | Fixed-rate monthly payment. In Excel, `=-PMT(annual_rate / 12, tenure_months, loan_amount)` returns a positive payment for a positive loan amount. |
| **Post-loan DTI** | `(existing monthly debt payments + new EMI) / (annual income / 12)` |
| **DSCR** | `annual cash available / (existing annual debt service + 12 × new EMI)` |
| **Assumed PD** | Bounded illustrative heuristic based on credit score and post-loan DTI; not calibrated to observed defaults. |
| **Assumed LGD** | Bounded illustrative collateral proxy; not calibrated to observed recoveries. |
| **One-year ECL** | `loan amount × assumed PD × assumed LGD`, using loan amount as a proxy for exposure at default (EAD). |

### Risk grading rules

Rules are applied in the following order:

| Grade | Classification rule |
| --- | --- |
| **High** | PD ≥ 9% **or** DSCR < 1.00 |
| **Moderate** | If not High: PD ≥ 4.5% **or** DSCR < 1.25 |
| **Low** | All remaining borrowers |

These thresholds are project assumptions, not lending policy. The SQL manual-review filter is separate: it flags borrowers with **DSCR < 1.20 or post-loan DTI > 50%**.

## Stress testing

Scenarios apply multipliers to each borrower's baseline PD and LGD, with each stressed parameter capped at **100%**.

| Scenario | PD multiplier | LGD multiplier |
| --- | ---: | ---: |
| **Base** | 1.00× | 1.00× |
| **Adverse** | 1.75× | 1.20× |
| **Severe** | 2.75× | 1.50× |

The scenarios illustrate loss sensitivity to assumed credit deterioration; they are not forecasts of economic conditions or realised losses.

## Interpretation and limitations

The analysis illustrates how borrower characteristics and debt-service coverage can support risk segmentation and portfolio monitoring. Results depend on the synthetic data and the chosen assumptions.

- PD and LGD are heuristic inputs rather than empirically validated estimates.
- ECL uses loan principal as an EAD proxy and excludes amortisation, cash-flow timing, discounting, and multi-period credit migration.
- The project does not model securitisation cash-flow waterfalls or tranche-level risk.
- Outputs should not be used for loan approvals, estimates of actual default probabilities, or securities pricing.

## Potential extensions

- **PD calibration:** Use a labelled, appropriately licensed dataset to develop and validate a default model.
- **Performance analysis:** Add vintage delinquency, recovery analysis, and out-of-time validation.
- **Structured finance:** Model asset-backed security (ABS) cash-flow waterfalls and senior/junior tranche loss allocation.

## License

Released under the **MIT License**. See [`LICENSE`](LICENSE) for details.

The dataset is entirely synthetic and contains no personal customer information.
