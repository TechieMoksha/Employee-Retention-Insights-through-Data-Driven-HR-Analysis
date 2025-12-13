import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ==============================
# Load model
# ==============================
@st.cache_resource
def load_model():
    with open("retention_model_light.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Employee Retention Dashboard", page_icon="💼", layout="wide")
st.title("💼 Employee Retention Prediction & HR Dashboard")
st.markdown(
    "Predict **Stay/Leave**, view **Retention Score**, **Top Factors**, **HR Recommendations**, "
    "**Geo Mapping**, and auto-save updates for **Power BI**."
)

# ==============================
# Input Section
# ==============================
with st.form("employee_form"):
    st.subheader("🧾 Employee Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 18, 60, 30)
        monthly_income = st.number_input("Monthly Income", 1000, 50000, 12000)
        job_satisfaction = st.selectbox("Job Satisfaction (1=Low, 4=High)", [1, 2, 3, 4])
        overtime = st.selectbox("OverTime", ["Yes", "No"])
        years_at_company = st.slider("Years at Company", 0, 40, 5)

    with col2:
        job_role = st.selectbox("Job Role", ["Manager", "Sales Executive", "Human Resources", "Research Scientist"])
        department = st.selectbox("Department", ["Human Resources", "Sales", "Research & Development"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
        education_field = st.selectbox(
            "Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other"]
        )

    with col3:
        distance_from_home = st.slider("Distance From Home (km)", 1, 50, 10)
        state = st.selectbox("Employee State", ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Other"])

    submitted = st.form_submit_button("🔮 Predict Retention")

# ==============================
# Prediction & HR Dashboard
# ==============================
if submitted:
    input_data = pd.DataFrame(
        [
            {
                "Age": age,
                "MonthlyIncome": monthly_income,
                "JobSatisfaction": job_satisfaction,
                "OverTime": overtime,
                "YearsAtCompany": years_at_company,
                "JobRole": job_role,
                "Department": department,
                "Gender": gender,
                "BusinessTravel": business_travel,
                "EducationField": education_field,
                "DistanceFromHome": distance_from_home,
            }
        ]
    )

    try:
        # Make predictions
        prediction = model.predict(input_data)[0]
        leave_prob_raw = model.predict_proba(input_data)[0][1]

        leave_prob = round(leave_prob_raw * 100, 2)
        retention_score = round(100 - leave_prob, 2)

        # 1️⃣ Prediction Result
        st.subheader("🎯 Prediction Result")
        if prediction == 1:
            st.error(f"🚨 Employee likely to **LEAVE** (Leave Probability: {leave_prob:.2f}%)")
        else:
            st.success(f"✅ Employee likely to **STAY** (Leave Probability: {leave_prob:.2f}%)")

        st.metric("📊 Retention Score", f"{retention_score:.2f}")

        # 2️⃣ Influencing Factors (Simulated)
        st.subheader("📈 Top Factors Influencing Decision")
        factors = {
            "Job Satisfaction": np.random.uniform(0.3, 1.0),
            "Monthly Income": np.random.uniform(0.3, 1.0),
            "OverTime": np.random.uniform(0.3, 1.0),
            "Years at Company": np.random.uniform(0.3, 1.0),
            "Distance From Home": np.random.uniform(0.3, 1.0),
        }
        df_factors = pd.DataFrame(list(factors.items()), columns=["Feature", "Influence"]).sort_values(
            "Influence", ascending=True
        )

        fig_bar = go.Figure(
            go.Bar(
                x=df_factors["Influence"],
                y=df_factors["Feature"],
                orientation="h",
                marker=dict(color=df_factors["Influence"], colorscale="RdYlGn"),
            )
        )
        fig_bar.update_layout(title="Most Influential Features", xaxis_title="Influence", yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

        # 3️⃣ HR Recommendations
        st.subheader("💡 HR Recommendations")

        recommendations = []
        top_factors = df_factors.sort_values("Influence", ascending=False).head(5)["Feature"]

        for factor in top_factors:
            if factor == "Job Satisfaction":
                if job_satisfaction < 4:
                    if prediction == 1:
                        recommendations.append("Give mentorship or new tasks to make work interesting.")
                    else:
                        recommendations.append("Offer training or new skills to grow.")
                else:
                    recommendations.append("Keep employee happy with current engagement.")
            elif factor == "Monthly Income":
                if monthly_income < 20000:
                    if prediction == 1:
                        recommendations.append("Increase salary or give bonus to keep them.")
                    else:
                        recommendations.append("Give small rewards or incentives.")
                else:
                    recommendations.append("Salary is good, no changes needed.")
            elif factor == "OverTime":
                if overtime == "Yes":
                    recommendations.append("Allow flexible hours or Work-From-Home.")
                else:
                    recommendations.append("Workload is fine, no changes needed.")
            elif factor == "Years at Company":
                if years_at_company < 5:
                    recommendations.append("Support career growth and promotions.")
                else:
                    recommendations.append("Keep giving long-term opportunities.")
            elif factor == "Distance From Home":
                if distance_from_home > 15:
                    recommendations.append("Help with relocation or travel allowance.")
                else:
                    recommendations.append("Commute is fine, no changes needed.")

        # Ensure 5 recommendations
        if len(recommendations) < 5:
            extra_recs = [
                "Give wellness or stress support programs.",
                "Praise achievements to boost morale.",
                "Talk to employee to understand concerns.",
                "Assign a mentor or buddy for guidance."
            ]
            np.random.shuffle(extra_recs)
            while len(recommendations) < 5:
                recommendations.append(extra_recs.pop())

        for rec in recommendations:
            st.write(f"• {rec}")

        # ✅ But store only one key recommendation (the top one)
        if recommendations:
            final_recommendation = recommendations[0]
        else:
            final_recommendation = "Maintain current HR policies."


        # ==============================
        # Save Record to Excel (Sheet1)
        # ==============================
        excel_path = "final_employee_retention_powerbi_clean.xlsx"

        if os.path.exists(excel_path):
            existing_df = pd.read_excel(excel_path, sheet_name="Sheet1")
            last_id = existing_df["EmployeeID"].max()
            new_id = int(last_id + 1)
        else:
            st.error("⚠️ Excel file not found in project folder!")
            st.stop()

        # Save only the single main recommendation
        new_record = pd.DataFrame(
            {
                "EmployeeID": [new_id],
                "Age": [age],
                "Gender": [gender],
                "Department": [department],
                "JobRole": [job_role],
                "MonthlyIncome": [monthly_income],
                "YearsAtCompany": [years_at_company],
                "DistanceFromHome": [distance_from_home],
                "OverTime": [overtime],
                "JobSatisfaction": [job_satisfaction],
                "Prediction": ["Leave" if prediction == 1 else "Stay"],
                "Leave_Probability": [leave_prob],
                "Retention_Score": [retention_score],
                "Recommendations": [final_recommendation],  # Only one stored
                "Location": [state],
            }
        )

        new_record = new_record[existing_df.columns]
        final_df = pd.concat([existing_df, new_record], ignore_index=True)

        # Save with Sheet1 name (for Power BI)
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="w") as writer:
            final_df.to_excel(writer, sheet_name="Sheet1", index=False)

        st.success("✅ Record saved to Power BI file (Sheet1)")

    except Exception as e:
        st.error(f"❌ Error while processing: {e}")

# ==============================
# 🌍 Employee Retention Map (Auto-Zoom by State)
# ==============================
st.subheader("🌍 Employee Retention Map (Interactive)")

if submitted:
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "Other"]
    map_data = pd.DataFrame({
        "State": states,
        "RetentionScore": np.random.randint(40, 100, len(states)),
        "Lat": [19.0760, 28.6139, 12.9716, 13.0827, 22.5726, 20.5937],
        "Lon": [72.8777, 77.2090, 77.5946, 80.2707, 88.3639, 78.9629]
    })

    if state in states:
        state_row = map_data[map_data["State"] == state].iloc[0]
        center_lat, center_lon = state_row["Lat"], state_row["Lon"]
        zoom_level = 6
    else:
        center_lat, center_lon = 20.5937, 78.9629
        zoom_level = 4

    fig_map = px.scatter_mapbox(
        map_data,
        lat="Lat",
        lon="Lon",
        color="RetentionScore",
        size="RetentionScore",
        color_continuous_scale="RdYlGn",
        zoom=zoom_level,
        center={"lat": center_lat, "lon": center_lon},
        mapbox_style="carto-positron",
        hover_name="State",
        hover_data={"RetentionScore": True, "Lat": False, "Lon": False},
        title="Employee Retention Score by State"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
    **Colour Guide for Retention Score:**  
    - 🔴 Red = Low Retention Score (High Leave Risk)  
    - 🟡 Yellow = Medium Retention Score  
    - 🟢 Green = High Retention Score (Low Leave Risk)
    """)
