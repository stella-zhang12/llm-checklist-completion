PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`tb1_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`tb1_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`tb1_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`tb1_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`tb1_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`tb1_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`tb1_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `tb1_h_1`: Since when have you had this cough?
- `tb1_h_2`: What is the cough type?
- `tb1_h_3`: What is the color of the sputum?
- `tb1_h_4`: Is there any blood in the sputum?
- `tb1_h_5`: What is the color of the blood?
- `tb1_h_6`: Is the cough a change in a particular condition, such as when it is cold?
- `tb1_h_7`: Do you experience chest pain or breathing difficulty?
- `tb1_h_8`: Do you have a fever? If yes, is it high or low?
- `tb1_h_9`: How was the fever pattern?
- `tb1_h_10`: Do you have any night sweats?
- `tb1_h_11`: Does anyone in your household have a chronic cough?
- `tb1_h_12`: Has your father gotten treatment?
- `tb1_h_13`: Do you experience weight loss?
- `tb1_h_14`: Does your appetite change?
- `tb1_h_15`: Do you have fatigue?
- `tb1_h_16`: Have you ever had a similar cough like this before (prior episodes)?
- `tb1_h_17`: Do you have a history of previous medication?
- `tb1_h_18`: How about your alcohol use?
- `tb1_h_19`: Do you smoke?
- `tb1_h_20`: Have you ever tested for HIV?
- `tb1_h_21`: How about your diet?
- `tb1_h_22`: What is your profession?
- `tb1_h_23`: Have you had sex with a sex worker previously? Any high-risk sexual behavior?
- `tb1_h_24`: Have you ever engaged with IV drug use?

**Laboratory Tests (Did the provider order...?)**
- `tb1_lt_1`: Sputum exam
- `tb1_lt_2`: Chest x-ray
- `tb1_lt_3`: ESR (erythrocyte sedimentation rate)
- `tb1_lt_4`: HIV test
- `tb1_lt_5`: Blood sugar test
- `tb1_lt_6`: Offered any other laboratory tests?

**Diagnosis**
- `tb1_d`: correctly diagnose TB?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `tb1_t_1`: Start TB regimen (4 drugs for 2 months, then 2 drugs for 6 months)
- `tb1_t_2`: Refer to the TB clinic for follow-up

**Counseling (Did the provider mention...?)**
- `tb1_con_1`: Explain adherence to TB medication
- `tb1_con_2`: Testing and treatment for close contacts
- `tb1_con_3`: Explain hygiene and ventilation
- `tb1_con_4`: Explain nutrition guidance

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `tb1_t_p_1`: Start TB regimen (4 drugs for 2 months, then 2 drugs for 6 months)
- `tb1_t_p_2`: Refer to the TB clinic for follow-up

**Final Counseling (In 'Treatment_Post' context)**
- `tb1_con_p_1`: Explain adherence to TB medication
- `tb1_con_p_2`: Testing and treatment for close contacts
- `tb1_con_p_3`: Explain hygiene and ventilation
- `tb1_con_p_4`: Explain nutrition guidance
- `tb1_referral_p`: Did the provider make a referral?


**Clinical Exams (Did the provider order/check...?)**
- `tb1_ce_1`: Weight
- `tb1_ce_2`: Height
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
      "output_variable": "tb1_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
