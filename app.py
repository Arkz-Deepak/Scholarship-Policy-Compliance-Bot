import streamlit as st
import pandas as pd
from data_loader import load_data
from rules_engine import check_eligibility
from fraud_guard import run_fraud_detection

st.set_page_config(page_title="Scholarship Compliance Bot", layout="wide", page_icon="⚖️")

# --- LOAD DATA ---
students, scholarships, institutions, dual_benefit, fraud_rules = load_data()

if students is None:
    st.error("Data files not found! Please check data_loader.py")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Admin Console")
    st.info("System Status: Online")
    
    # Select Student
    student_list = students['student_id'].astype(str) + " - " + students['name']
    selected_student_str = st.selectbox("Select Applicant", student_list)
    selected_student_id = selected_student_str.split(" - ")[0]
    
    # Simulate: What scholarships do they ALREADY have?
    st.subheader("Simulate Student State")
    current_awards = st.multiselect(
        "Already Holding (for Dual Benefit Test)", 
        scholarships['scholarship_id'].tolist()
    )

# --- MAIN PAGE ---
st.title("🛡️ Scholarship Policy Compliance Bot")
st.markdown("Automated validation of eligibility, dual-benefit rules, and fraud detection.")
st.divider()

# Get Objects
student_row = students[students['student_id'] == selected_student_id].iloc[0]
institution_row = institutions[institutions['institution_id'] == student_row['institution_id']].iloc[0]

# Display Student Profile
col1, col2, col3, col4 = st.columns(4)
col1.metric("Student Name", student_row['name'])
col2.metric("Category", student_row['category'])
col3.metric("CGPA", student_row['cgpa'])
col4.metric("Income", f"₹{student_row['annual_income']:,}")

st.divider()

# Select Target Scholarship
st.subheader("New Application Processing")
target_sch_id = st.selectbox("Select Scholarship to Apply For", scholarships['scholarship_id'] + " - " + scholarships['scholarship_name'])
target_sch_id = target_sch_id.split(" - ")[0]
target_sch_row = scholarships[scholarships['scholarship_id'] == target_sch_id].iloc[0]

# --- ACTION BUTTON ---
if st.button("RUN COMPLIANCE CHECK", type="primary"):
    
    # 1. Deterministic Rule Check
    status, logs = check_eligibility(
        student_row, 
        target_sch_row, 
        institution_row, 
        dual_benefit, 
        current_awards, 
        scholarships
    )
    
    # 2. Display Results
    if status == "APPROVED":
        st.success(f"✅ APPLICATION APPROVED for {target_sch_id}")
        st.write("All eligibility and policy rules passed.")
    else:
        st.error(f"❌ APPLICATION REJECTED")
        st.write("### Violation Log (Explainable AI)")
        for log in logs:
            st.warning(log)
            
    # 3. AI Fraud Check (Bonus)
    st.divider()
    st.subheader("🕵️ Anomaly & Fraud Detection")
    
    # Run AI on the whole batch to find context
    analyzed_students = run_fraud_detection(students.copy())
    student_risk = analyzed_students[analyzed_students['student_id'] == selected_student_id].iloc[0]
    
    if student_risk['risk_status'] == 'HIGH RISK':
        st.error(f"⚠️ HIGH FRAUD RISK DETECTED (Anomaly Score: -1)")
        st.write("Reason: This student's Income/CGPA pattern is statistically unusual compared to peers.")
        st.caption("Algorithm: Isolation Forest (Unsupervised Learning)")
    else:
        st.success("✅ Fraud Risk: LOW (Normal Pattern)")

# Show Data Tables (For Audit)
with st.expander("View Underlying Data (Audit)"):
    st.write("Student Record:", student_row)
    st.write("Institution Record:", institution_row)