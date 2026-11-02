import csv,random,math,os,statistics,zipfile
from collections import defaultdict
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from artifact_tool import Workbook,SpreadsheetFile
root='.';random.seed(20261102)
rows=[]
for i in range(1,501):
 score=random.randint(540,835);income=random.randrange(360000,2400001,12000);principal=random.randrange(100000,1600001,10000);rate=round(random.uniform(.085,.185),4);months=random.choice([24,36,48,60,72]);existing=round(income/12*random.uniform(.05,.36),2);cash=round(income*random.uniform(.32,.65),2);existing_service=round(existing*12,2);collateral=round(principal*random.uniform(.65,1.4),2)
 monthly=principal*(rate/12)*(1+rate/12)**months/((1+rate/12)**months-1);dti=(existing+monthly)/(income/12);dscr=cash/(existing_service+monthly*12)
 pd=min(.40,max(.008,.035+(700-score)*.00032+max(dti-.4,0)*.15));lgd=max(.15,min(.85,1-.70*collateral/principal));ecl=principal*pd*lgd
 grade='High' if pd>=.09 or dscr<1 else 'Moderate' if pd>=.045 or dscr<1.25 else 'Low'
 rows.append([f'B{i:04}',income,existing,principal,rate,months,score,cash,existing_service,collateral,round(monthly,2),round(dti,4),round(dscr,3),round(pd,4),round(lgd,4),round(ecl,2),grade])
headers=['Borrower_ID','Annual_Income_INR','Existing_Monthly_Debt_INR','Loan_Amount_INR','Annual_Interest_Rate','Tenure_Months','Credit_Score','Annual_Cash_Available_INR','Existing_Annual_Debt_Service_INR','Collateral_Value_INR','New_Loan_EMI_INR','Post_Loan_DTI','DSCR','Assumed_PD','Assumed_LGD','One_Year_ECL_INR','Risk_Grade']
with open(root+'/data/synthetic_borrowers.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(headers);w.writerows(rows)
