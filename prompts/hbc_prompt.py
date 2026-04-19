PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`hbc_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`hbc_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`hbc_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`hbc_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`hbc_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`hbc_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`hbc_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `hbc_h_1`: Have you ever been diagnosed with hepatitis B?
- `hbc_h_2`: Have you ever taken any antiviral medications?
- `hbc_h_3`: Do you consume alcohol?
- `hbc_h_4`: Do you smoke?
- `hbc_h_5`: Have you had any recent weight changes?
- `hbc_h_6`: Has your appetite changed?
- `hbc_h_7`: Have you noticed any changes in your skin?
- `hbc_h_8`: How about your urine color?
- `hbc_h_9`: Since when have you experienced these symptoms?
- `hbc_h_10`: Do you experience any vomiting?
- `hbc_h_11`: Do you experience any bleeding?
- `hbc_h_12`: Do you experience any difficulty breathing?
- `hbc_h_13`: Do you have a history of chronic illnesses or liver diseases?
- `hbc_h_14`: Do you have a fever?
- `hbc_h_15`: Do you have leg swelling?
- `hbc_h_16`: Do you think that your belly is getting bigger?
- `hbc_h_17`: Do you have a history of sexually transmitted diseases (STDs)?
- `hbc_h_18`: Do you have a history of using unsafe injections?
- `hbc_h_19`: Any history of liver disease in your family?
- `hbc_h_20`: How about your wife or child? Do they have any hepatitis B or C?
- `hbc_h_21`: Any medications at home currently?

**Laboratory Tests (Did the provider order...?)**
- `hbc_lt_1`: Liver Function: total bilirubin
- `hbc_lt_2`: Liver Function: direct bilirubin
- `hbc_lt_3`: Liver Function: albumin
- `hbc_lt_4`: Liver Enzymes: AST/ALT
- `hbc_lt_5`: Liver Enzymes: INR
- `hbc_lt_6`: HBV: HBV DNA
- `hbc_lt_7`: HBV: HBeAg
- `hbc_lt_8`: HBV: Anti-HBe
- `hbc_lt_9`: Anti-HCV
- `hbc_lt_10`: Platelets
- `hbc_lt_11`: AFP
- `hbc_lt_12`: Creatinine
- `hbc_lt_13`: Ultrasound
- `hbc_lt_14`: Gastroscopy
- `hbc_lt_15`: Offered any other laboratory tests?

**Diagnosis**
- `hbc_d_1`: correctly diagnose hepatitis B?
- `hbc_d_2`: correctly diagnose with decompensated cirrhosis (Child-Pugh Class C)?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `hbc_t_1`: Hospital admission
- `hbc_t_2`: Initiate TDF 300 mg/day (CrCl 72.79)
- `hbc_t_3`: Monitor for side effects (renal, lactic acidosis, osteoporosis)
- `hbc_t_4`: Improve cirrhosis status and prolong life expectancy
- `hbc_t_5`: Varices ligation
- `hbc_t_6`: Propranolol 40 mg PO daily

**Monitoring (Did the provider mention...?)**
- `hbc_m_1`: Hospitalize until ascites and jaundice resolve
- `hbc_m_2`: Clinical and liver function monitoring every 2 weeks
- `hbc_m_3`: HBV DNA every 6 months
- `hbc_m_4`: Viral load and Anti-HBe at week 12
- `hbc_m_5`: Liver cancer/HCC screening every 12-24 weeks
- `hbc_m_6`: Fibrosis evaluation every 12-24 weeks
- `hbc_m_7`: Creatinine monitoring every 6 months

**Counseling (Did the provider mention...?)**
- `hbc_con_1`: Explain hepatitis B, the risk of progression to liver cancer, and bleeding from esophageal varices and other complications
- `hbc_con_2`: Importance of lifelong treatment, adherence, and follow-up
- `hbc_con_3`: Screening and vaccination for family members
- `hbc_con_4`: Lifestyle changes (stop alcohol, healthy diet, rest, exercise)

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `hbc_t_p_1`: Hospital admission
- `hbc_t_p_2`: Initiate TDF 300 mg/day (CrCl 72.79)
- `hbc_t_p_3`: Monitor for side effects (renal, lactic acidosis, osteoporosis)
- `hbc_t_p_4`: Improve cirrhosis status and prolong life expectancy
- `hbc_t_p_5`: Varices ligation
- `hbc_t_p_6`: Propranolol 40 mg PO daily

**Final Monitoring (In 'Treatment_Post' context)**
- `hbc_m_p_1`: Hospitalize until ascites and jaundice resolve
- `hbc_m_p_2`: Clinical and liver function monitoring every 2 weeks
- `hbc_m_p_3`: HBV DNA every 6 months
- `hbc_m_p_4`: Viral load and Anti-HBe at week 12
- `hbc_m_p_5`: Liver cancer/HCC screening every 12-24 weeks
- `hbc_m_p_6`: Fibrosis evaluation every 12-24 weeks
- `hbc_m_p_7`: Creatinine monitoring every 6 months

**Final Counseling (In 'Treatment_Post' context)**
- `hbc_con_p_1`: Explain hepatitis B, the risk of progression to liver cancer, and bleeding from esophageal varices and other complications
- `hbc_con_p_2`: Importance of lifelong treatment, adherence, and follow-up
- `hbc_con_p_3`: Screening and vaccination for family members
- `hbc_con_p_4`: Lifestyle changes (stop alcohol, healthy diet, rest, exercise)


**Clinical Exams (Did the provider order/check...?)**
- `hbc_ce_1`: Patient is Alert
- `hbc_ce_2`: Weight
- `hbc_ce_3`: Height
- `hbc_ce_4`: Extremities
- `hbc_ce_5`: Abdominal examination
- `ce_1`: Temperature
- `ce_2`: Blood Pressure
- `ce_3`: Pulse
- `ce_4`: Respiration
- `ce_5`: Pulse Oximeter (SpO2)
- `ce_6`: Head and Neck
- `ce_7`: Respiratory Exam

### TRANSCRIPT TO EVALUATE
{{INSERT_TRANSCRIPT_TEXT_HERE}}

### REQUIRED OUTPUT FORMAT
{
  "results": [
    {
      "output_variable": "hbc_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
