PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
   - **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
   - **History Questions (`ast_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
   - **Labs/Exams (`ast_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
   - **Diagnosis (`ast_d`):** Check the "Diagnosis" field in the transcript.
   - **Treatment (`ast_t_*`):** Check the "Treatment" field in the transcript.
   - **Counseling (`ast_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
   - **Final Treatment (`ast_t_p_*`):** Check the "Treatment_Post" field in the transcript.
   - **Final Counseling (`ast_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

**History (Did the provider ask...?)**
- `ast_h_1`: Does the difficulty breathing come and go and/or is it episodic?
- `ast_h_2`: How long does an episode or attack typically last?
- `ast_h_3`: Since when have you had these symptoms?
- `ast_h_4`: Have you had any other episodes previously?
- `ast_h_5`: Do you have a fever?
- `ast_h_6`: How often does it happen?
- `ast_h_7`: Do you cough?
- `ast_h_8`: Are you coughing a lot?
- `ast_h_9`: Tell me more about your cough. Is it dry or wet?
- `ast_h_10`: Are you coughing up any blood or mucus?
- `ast_h_11`: Do you ever have wheezing/noise in your chest?
- `ast_h_12`: Have you been in contact with anyone with fever and cough in the previous 3-5 days?
- `ast_h_13`: Have you lost weight?
- `ast_h_14`: Have you had night sweats?
- `ast_h_15`: Do you have any pain?
- `ast_h_16`: How do you get relief?
- `ast_h_17`: What triggers the episodes (e.g., dust, pollution, bad air quality, cold)?
- `ast_h_18`: Does it happen when the weather is cold?
- `ast_h_19`: Does it happen when it is dusty?
- `ast_h_20`: Does it happen when it is smoky?
- `ast_h_21`: Does it change with the season change?
- `ast_h_22`: Is it worse at certain times of the day?
- `ast_h_23`: Do any of your siblings/parents have similar problems?
- `ast_h_24`: Does anyone in your household or family have a history of similar symptoms?
- `ast_h_25`: Has this happened before when you were younger?
- `ast_h_26`: Have you taken any medication?
- `ast_h_27`: Do you know the name of the cough syrup?
- `ast_h_28`: Do you smoke?
- `ast_h_29`: Do you drink alcohol?
- `ast_h_30`: Do you have hypertension / high blood pressure or diabetes/blood sugar issues?
- `ast_h_31`: Have you ever had any HIV/STIs/STDs? Any history of HIV/STIs/STDs?

**Laboratory Tests (Did the provider order...?)**
- `ast_lt_1`: Peak Expiratory Flow (PEF)
- `ast_lt_2`: Predicted FEV1
- `ast_lt_3`: Offered any other laboratory tests?

**Diagnosis**
- `ast_d`: correctly diagnose asthma?

**Treatment (Did the provider order in the 'Treatment' section?)**
- `ast_t_1`: Low-dose ICS-formoterol for symptom relief. (e.g., Budesonide-fomoterol 160/4.5 mcd, 1 inhalation as needed)
- `ast_t_2`: As-needed SABA?

**Counseling (Did the provider mention...?)**
- `ast_con_1`: Explain possible triggers (i.e., dust, cold air), and the importance of limiting exposure to the triggers
- `ast_con_2`: Use a mask, particularly in places or conditions where the trigger is present
- `ast_con_3`: Keep the room clean and well-ventilated
- `ast_con_4`: Explain conditions that required emergency management (e.g., worsening difficulty breathing)
- `ast_con_5`: Explain how to use the medication (inhaler or spacer technique)

**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**
- `ast_t_p_1`: Low-dose ICS-formoterol for symptom relief. (e.g., Budesonide-fomoterol 160/4.5 mcd, 1 inhalation as needed)
- `ast_t_p_2`: As-needed SABA?

**Final Counseling (In 'Treatment_Post' context)**
- `ast_con_p_1`: Explain possible triggers (i.e., dust, cold air), and the importance of limiting exposure to the triggers
- `ast_con_p_2`: Use a mask, particularly in places or conditions where the trigger is present
- `ast_con_p_3`: Keep the room clean and well-ventilated
- `ast_con_p_4`: Explain conditions that required emergency management (e.g., worsening difficulty breathing)
- `ast_con_p_5`: Explain how to use the medication (inhaler or spacer technique)
- `ast_referral_p`: Did the provider make a referral?


**Clinical Exams (Did the provider order/check...?)**
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
      "output_variable": "ast_h_1",
      "value_type": "select_one_yesno",
      "value": 0 or 1
    },
    ... (repeat for all variables in checklist)
  ]
}
"""
