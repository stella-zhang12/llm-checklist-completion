PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`hcv_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`hcv_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`hcv_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`hcv_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`hcv_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`hcv_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`hcv_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `hcv_h_1`: How long have you been experiencing these symptoms?
- `hcv_h_2`: What symptoms have you noticed?
- `hcv_h_3`: Do you have shortness of breath?
- `hcv_h_4`: Do your skin or eyes become yellow?
- `hcv_h_5`: How about your urine color?
- `hcv_h_6`: Do you have leg swelling?
- `hcv_h_7`: Do you have a fever?
- `hcv_h_8`: Do you have any history of chronic illnesses or medications?
- `hcv_h_9`: Any history of blood transfusions or surgeries?
- `hcv_h_10`: Have you used traditional or herbal medicine for your current symptoms?
- `hcv_h_11`: Have your family members been tested with Hepatitis?
- `hcv_h_12`: Do you have any past history of liver disease?
- `hcv_h_13`: Did you get antiviral treatment?
- `hcv_h_14`: For your current condition, have you taken any previous laboratory tests?
- `hcv_h_15`: Have you been vaccinated against Hepatitis B?
- `hcv_h_16`: Do you have any family members who have liver disease?
- `hcv_h_17`: Do you drink alcohol or smoke?
- `hcv_h_18`: Do you know your hepatitis B status?
- `hcv_h_19`: Do you know your HIV status?
- `hcv_h_20`: Do you have a history of using unsafe injections?

**Laboratory Tests (Did the provider order...?)**
- `hcv_lt_1`: CBC: PLT
- `hcv_lt_2`: CBC: HGB
- `hcv_lt_3`: Hepatitis B: HBeAg
- `hcv_lt_4`: Hepatitis C: HCV RNA
- `hcv_lt_5`: Liver Enzyme: AST/ALT
- `hcv_lt_6`: Ultrasound
- `hcv_lt_7`: Bilirubin
- `hcv_lt_8`: Albumin
- `hcv_lt_9`: Hepatitis C: Anti-HCV
- `hcv_lt_10`: Hepatitis B: Anti-HBV
- `hcv_lt_11`: HIV
- `hcv_lt_12`: Offered any other laboratory tests?

**Diagnosis**
- `hcv_d_1`: correctly diagnose Chronic HCV?
- `hcv_d_2`: correctly diagnose advanced fibrosis (F3)?
- `hcv_d_3`: correctly diagnose without cirrhosis?
- `hcv_d_4`: correctly diagnose without co-infections?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `hcv_t_1`: Eligible for DAA therapy: SOF/VEL or SOF+DAC for 12 weeks

**Monitoring (Did the provider mention...?)**
- `hcv_m_1`: After 1 month: LFTs, CBC
- `hcv_m_2`: SVR12: HCV RNA, fibrosis, AFP, ultrasound, LFT, CBC
- `hcv_m_3`: Screen for HCC every 6 months after SVR 12 evaluation (as he has F3 fibrosis)

**Counseling (Did the provider mention...?)**
- `hcv_con_1`: Explain the disease, purpose, and benefits of treatment
- `hcv_con_2`: Importance of adherence and side effect awareness
- `hcv_con_3`: Prevent reinfection
- `hcv_con_4`: Screen spouse and child
- `hcv_con_5`: Importance of seeking health services earlier and awareness of utilizing unstandardized traditional medicine

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `hcv_t_p_1`: Eligible for DAA therapy: SOF/VEL or SOF+DAC for 12 weeks

**Final Monitoring (In 'Treatment_Post' context)**
- `hcv_m_p_1`: After 1 month: LFTs, CBC
- `hcv_m_p_2`: SVR12: HCV RNA, fibrosis, AFP, ultrasound, LFT, CBC
- `hcv_m_p_3`: Screen for HCC every 6 months after SVR 12 evaluation (as he has F3 fibrosis)

**Final Counseling (In 'Treatment_Post' context)**
- `hcv_con_p_1`: Explain the disease, purpose, and benefits of treatment
- `hcv_con_p_2`: Importance of adherence and side effect awareness
- `hcv_con_p_3`: Prevent reinfection
- `hcv_con_p_4`: Screen spouse and child
- `hcv_con_p_5`: Importance of seeking health services earlier and awareness of utilizing unstandardized traditional medicine


**Clinical Exams (Did the provider order/check...?)**
- `hcv_ce_1`: Patient is Alert
- `hcv_ce_2`: Extremities
- `hcv_ce_3`: Abdominal examination
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
      "output_variable": "hcv_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
