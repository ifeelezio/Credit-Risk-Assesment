# Credit Risk Assessment & Financial Modelling

**Portfolio project | Microsoft Excel + SQL Server | Synthetic data**

A reproducible credit risk case study assessing 500 simulated borrowers using repayment capacity, borrower segmentation, illustrative probability of default (PD), loss given default (LGD), and one-year expected credit loss (ECL). Designed to demonstrate analytical skills relevant to entry-level credit risk and structured finance roles.

> **Important:** All borrower data and PD/LGD rules are synthetic and heuristic. This is not a validated underwriting, regulatory capital, or IFRS 9 impairment model.

## Portfolio snapshot (generated seed: 20261102)

| Metric | Value |
|---|---:|
| Borrowers | 500 |
| Principal exposure | INR 435,060,000 |
| Illustrative one-year ECL | INR 8,977,559 |
| ECL / exposure | 2.06% |
| Low / Moderate / High grades | 103 / 175 / 222 |

## Repository structure

```text
data/synthetic_borrowers.csv          Synthetic portfolio (500 borrowers)
sql/credit_risk_analysis.sql          SQL Server portfolio queries
models/Credit_Risk_Financial_Model.xlsx  Formula-driven Excel model and scenarios
reports/Credit_Risk_Report.pdf        Credit-risk findings and limitations
src/generate_data.py                 Deterministic Python data generation
README.md                            Setup, methods, and caveats
```

## Quick start

1. Open `models/Credit_Risk_Financial_Model.xlsx` in desktop Excel; allow formulas to calculate. Review **Dashboard**, **Borrower Model**, **Stress Testing**, and **Methodology**.
2. For SQL analysis, import `data/synthetic_borrowers.csv` into a SQL Server table named `dbo.Borrowers`, keeping the CSV headers as column names and using numeric types for numeric fields. Run `sql/credit_risk_analysis.sql` in SSMS.
3. To regenerate the synthetic dataset, run `python src/generate_data.py` from the repository root. The prebuilt Excel model references the same deterministic 500 borrowers; regenerate the workbook separately if you alter generator logic or row count.
4. Read `reports/Credit_Risk_Report.pdf` for the project summary and limitations.

## Formulas and definitions

- **EMI:** fixed-rate monthly loan payment using `PMT(annual_rate/12, months, principal)`.
- **Post-loan DTI:** (existing monthly debt payments + new EMI) / (annual income / 12).
- **DSCR:** annual cash available for debt service / (existing annual debt service + 12 x new EMI).
- **PD:** bounded illustrative score/DTI heuristic; not fitted to observed defaults.
- **LGD:** bounded illustrative collateral proxy; not fitted to observed recoveries.
- **One-year ECL:** loan amount (EAD proxy) x PD x LGD. Ignores amortization, timing, discounting and multi-period migration.
- **Risk grade:** High if PD >= 9% or DSCR < 1; Moderate if PD >= 4.5% or DSCR < 1.25; otherwise Low. Thresholds are project assumptions, not lending policy.
- **Stress scenarios:** Base (PD 1x, LGD 1x), Adverse (PD 1.75x, LGD 1.2x), Severe (PD 2.75x, LGD 1.5x), with parameters capped at 100%.

## Interpretation

This project demonstrates how borrower characteristics and debt-service coverage can support risk segmentation and portfolio monitoring. The model should not be used to approve loans, estimate actual default probabilities, or price securities.

## Suggested extensions

- Replace heuristic PD with a calibrated model using a labeled, appropriately licensed dataset.
- Add vintage delinquency, recovery analysis and out-of-time validation.
- Model ABS cash-flow waterfalls and senior/junior tranche loss allocation for structured finance relevance.

## License

MIT (see `LICENSE`). Synthetic data only; no personal customer information.
