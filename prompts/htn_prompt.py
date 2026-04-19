PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`htn_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`htn_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`htn_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`htn_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`htn_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`htn_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`htn_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `htn_h_1`: What other symptoms do you have?
- `htn_h_2`: Can you describe how the headache is?
- `htn_h_3`: When does it usually start during the day?
- `htn_h_4`: How many days has it been?
- `htn_h_5`: Does the headache come every day?
- `htn_h_6`: Is there chest pain?
- `htn_h_7`: Any difficulty in breathing?
- `htn_h_8`: Any vision changes?
- `htn_h_9`: Any heart palpitations?
- `htn_h_10`: Do you have numbness or tingling in the limbs?
- `htn_h_11`: Do you feel tired easily?
- `htn_h_12`: Do you have a previous disease or illness?
- `htn_h_13`: Do you have a history of diabetes?
- `htn_h_14`: Do you have a history of high blood pressure?
- `htn_h_15`: Do you have a history of stroke?
- `htn_h_16`: Do you have any family history of hypertension?
- `htn_h_17`: Do you regularly exercise?
- `htn_h_18`: How about your everyday food?
- `htn_h_19`: Have you received any medication?
- `htn_h_20`: Did you take any health checks before?

**Laboratory Tests (Did the provider order...?)**
- `htn_lt_1`: Haemoglobin
- `htn_lt_2`: Lipid Profile: total cholesterol
- `htn_lt_3`: Lipid Profile: LDL
- `htn_lt_4`: Lipid Profile: HDL
- `htn_lt_5`: Lipid Profile: triglycerides
- `htn_lt_6`: Renal Function: creatinine
- `htn_lt_7`: Renal Function: sodium
- `htn_lt_8`: Renal Function: potassium
- `htn_lt_9`: Renal Function: chloride
- `htn_lt_10`: ECG
- `htn_lt_11`: Urinalysis: protein
- `htn_lt_12`: Urinalysis: glucose
- `htn_lt_13`: Urinalysis: pH
- `htn_lt_14`: Urinalysis: RBC/WBC
- `htn_lt_15`: Offered any other laboratory tests?

**Diagnosis**
- `htn_d`: correctly diagnose hypertension?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `htn_t_1`: Give Antihypertension (ACEI inhibitor or CCB) for 2 weeks.
- `htn_t_2`: Initiate statin treatment
- `htn_t_3`: Recheck BP in 1 months

**Counseling (Did the provider mention...?)**
- `htn_con_1`: Instruct on how to drink the medicine
- `htn_con_2`: Lifestyle modification (DASH diet-low sodium, high fruits, low saturated fat, exercise regularly, reduce salt intake, and alcohol)
- `htn_con_3`: Instruct to return after 2 weeks
- `htn_con_4`: Explain conditions that needs emergency care

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `htn_t_p_1`: Give Antihypertension (ACEI inhibitor or CCB) for 2 weeks.
- `htn_t_p_2`: Initiate statin treatment
- `htn_t_p_3`: Recheck BP in 1 months

**Final Counseling (In 'Treatment_Post' context)**
- `htn_con_p_1`: Instruct on how to drink the medicine
- `htn_con_p_2`: Lifestyle modification (DASH diet-low sodium, high fruits, low saturated fat, exercise regularly, reduce salt intake, and alcohol)
- `htn_con_p_3`: Instruct to return after 2 weeks
- `htn_con_p_4`: Explain conditions that needs emergency care
- `htn_referral_p`: Did the provider make a referral?


**Clinical Exams (Did the provider order/check...?)**
- `htn_ce_1`: Weight
- `htn_ce_2`: Height
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
      "output_variable": "htn_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
