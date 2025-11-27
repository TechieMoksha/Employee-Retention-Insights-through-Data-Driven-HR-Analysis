A complete Employee Attrition Prediction & HR Insights project using Python, Machine Learning, Power BI, and Streamlit.
This system helps HR teams identify why employees leave and predicts who is at risk, giving data-driven recommendations.

🚀 Project Overview

This project performs end-to-end HR analytics using employee data. It includes:

Data cleaning

Exploratory analysis

ML model for attrition prediction

Streamlit dashboard for interactive insights

Power BI dashboard for business-level reporting

The goal is to help organizations improve employee satisfaction and retention strategy.

🏗️ Project Architecture
Raw Dataset 
   → Data Cleaning & Feature Engineering
   → EDA
   → ML Model Training & Evaluation
   → Model Export (model.pkl)
   → Streamlit Dashboard
   → Power BI Dashboard (Optional)

🛠️ Technologies Used
Languages & Libraries

Python

pandas, numpy

scikit-learn

matplotlib, seaborn

joblib

Dashboards

Streamlit

Power BI

Other Tools

Excel

GitHub

🎯 Features
🔹 Machine Learning

Predicts whether an employee is At Risk or Safe

Shows confidence score

Highlights top influencing factors

🔹 Streamlit Dashboard

Dataset overview

Interactive EDA charts

Live prediction system

Clean and user-friendly interface

🔹 Power BI Dashboard

Department-wise attrition

KPIs (overall attrition, retention rate)

Salary, age, overtime comparison

Filters for HR decision-making

⚙️ How This Project Works (Step-by-Step)

This is the exact way to run the project from your system.
1️⃣ Place All Files in One Folder

Create one main folder and put all project files together:
Employee-Retention-Analysis/
│
├── app.py
├── model.pkl
├── train_retention_fixed.py
├── final_dash.py
├── final_employee_retention_powerbi_clean.xlsx
├── EmployeeRetentionDashboard.pbix
├── requirements.txt
└── documentation/
This ensures Streamlit, datasets, and model load without errors.

2️⃣ Install Required Python Libraries
pip install pandas numpy scikit-learn matplotlib seaborn joblib streamlit openpyxl plotly


3️⃣ Run the Streamlit Dashboard

Use the command:

1. cd "YourFolderPath"
2. python -m streamlit run "YourFinalAppPath"

Streamlit will:

Start a local server

Open the dashboard in your browser

Load dataset + model + visualizations

You will see a fully working web app.

4️⃣ How the System Works Internally
✔️ (a) Loads Clean Dataset

final_employee_retention_powerbi_clean.xlsx
→ Used for charts, EDA, and Power BI

✔️ (b) Loads Trained Machine Learning Model

model.pkl
→ Predicts employee attrition

✔️ (c) Preprocessing Script

train_retention_fixed.py
→ Handles encoding, feature scaling, model preparation

✔️ (d) Visualization Script

final_dash.py
→ Generates charts like:

Attrition by department

Salary vs attrition

Work-life balance

Overtime analysis

✔️ (e) Streamlit Output

Based on user input, the app shows:

Attrition Prediction

Confidence Score

Key drivers (important features)

EDA graphs4️⃣ How the System Works Internally
✔️ (a) Loads Clean Dataset

final_employee_retention_powerbi_clean.xlsx
→ Used for charts, EDA, and Power BI

✔️ (b) Loads Trained Machine Learning Model

model.pkl
→ Predicts employee attrition

✔️ (c) Preprocessing Script

train_retention_fixed.py
→ Handles encoding, feature scaling, model preparation

✔️ (d) Visualization Script

final_dash.py
→ Generates charts like:

Attrition by department

Salary vs attrition

Work-life balance

Overtime analysis

✔️ (e) Streamlit Output

Based on user input, the app shows:

Attrition Prediction

Confidence Score

Key drivers (important features)

EDA graphs

Final Output You Will Get
✔️ A working Streamlit web app
✔️ Machine learning prediction system
✔️ Interactive EDA dashboard
✔️ Power BI business insights
✔️ Full documentation
✔️ Clean, structured GitHub repository

👥 Team Members

Mokshada Patil
Ajay Gaikwad 
Chinmayee Lokhande
Khushi Chaudhari

⭐ Support

If this project helped you, please give a ⭐ star on GitHub!
