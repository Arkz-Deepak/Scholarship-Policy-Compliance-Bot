import pandas as pd
import json
import os

def load_data():
    try:
        print("Loading datasets...")
        # Using the exact filenames from your screenshot
        students = pd.read_excel(r'Scholarship dataset\students.xlsx')
        scholarships = pd.read_excel(r'Scholarship dataset\scholarships.xlsx')
        institutions = pd.read_excel(r'Scholarship dataset\institutions.xlsx')
        dual_benefit = pd.read_excel(r'Scholarship dataset\dual_benefit_rules.xlsx')
        
        with open(r"Scholarship dataset\fraud_rules.json", 'r') as f:
            fraud_rules = json.load(f)

        print("🧹 Cleaning data types...")

        # Fix Students Table
        if 'student_id' in students.columns:
            students['student_id'] = students['student_id'].astype(str)
        if 'annual_income' in students.columns:
            students['annual_income'] = pd.to_numeric(students['annual_income'], errors='coerce').fillna(0)
        if 'cgpa' in students.columns:
            students['cgpa'] = pd.to_numeric(students['cgpa'], errors='coerce').fillna(0)

        # Fix Scholarships Table
        if 'scholarship_id' in scholarships.columns:
            scholarships['scholarship_id'] = scholarships['scholarship_id'].astype(str)
        if 'funding_amount' in scholarships.columns:
            scholarships['funding_amount'] = pd.to_numeric(scholarships['funding_amount'], errors='coerce').fillna(0)
            
        # Fix Institutions Table
        if 'institution_id' in institutions.columns:
            institutions['institution_id'] = institutions['institution_id'].astype(str)

        print("✅ Data loaded and cleaned successfully!")
        return students, scholarships, institutions, dual_benefit, fraud_rules
        
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file {e.filename}")
        return None, None, None, None, None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None, None, None, None, None