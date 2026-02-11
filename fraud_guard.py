import pandas as pd
from sklearn.ensemble import IsolationForest

def run_fraud_detection(students_df):
    # 1. Select numeric features for AI analysis
    # We use Income and GPA to find statistical outliers
    features = students_df[['annual_income', 'cgpa']].fillna(0)
    
    # 2. Initialize the AI Model (Isolation Forest)
    # contamination=0.1 means we expect roughly 10% anomalies
    model = IsolationForest(contamination=0.1, random_state=42)
    
    # 3. Predict Anomalies
    # Returns -1 for Outliers, 1 for Normal
    students_df['anomaly_score'] = model.fit_predict(features)
    
    # 4. Convert to readable status
    students_df['risk_status'] = students_df['anomaly_score'].apply(lambda x: 'HIGH RISK' if x == -1 else 'Normal')
    
    return students_df