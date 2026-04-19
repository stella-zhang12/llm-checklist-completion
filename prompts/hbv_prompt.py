PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`hbv_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`hbv_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`hbv_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`hbv_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`hbv_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`hbv_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`hbv_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `hbv_h_1`: When did you find out about hepatitis B?
- `hbv_h_2`: How do you know about your hepatitis B status?
- `hbv_h_3`: Besides HBsAg, are there other laboratory tests that you took before?
- `hbv_h_4`: Have you received any antiviral treatment?
- `hbv_h_5`: Do you currently experience any symptoms?
- `hbv_h_6`: Do you have any fatigue?
- `hbv_h_7`: Do you have a loss of appetite?
- `hbv_h_8`: Do you have yellow eyes or skin?
- `hbv_h_9`: Do you have any bleeding?
- `hbv_h_10`: Do you have other health conditions?
- `hbv_h_11`: Is there anyone in your family who has liver disease?
- `hbv_h_12`: Has your family been tested for hepatitis before?
- `hbv_h_13`: Has your mother or anyone else in your family been diagnosed with HCC?
- `hbv_h_14`: How about the hepatitis B status of your wife and children?
- `hbv_h_15`: Do you know your HIV status?
- `hbv_h_16`: Do you know your HCV status?
- `hbv_h_17`: Are you taking any medications?
- `hbv_h_18`: Do you smoke or drink?
- `hbv_h_19`: Do you ever use any injection drugs?
- `hbv_h_20`: Do you have any history of sexually transmitted diseases (STDs)?
- `hbv_h_21`: Do you have a history of any risky behaviour?

**Laboratory Tests (Did the provider order...?)**
- `hbv_lt_1`: CBC: PLT
- `hbv_lt_2`: CBC: HGB
- `hbv_lt_3`: HBV: HBeAg
- `hbv_lt_4`: HBV: HBV DNA
- `hbv_lt_5`: Liver Enzyme: AST/ALT
- `hbv_lt_6`: Ultrasound
- `hbv_lt_7`: Offered any other laboratory tests?

**Diagnosis**
- `hbv_d_1`: correctly diagnose chronic hepatitis B?
- `hbv_d_2`: correctly diagnose without fibrosis?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `hbv_t_1`: Did the provider prescribe treatments?
- `hbv_t_2`: Did the provider prescribe additional tests?

**Monitoring (Did the provider mention...?)**
- `hbv_m_1`: Follow up every 6-12 months
- `hbv_m_2`: Clinical exam, LFTs, fibrosis, HBV DNA, and HBeAg

**Counseling (Did the provider mention...?)**
- `hbv_con_1`: Disease is stable, no treatment needed
- `hbv_con_2`: Importance of regular monitoring
- `hbv_con_3`: Screen family
- `hbv_con_4`: Avoid alcohol and live a healthy lifestyle

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `hbv_t_p_1`: Did the provider prescribe treatments?
- `hbv_t_p_2`: Additional Tests

**Final Monitoring (In 'Treatment_Post' context)**
- `hbv_m_p_1`: Follow up every 6-12 months
- `hbv_m_p_2`: Clinical exam, LFTs, fibrosis, HBV DNA, and HBeAg

**Final Counseling (In 'Treatment_Post' context)**
- `hbv_con_p_1`: Disease is stable, no treatment needed
- `hbv_con_p_2`: Importance of regular monitoring
- `hbv_con_p_3`: Screen family
- `hbv_con_p_4`: Avoid alcohol and live a healthy lifestyle


**Clinical Exams (Did the provider order/check...?)**
- `hbv_ce_1`: Patient is Alert
- `hbv_ce_2`: Extremities
- `hbv_ce_3`: Abdominal examination
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
      "output_variable": "hbv_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
