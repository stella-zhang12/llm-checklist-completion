PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`hbp_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`hbp_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`hbp_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`hbp_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`hbp_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`hbp_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`hbp_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `hbp_h_1`: When did you find out about hepatitis B?
- `hbp_h_2`: How do you know about your hepatitis B status?
- `hbp_h_3`: Besides HBsAg, are there other laboratory tests, such as liver enzymes or virus count, that you took before?
- `hbp_h_4`: Have you received any antiviral treatment?
- `hbp_h_5`: Do you experience any symptoms?
- `hbp_h_6`: Do you have any fatigue?
- `hbp_h_7`: Do you have a loss of appetite?
- `hbp_h_8`: Have you ever had yellow eyes or skin?
- `hbp_h_9`: Do you have any bleeding?
- `hbp_h_10`: Do you have other health conditions or medications?
- `hbp_h_11`: How about your current pregnancy condition?
- `hbp_h_12`: Is there anyone in your family who has liver disease?
- `hbp_h_13`: Has your family been tested for hepatitis before?
- `hbp_h_14`: How about the hepatitis B status of your husband and children?
- `hbp_h_15`: In your first pregnancy, did you get any viral tests or other health checks?
- `hbp_h_16`: Do you know your HIV status?
- `hbp_h_17`: Have you taken a syphilis test?
- `hbp_h_18`: Do you consume alcohol?
- `hbp_h_19`: Do you smoke?

**Laboratory Tests (Did the provider order...?)**
- `hbp_lt_1`: CBC: PLT
- `hbp_lt_2`: CBC: HGB
- `hbp_lt_3`: Hepatitis B: HBeAg
- `hbp_lt_4`: Hepatitis B: HBV DNA
- `hbp_lt_5`: Anti-HCV
- `hbp_lt_6`: HIV
- `hbp_lt_7`: Ultrasound
- `hbp_lt_8`: Liver Enzyme: AST/ALT
- `hbp_lt_9`: Offered any other laboratory tests?

**Diagnosis**
- `hbp_d_1`: correctly diagnose chronic hepatitis B?
- `hbp_d_2`: correctly diagnose without fibrosis?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `hbp_t_1`: Did the provider prescribe antiviral treatment?
- `hbp_t_2`: Did the provider prescribe prophylaxis?

**Monitoring (Did the provider mention...?)**
- `hbp_m_1`: Mother -- re-evaluate 3 months after delivery or earlier if symptoms occur
- `hbp_m_2`: Baby -- HBV vaccine and HBIG within 24 hours after birth
- `hbp_m_3`: Baby -- 3 HBV doses in Expanded Program on immunization (EPI)
- `hbp_m_4`: Baby -- HBsAg and anti-HBs from month 7

**Counseling (Did the provider mention...?)**
- `hbp_con_1`: Explain the current disease status and the need for monitoring
- `hbp_con_2`: Infant protection protocol
- `hbp_con_3`: Encourage family testing
- `hbp_con_4`: Breastfeeding is safe
- `hbp_con_5`: Choose to disclose status if desired

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `hbp_t_p_1`: Did the provider prescribe antiviral treatment?
- `hbp_t_p_2`: Did the provider prescribe prophylaxis?

**Final Monitoring (In 'Treatment_Post' context)**
- `hbp_m_p_1`: Mother -- re-evaluate 3 months after delivery or earlier if symptoms occur
- `hbp_m_p_2`: Baby -- HBV vaccine and HBIG within 24 hours after birth
- `hbp_m_p_3`: Baby -- 3 HBV doses in Expanded Program on immunization (EPI)
- `hbp_m_p_4`: Baby -- HBsAg and anti-HBs from month 7

**Final Counseling (In 'Treatment_Post' context)**
- `hbp_con_p_1`: Explain the current disease status and the need for monitoring
- `hbp_con_p_2`: Infant protection protocol
- `hbp_con_p_3`: Encourage family testing
- `hbp_con_p_4`: Breastfeeding is safe
- `hbp_con_p_5`: Choose to disclose status if desired


**Clinical Exams (Did the provider order/check...?)**
- `hbp_ce_1`: Patient is Alert
- `hbp_ce_2`: Extremities
- `hbp_ce_3`: Abdominal examination
- `hbp_ce_4`: Fetal Growth
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
      "output_variable": "hbp_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
