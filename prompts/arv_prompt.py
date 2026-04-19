PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. 
Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were 
taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`arv_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`arv_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`arv_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`arv_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`arv_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`arv_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`arv_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `arv_h_1`: Have you had any symptoms recently?
- `arv_h_2`: Since when have you experienced those symptoms?
- `arv_h_3`: Do you experience a fever?
- `arv_h_4`: Do you experience leg edema?
- `arv_h_5`: Do you experience bleeding?
- `arv_h_6`: How about your urine color?
- `arv_h_7`: How about your appetite?
- `arv_h_8`: Do you have diarrhea?
- `arv_h_9`: Do you have a chronic productive cough?
- `arv_h_10`: Since when have you been taking ARV treatment?
- `arv_h_11`: What regimen that you take?
- `arv_h_12`: Are you taking your HIV treatment regularly?
- `arv_h_13`: Do you have a history of liver disease?
- `arv_h_14`: Besides that, did you take other laboratory tests such as an HCV RNA test?
- `arv_h_15`: Did you take any antiviral or hepatitis medication?
- `arv_h_16`: Do you drink alcohol?
- `arv_h_17`: Do you have a history of using injection drugs?
- `arv_h_18`: Do you have any family members with a history of liver cancer or Hepatitis B, or C?
- `arv_h_19`: Have your family members been tested for hepatitis?

**Laboratory Tests (Did the provider order...?)**
- `arv_lt_1`: CBC: PLT
- `arv_lt_2`: CBC: HGB
- `arv_lt_3`: Hepatitis B: HBeAg
- `arv_lt_4`: Hepatitis B: HBV DNA
- `arv_lt_5`: Liver Enzyme: AST/ALT
- `arv_lt_6`: Liver Function: total bilirubin
- `arv_lt_7`: Liver Function: albumin
- `arv_lt_8`: CD4
- `arv_lt_9`: Creatinine
- `arv_lt_10`: HIV
- `arv_lt_11`: Ultrasound
- `arv_lt_12`: Hepatitis C: HCV RNA
- `arv_lt_13`: Offered any other laboratory tests?

**Diagnosis**
- `arv_d_1`: correctly diagnose Chronic viremic HCV infection, co-infected with HBV and HIV, compensated liver cirrhosis?
- `arv_d_2`: correctly diagnose Chronic viremic HCV infection?
- `arv_d_3`: correctly diagnose co-infected with HBV?
- `arv_d_4`: correctly diagnose co-infected with HIV?
- `arv_d_5`: correctly diagnose compensated liver cirrhosis?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `arv_t_1`: Continue ART (switch from TDF/3TC/EFV to TDF/3TC/DTG (TLD) regimen)
- `arv_t_2`: Begin SOF + DAC x 24 weeks

**Monitoring (Did the provider mention...?)**
- `arv_m_1`: 4-week follow-up: LFTs, CBC, creatinine
- `arv_m_2`: SVR12 testing after 12 weeks post-treatment
- `arv_m_3`: Continue HCC screening every 6 months

**Counseling (Did the provider mention...?)**
- `arv_con_1`: Explain the disease, purpose, and benefits of treatment
- `arv_con_2`: Importance of adherence to ARV and DAA
- `arv_con_3`: Monitor for interactions and side effects
- `arv_con_4`: Encourage partner and family testing
- `arv_con_5`: Emphasize a healthy lifestyle and prevention of reinfection

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `arv_t_p_1`: Continue ART (switch from TDF/3TC/EFV to TDF/3TC/DTG (TLD) regimen)
- `arv_t_p_2`: Begin SOF + DAC x 24 weeks

**Final Monitoring (In 'Treatment_Post' context)**
- `arv_m_p_1`: 4-week follow-up: LFTs, CBC, creatinine
- `arv_m_p_2`: SVR12 testing after 12 weeks post-treatment
- `arv_m_p_3`: Continue HCC screening every 6 months

**Final Counseling (In 'Treatment_Post' context)**
- `arv_con_p_1`: Explain the disease, purpose, and benefits of treatment
- `arv_con_p_2`: Importance of adherence to ARV and DAA
- `arv_con_p_3`: Monitor for interactions and side effects
- `arv_con_p_4`: Encourage partner and family testing
- `arv_con_p_5`: Emphasize a healthy lifestyle and prevention of reinfection


**Clinical Exams (Did the provider order/check...?)**
- `arv_ce_1`: Patient is Alert
- `arv_ce_2`: Extremities
- `arv_ce_3`: Abdominal examination
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
      "output_variable": "arv_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
