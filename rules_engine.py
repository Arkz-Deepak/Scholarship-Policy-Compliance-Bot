import pandas as pd

def check_eligibility(student, target_scholarship, institution, dual_rules, currently_held_scholarships_ids, scholarships_db):
    logs = []
    status = "APPROVED"
    
    # --- 1. INSTITUTION VALIDATION ---
    # Check if the college is accredited
    if institution['accredited'].strip().lower() == 'no':
        status = "REJECTED"
        logs.append(f"❌ Institution '{institution['name']}' is not accredited.")

    # --- 2. ACADEMIC ELIGIBILITY ---
    # Check CGPA
    if student['cgpa'] < target_scholarship['min_cgpa']:
        status = "REJECTED"
        logs.append(f"❌ CGPA {student['cgpa']} is below requirement ({target_scholarship['min_cgpa']}).")

    # --- 3. FINANCIAL ELIGIBILITY ---
    # Check Income
    if student['annual_income'] > target_scholarship['max_income']:
        status = "REJECTED"
        logs.append(f"❌ Annual Income {student['annual_income']} exceeds limit ({target_scholarship['max_income']}).")

    # --- 4. CATEGORY & COURSE CHECK ---
    # Check Category (Split by comma)
    valid_categories = [c.strip() for c in str(target_scholarship['eligible_categories']).split(',')]
    if student['category'] not in valid_categories:
        status = "REJECTED"
        logs.append(f"❌ Student Category '{student['category']}' not in eligible list: {valid_categories}")

    # Check Course
    valid_courses = [c.strip() for c in str(target_scholarship['eligible_courses']).split(',')]
    if student['course'] not in valid_courses:
        status = "REJECTED"
        logs.append(f"❌ Course '{student['course']}' is not eligible for this grant.")

    # --- 5. DUAL BENEFIT LOGIC (The Hard Part) ---
    target_id = target_scholarship['scholarship_id']
    target_amount = target_scholarship['funding_amount']
    
    for held_id in currently_held_scholarships_ids:
        # Find the held scholarship details to get its amount
        held_sch = scholarships_db[scholarships_db['scholarship_id'] == held_id].iloc[0]
        held_amount = held_sch['funding_amount']
        
        # SEARCH RULES: Check if specific pair exists in rules DB
        # Look for (A=Target & B=Held) OR (A=Held & B=Target)
        rule_match = dual_rules[
            ((dual_rules['scholarship_a'] == target_id) & (dual_rules['scholarship_b'] == held_id)) |
            ((dual_rules['scholarship_b'] == target_id) & (dual_rules['scholarship_a'] == held_id))
        ]

        if not rule_match.empty:
            rule = rule_match.iloc[0]
            if rule['allowed'] == 'No':
                status = "REJECTED"
                logs.append(f"⛔ Dual Benefit Violation: Rule {rule['rule_id']} forbids combining {target_id} with {held_id}.")
            elif rule['allowed'] == 'Yes':
                # Check Combined Cap
                combined_total = target_amount + held_amount
                if combined_total > rule['max_combined_amount']:
                    status = "REJECTED"
                    logs.append(f"💰 Funding Cap Exceeded: Combined {combined_total} exceeds limit of {rule['max_combined_amount']}.")
        
        # CHECK EXCLUSIVE RULES (The "ANY" keyword)
        # Does the target scholarship forbid ANY other scholarship?
        exclusive_rule = dual_rules[
            (dual_rules['scholarship_a'] == target_id) & (dual_rules['scholarship_b'] == 'ANY')
        ]
        if not exclusive_rule.empty:
             status = "REJECTED"
             logs.append(f"⛔ Exclusivity Violation: {target_id} cannot be combined with ANY other scholarship.")

    return status, logs