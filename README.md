# 🛡️ Scholarship Policy Compliance Bot

> A Hybrid AI System for detecting scholarship fraud and enforcing dual-benefit policies in real-time.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red) ![Scikit-Learn](https://img.shields.io/badge/AI-IsolationForest-orange)

## 📸 Demo Dashboard

![Dashboard Screenshot](Screenshots/1.png)

## 📌 Problem Statement

Educational institutions face massive fund leakage due to:

1. **Dual Benefit Violations:** Students applying for conflicting scholarships (Double Dipping).
2. **Fraud:** Fake income certificates or data anomalies.
3. **Manual Errors:** Human verification is slow and error-prone.

## 💡 The Solution: Hybrid AI Architecture

We solved this using a two-layer approach, combining deterministic logic with machine learning.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Policy Engine** | Python (Pandas) | Enforces strict government rules (GPA cuts, Income caps, Mutual Exclusivity) with 100% accuracy. |
| **Fraud Guard** | Scikit-Learn | An **Isolation Forest** model (Unsupervised Learning) detects statistical anomalies in applicant data. |
| **Dashboard** | Streamlit | Real-time interface for administrators to validate applications. |

## 🚀 Features

* **Dynamic Rule Loading:** Reads policy rules from Excel/JSON, allowing updates without changing code.
* **Dual-Benefit Detection:** checks `dual_benefit_rules.xlsx` to prevent students from holding conflicting grants.
* **Anomaly Scoring:** Flags "High Risk" applications where Income/CGPA ratios deviate from the norm.
* **Explainable AI:** Provides exact reasons for rejection (e.g., "Rule DBR-001 Violation").

## 🛠️ Installation & Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/Arkz-Deepak/Scholarship-Policy-Compliance-Bot.git
   cd Scholarship-Policy-Compliance-Bot# 🛡️ Scholarship Policy Compliance Bot

2.**Install Dependencies**
    ```bash
    pip install pandas streamlit scikit-learn openpyxl
    ```

3.**Run the App**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```text
├── app.py                # Main Dashboard Interface
├── data_loader.py        # Dynamic Data Ingestion Script
├── rules_engine.py       # Deterministic Logic (The "Lawyer")
├── fraud_guard.py        # ML Model (The "Detective")
├── Scholarship dataset/  # Excel/JSON Data Sources
│   ├── students.xlsx
│   ├── scholarships.xlsx
│   ├── dual_benefit_rules.xlsx
│   └── fraud_rules.json
└── README.md             # Documentation
```
---
# 👥 Team Arkz
### Deepak R - AI Architect & Backend Logic

### Kamalesh - Frontend & Presentation
---
Built for the Build-a-Bot Hackathon 2026.
