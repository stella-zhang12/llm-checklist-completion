PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`t2d_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`t2d_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`t2d_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`t2d_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`t2d_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`t2d_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`t2d_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `t2d_h_1`: How long has this been going on?
- `t2d_h_2`: Do you have a fever?
- `t2d_h_3`: Do you have any vomiting?
- `t2d_h_4`: Has your appetite changed?
- `t2d_h_5`: Has your thirst changed?
- `t2d_h_6`: Do you have diarrhea?
- `t2d_h_7`: Do you have a cough?
- `t2d_h_8`: Do you experience shortness of breath?
- `t2d_h_9`: Do you take any medications?
- `t2d_h_10`: How about your urination?
- `t2d_h_11`: Do you experience numbness or tingling in your limbs?
- `t2d_h_12`: Do you smoke?
- `t2d_h_13`: Do you consume alcohol?
- `t2d_h_14`: Do you regularly exercise?
- `t2d_h_15`: Did you take any health checks?
- `t2d_h_16`: How about blood pressure? Do you have a history of high blood pressure?
- `t2d_h_17`: Do you have any family history of diabetes?
- `t2d_h_18`: Do you have any family history of hypertension?
- `t2d_h_19`: Do you experience any dizziness?
- `t2d_h_20`: Do you have any headaches or joint pain?

**Laboratory Tests (Did the provider order...?)**
- `t2d_lt_1`: Fasting blood sugar
- `t2d_lt_2`: Random blood sugar
- `t2d_lt_3`: HbA1c
- `t2d_lt_4`: Offered any other laboratory tests?

**Diagnosis**
- `t2d_d`: correctly diagnose diabetes?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `t2d_t_1`: Refer to the diabetic clinic
- `t2d_t_2`: Start oral hypoglycemics
- `t2d_t_3`: Lifestyle modifications (diet and exercise)
- `t2d_t_4`: Monitor glucose levels

**Counseling (Did the provider mention...?)**
- `t2d_con_1`: Explain his condition and diagnosis
- `t2d_con_2`: Explain the importance of foot care and how to do that
- `t2d_con_3`: Instructions about diet and exercise guidance
- `t2d_con_4`: Medication adherence

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `t2d_t_p_1`: Refer to the diabetic clinic
- `t2d_t_p_2`: Start oral hypoglycemics
- `t2d_t_p_3`: Lifestyle modifications (diet and exercise)
- `t2d_t_p_4`: Monitor glucose levels

**Final Counseling (In 'Treatment_Post' context)**
- `t2d_con_p_1`: Explain his condition and diagnosis
- `t2d_con_p_2`: Explain the importance of foot care and how to do that
- `t2d_con_p_3`: Instructions about diet and exercise guidance
- `t2d_con_p_4`: Medication adherence
- `t2d_referral_p`: Did the provider make a referral?


**Clinical Exams (Did the provider order/check...?)**
- `t2d_ce_1`: Abdomen Exam
- `t2d_ce_2`: Oral Exam
- `t2d_ce_3`: Neurological Exam
- `t2d_ce_4`: Fundoscopy
- `t2d_ce_5`: Weight
- `t2d_ce_6`: Height
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
      "output_variable": "t2d_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
