-- SQL Server (T-SQL). Import data/synthetic_borrowers.csv as dbo.Borrowers.
-- Rates and probabilities are decimals (e.g., 0.05 = 5%).
-- Synthetic data and illustrative assumptions; not a validated credit model.

-- 1. Portfolio
SELECT COUNT(*) AS Borrowers, SUM(Loan_Amount_INR) AS Total_Exposure_INR,
       SUM(One_Year_ECL_INR) AS Total_One_Year_ECL_INR,
       SUM(One_Year_ECL_INR)/NULLIF(SUM(Loan_Amount_INR),0) AS ECL_Rate
FROM dbo.Borrowers;

-- 2. Exposure, loss and credit score by risk grade
SELECT Risk_Grade, COUNT(*) AS Borrowers,
       SUM(Loan_Amount_INR) AS Exposure_INR,
       AVG(CAST(Credit_Score AS FLOAT)) AS Average_Credit_Score,
       SUM(One_Year_ECL_INR) AS Expected_Loss_INR
FROM dbo.Borrowers
GROUP BY Risk_Grade
ORDER BY CASE Risk_Grade WHEN 'High' THEN 1 WHEN 'Moderate' THEN 2 ELSE 3 END;

-- 3. Borrowers for manual review
SELECT Borrower_ID, Credit_Score, Loan_Amount_INR, Post_Loan_DTI, DSCR, Assumed_PD,
       One_Year_ECL_INR
FROM dbo.Borrowers
WHERE DSCR < 1.20 OR Post_Loan_DTI > 0.50
ORDER BY One_Year_ECL_INR DESC;

-- 4. Credit score segmentation with CTE and window function
WITH Segments AS (
 SELECT CASE WHEN Credit_Score < 650 THEN 'Below 650'
             WHEN Credit_Score < 750 THEN '650-749' ELSE '750+' END AS Score_Band,
        Loan_Amount_INR, One_Year_ECL_INR
 FROM dbo.Borrowers
), Totals AS (
 SELECT Score_Band, COUNT(*) AS Borrowers, SUM(Loan_Amount_INR) AS Exposure_INR,
        SUM(One_Year_ECL_INR) AS ECL_INR FROM Segments GROUP BY Score_Band
)
SELECT *, CAST(Exposure_INR*1.0/NULLIF(SUM(Exposure_INR) OVER(),0) AS DECIMAL(10,4)) AS Exposure_Share
FROM Totals ORDER BY Score_Band;

-- 5. Data quality checks (should return zero rows)
SELECT * FROM dbo.Borrowers
WHERE Annual_Income_INR <= 0 OR Loan_Amount_INR <= 0 OR Tenure_Months <= 0
   OR Assumed_PD NOT BETWEEN 0 AND 1 OR Assumed_LGD NOT BETWEEN 0 AND 1
   OR Borrower_ID IS NULL;
