import os
import re

# ==========================================
# 1. RAW DATA INPUT
# ==========================================
RAW_DATA = """
begin group
ast
select_one yesno
ast_h_1
AH1: Does the difficulty breathing come and go and/or is it episodic?
select_one yesno
ast_h_2
AH2: How long does an episode or attack typically last?
select_one yesno
ast_h_3
AH3: Since when have you had these symptoms?
select_one yesno
ast_h_4
AH4: Have you had any other episodes previously?
select_one yesno
ast_h_5
AH5: Do you have a fever?
select_one yesno
ast_h_6
AH6: How often does it happen?
select_one yesno
ast_h_7
AH7: Do you cough?
select_one yesno
ast_h_8
AH8: Are you coughing a lot?
select_one yesno
ast_h_9
AH9: Tell me more about your cough. Is it dry or wet?
select_one yesno
ast_h_10
AH10: Are you coughing up any blood or mucus?
select_one yesno
ast_h_11
AH11: Do you ever have wheezing/noise in your chest?
select_one yesno
ast_h_12
AH12: Have you been in contact with anyone with fever and cough in the previous 3-5 days?
select_one yesno
ast_h_13
AH13: Have you lost weight?
select_one yesno
ast_h_14
AH14: Have you had night sweats?
select_one yesno
ast_h_15
AH15: Do you have any pain?
select_one yesno
ast_h_16
AH16: How do you get relief?
select_one yesno
ast_h_17
AH17: What triggers the episodes (e.g., dust, pollution, bad air quality, cold)?
select_one yesno
ast_h_18
AH18: Does it happen when the weather is cold?
select_one yesno
ast_h_19
AH19: Does it happen when it is dusty?
select_one yesno
ast_h_20
AH20: Does it happen when it is smoky?
select_one yesno
ast_h_21
AH21: Does it change with the season change?
select_one yesno
ast_h_22
AH22: Is it worse at certain times of the day?
select_one yesno
ast_h_23
AH23: Do any of your siblings/parents have similar problems?
select_one yesno
ast_h_24
AH24: Does anyone in your household or family have a history of similar symptoms?
select_one yesno
ast_h_25
AH25: Has this happened before when you were younger?
select_one yesno
ast_h_26
AH26: Have you taken any medication?
select_one yesno
ast_h_27
AH27: Do you know the name of the cough syrup?
select_one yesno
ast_h_28
AH28: Do you smoke?
select_one yesno
ast_h_29
AH29: Do you drink alcohol?
select_one yesno
ast_h_30
AH30: Do you have hypertension / high blood pressure or diabetes/blood sugar issues?
select_one yesno
ast_h_31
AH31: Have you ever had any HIV/STIs/STDs? Any history of HIV/STIs/STDs?
select_one yesno
ast_lt_1
ALT1: Peak Expiratory Flow (PEF)
select_one yesno
ast_lt_2
ALT2: Predicted FEV1
select_one yesno
ast_lt_3
ALT3: Offered any other laboratory tests?
select_one yesno
ast_d
AD: correctly diagnose asthma?
select_one yesno
ast_t_1
AT1: Low-dose ICS-formoterol for symptom relief. (e.g., Budesonide-fomoterol 160/4.5 mcd, 1 inhalation as needed)
select_one yesno
ast_t_2
AT2: As-needed SABA?
select_one yesno
ast_con_1
ACON1: Explain possible triggers (i.e., dust, cold air), and the importance of limiting exposure to the triggers
select_one yesno
ast_con_2
ACON2: Use a mask, particularly in places or conditions where the trigger is present
select_one yesno
ast_con_3
ACON3: Keep the room clean and well-ventilated
select_one yesno
ast_con_4
ACON4: Explain conditions that required emergency management (e.g., worsening difficulty breathing)
select_one yesno
ast_con_5
ACON5: Explain how to use the medication (inhaler or spacer technique)
select_one yesno
ast_referral
Did the provider make a referral?
select_one yesno
ast_t_p_1
ATP1: Low-dose ICS-formoterol for symptom relief. (e.g., Budesonide-fomoterol 160/4.5 mcd, 1 inhalation as needed)
select_one yesno
ast_t_p_2
ATP2: As-needed SABA?
select_one yesno
ast_con_p_1
ACON1: Explain possible triggers (i.e., dust, cold air), and the importance of limiting exposure to the triggers
select_one yesno
ast_con_p_2
ACON2: Use a mask, particularly in places or conditions where the trigger is present
select_one yesno
ast_con_p_3
ACON3: Keep the room clean and well-ventilated
select_one yesno
ast_con_p_4
ACON4: Explain conditions that required emergency management (e.g., worsening difficulty breathing)
select_one yesno
ast_con_p_5
ACON5: Explain how to use the medication (inhaler or spacer technique)
select_one yesno
ast_referral_p
Did the provider make a referral?
end group

begin group
pne
select_one yesno
pne_h_1
PH1: What other symptoms do you have?
select_one yesno
pne_h_2
PH2: How long has the cough lasted?
select_one yesno
pne_h_3
PH3: Is the cough dry or productive?
select_one yesno
pne_h_4
PH4: What color is the sputum/mucus?
select_one yesno
pne_h_5
PH5: Is there blood in the sputum/mucus?
select_one yesno
pne_h_6
PH6: Is there chest pain?
select_one yesno
pne_h_7
PH7: Any difficulty in breathing?
select_one yesno
pne_h_8
PH8: How is your appetite?
select_one yesno
pne_h_9
PH9: Do you have a high or low fever?
select_one yesno
pne_h_10
PH10: Are you tired or lethargic?
select_one yesno
pne_h_11
PH11: Any difficulty in swallowing?
select_one yesno
pne_h_12
PH12: Is there a runny nose?
select_one yesno
pne_h_13
PH13: Have you received any medication?
select_one yesno
pne_h_14
PH14: Have you experienced similar symptoms before?
select_one yesno
pne_h_15
PH15: Do any of your siblings/parents currently have similar problems?
select_one yesno
pne_h_16
PH16: Does anyone in your household or family have a history of similar symptoms?
select_one yesno
pne_h_17
PH17: Redness of eyes?
select_one yesno
pne_h_18
PH18: Have you received the COVID-19 vaccine?
select_one yesno
pne_h_19
PH19: Have you received the influenza vaccine?
select_one yesno
pne_h_20
PH20: Do you smoke?
select_one yesno
pne_lt_1
PLT1: Chest X-ray
select_one yesno
pne_lt_2
PLT2: Complete Blood Count (CBC): WBC
select_one yesno
pne_lt_3
PLT3: Complete Blood Count (CBC): neutrophils
select_one yesno
pne_lt_4
PLT4: Complete Blood Count (CBC): bands
select_one yesno
pne_lt_5
PLT5: Complete Blood Count (CBC): lymphocytes
select_one yesno
pne_lt_6
PLT6: Complete Blood Count (CBC): Hb
select_one yesno
pne_lt_7
PLT7: Offered any other laboratory tests?
select_one yesno
pne_d
PD: correctly diagnose pneumonia?
select_one yesno
pne_t_1
PT1: Treat as an inpatient
select_one yesno
pne_t_2
PT2: Ceftriaxone 2g daily, IV
select_one yesno
pne_t_3
PT3: Paracetamol 500 mg PO up to four times daily
select_one yesno
pne_t_4
PT4: Monitor vital signs
select_one yesno
pne_con_1
ACON1: Explain conditions that required emergency management (e.g., confusion, worsening difficulty breathing)
select_one yesno
pne_con_2
ACON2: Encourage feeding and fluid intake
select_one yesno
pne_t_p_1
PTP1: Treat as an inpatient
select_one yesno
pne_t_p_2
PTP2: Ceftriaxone 2g daily, IV
select_one yesno
pne_t_p_3
PTP3: Paracetamol 500 mg PO up to four times daily
select_one yesno
pne_t_p_4
PTP4: Monitor vital signs
select_one yesno
pne_con_p_1
ACON1: Explain conditions that required emergency management (e.g., confusion, worsening difficulty breathing)
select_one yesno
pne_con_p_2
ACON2: Encourage feeding and fluid intake
select_one yesno
pne_referral_p
Did the provider make a referral?
end group

begin group
t2d
select_one yesno
t2d_h_1
DH1: How long has this been going on?
select_one yesno
t2d_h_2
DH2: Do you have a fever?
select_one yesno
t2d_h_3
DH3: Do you have any vomiting?
select_one yesno
t2d_h_4
DH4: Has your appetite changed?
select_one yesno
t2d_h_5
DH5: Has your thirst changed?
select_one yesno
t2d_h_6
DH6: Do you have diarrhea?
select_one yesno
t2d_h_7
DH7: Do you have a cough?
select_one yesno
t2d_h_8
DH8: Do you experience shortness of breath?
select_one yesno
t2d_h_9
DH9: Do you take any medications?
select_one yesno
t2d_h_10
DH10: How about your urination?
select_one yesno
t2d_h_11
DH11: Do you experience numbness or tingling in your limbs?
select_one yesno
t2d_h_12
DH12: Do you smoke?
select_one yesno
t2d_h_13
DH13: Do you consume alcohol?
select_one yesno
t2d_h_14
DH14: Do you regularly exercise?
select_one yesno
t2d_h_15
DH15: Did you take any health checks?
select_one yesno
t2d_h_16
DH16: How about blood pressure? Do you have a history of high blood pressure?
select_one yesno
t2d_h_17
DH17: Do you have any family history of diabetes?
select_one yesno
t2d_h_18
DH18: Do you have any family history of hypertension?
select_one yesno
t2d_h_19
DH19: Do you experience any dizziness?
select_one yesno
t2d_h_20
DH20: Do you have any headaches or joint pain?
select_one yesno
t2d_ce_1
DCE1: Abdomen Exam
select_one yesno
t2d_ce_2
DCE2: Oral Exam
select_one yesno
t2d_ce_3
DCE3: Neurological Exam
select_one yesno
t2d_ce_4
DCE4: Fundoscopy
select_one yesno
t2d_ce_5
DCE5: Weight
select_one yesno
t2d_ce_6
DCE6: Height
select_one yesno
t2d_lt_1
DLT1: Fasting blood sugar
select_one yesno
t2d_lt_2
DLT2: Random blood sugar
select_one yesno
t2d_lt_3
DLT3: HbA1c
select_one yesno
t2d_lt_4
DLT4: Offered any other laboratory tests?
select_one yesno
t2d_d
DD: correctly diagnose diabetes?
select_one yesno
t2d_t_1
DT1: Refer to the diabetic clinic
select_one yesno
t2d_t_2
DT2: Start oral hypoglycemics
select_one yesno
t2d_t_3
DT3: Lifestyle modifications (diet and exercise)
select_one yesno
t2d_t_4
DT4: Monitor glucose levels
select_one yesno
t2d_con_1
DCON1: Explain his condition and diagnosis
select_one yesno
t2d_con_2
DCON2: Explain the importance of foot care and how to do that
select_one yesno
t2d_con_3
DCON3: Instructions about diet and exercise guidance
select_one yesno
t2d_con_4
DCON4: Medication adherence
select_one yesno
t2d_referral
Did the provider make a referral?
select_one yesno
t2d_t_p_1
DTP1: Refer to the diabetic clinic
select_one yesno
t2d_t_p_2
DTP2: Start oral hypoglycemics
select_one yesno
t2d_t_p_3
DTP3: Lifestyle modifications (diet and exercise)
select_one yesno
t2d_t_p_4
DTP4: Monitor glucose levels
select_one yesno
t2d_con_p_1
DCON1: Explain his condition and diagnosis
select_one yesno
t2d_con_p_2
DCON2: Explain the importance of foot care and how to do that
select_one yesno
t2d_con_p_3
DCON3: Instructions about diet and exercise guidance
select_one yesno
t2d_con_p_4
DCON4: Medication adherence
select_one yesno
t2d_referral_p
Did the provider make a referral?
end group

begin group
tb1
select_one yesno
tb1_h_1
TH1: Since when have you had this cough?
select_one yesno
tb1_h_2
TH2: What is the cough type?
select_one yesno
tb1_h_3
TH3: What is the color of the sputum?
select_one yesno
tb1_h_4
TH4: Is there any blood in the sputum?
select_one yesno
tb1_h_5
TH5: What is the color of the blood?
select_one yesno
tb1_h_6
TH6: Is the cough a change in a particular condition, such as when it is cold?
select_one yesno
tb1_h_7
TH7: Do you experience chest pain or breathing difficulty?
select_one yesno
tb1_h_8
TH8: Do you have a fever? If yes, is it high or low?
select_one yesno
tb1_h_9
TH9: How was the fever pattern?
select_one yesno
tb1_h_10
TH10: Do you have any night sweats?
select_one yesno
tb1_h_11
TH11: Does anyone in your household have a chronic cough?
select_one yesno
tb1_h_12
TH12: Has your father gotten treatment?
select_one yesno
tb1_h_13
TH13: Do you experience weight loss?
select_one yesno
tb1_h_14
TH14: Does your appetite change?
select_one yesno
tb1_h_15
TH15: Do you have fatigue?
select_one yesno
tb1_h_16
TH16: Have you ever had a similar cough like this before (prior episodes)?
select_one yesno
tb1_h_17
TH17: Do you have a history of previous medication?
select_one yesno
tb1_h_18
TH18: How about your alcohol use?
select_one yesno
tb1_h_19
TH19: Do you smoke?
select_one yesno
tb1_h_20
TH20: Have you ever tested for HIV?
select_one yesno
tb1_h_21
TH21: How about your diet?
select_one yesno
tb1_h_22
TH22: What is your profession?
select_one yesno
tb1_h_23
TH23: Have you had sex with a sex worker previously? Any high-risk sexual behavior?
select_one yesno
tb1_h_24
TH24: Have you ever engaged with IV drug use?
select_one yesno
tb1_ce_1
TCE1: Weight
select_one yesno
tb1_ce_2
TCE2: Height
select_one yesno
tb1_lt_1
TLT1: Sputum exam
select_one yesno
tb1_lt_2
TLT2: Chest x-ray
select_one yesno
tb1_lt_3
TLT3: ESR (erythrocyte sedimentation rate)
select_one yesno
tb1_lt_4
TLT4: HIV test
select_one yesno
tb1_lt_5
TLT5: Blood sugar test
select_one yesno
tb1_lt_6
TLT6: Offered any other laboratory tests?
select_one yesno
tb1_d
TD:correctly diagnose TB?
select_one yesno
tb1_t_1
TT1: Start TB regimen (4 drugs for 2 months, then 2 drugs for 6 months)
select_one yesno
tb1_t_2
TT2: Refer to the TB clinic for follow-up
select_one yesno
tb1_con_1
TCON1: Explain adherence to TB medication
select_one yesno
tb1_con_2
TCON2: Testing and treatment for close contacts
select_one yesno
tb1_con_3
TCON3: Explain hygiene and ventilation
select_one yesno
tb1_con_4
TCON4: Explain nutrition guidance
select_one yesno
tb1_referral
Did the provider make a referral?
select_one yesno
tb1_t_p_1
TT1: Start TB regimen (4 drugs for 2 months, then 2 drugs for 6 months)
select_one yesno
tb1_t_p_2
TT2: Refer to the TB clinic for follow-up
select_one yesno
tb1_con_p_1
TCON1: Explain adherence to TB medication
select_one yesno
tb1_con_p_2
TCON2: Testing and treatment for close contacts
select_one yesno
tb1_con_p_3
TCON3: Explain hygiene and ventilation
select_one yesno
tb1_con_p_4
TCON4: Explain nutrition guidance
select_one yesno
tb1_referral_p
Did the provider make a referral?
end group

begin group
htn
select_one yesno
htn_h_1
HH1: What other symptoms do you have?
select_one yesno
htn_h_2
HH2: Can you describe how the headache is?
select_one yesno
htn_h_3
HH3: When does it usually start during the day?
select_one yesno
htn_h_4
HH4: How many days has it been?
select_one yesno
htn_h_5
HH5: Does the headache come every day?
select_one yesno
htn_h_6
HH6: Is there chest pain?
select_one yesno
htn_h_7
HH7: Any difficulty in breathing?
select_one yesno
htn_h_8
HH8: Any vision changes?
select_one yesno
htn_h_9
HH9: Any heart palpitations?
select_one yesno
htn_h_10
HH10: Do you have numbness or tingling in the limbs?
select_one yesno
htn_h_11
HH11: Do you feel tired easily?
select_one yesno
htn_h_12
HH12: Do you have a previous disease or illness?
select_one yesno
htn_h_13
HH13: Do you have a history of diabetes?
select_one yesno
htn_h_14
HH14: Do you have a history of high blood pressure?
select_one yesno
htn_h_15
HH15: Do you have a history of stroke?
select_one yesno
htn_h_16
HH16: Do you have any family history of hypertension?
select_one yesno
htn_h_17
HH17: Do you regularly exercise?
select_one yesno
htn_h_18
HH18: How about your everyday food?
select_one yesno
htn_h_19
HH19: Have you received any medication?
select_one yesno
htn_h_20
HH20: Did you take any health checks before?
select_one yesno
htn_ce_1
HCE1: Weight
select_one yesno
htn_ce_2
HCE2: Height
select_one yesno
htn_lt_1
HLT1: Haemoglobin
select_one yesno
htn_lt_2
HLT2: Lipid Profile: total cholesterol
select_one yesno
htn_lt_3
HLT3: Lipid Profile: LDL
select_one yesno
htn_lt_4
HLT4: Lipid Profile: HDL
select_one yesno
htn_lt_5
HLT5: Lipid Profile: triglycerides
select_one yesno
htn_lt_6
HLT6: Renal Function: creatinine
select_one yesno
htn_lt_7
HLT7: Renal Function: sodium
select_one yesno
htn_lt_8
HLT8: Renal Function: potassium
select_one yesno
htn_lt_9
HLT9: Renal Function: chloride
select_one yesno
htn_lt_10
HLT10: ECG
select_one yesno
htn_lt_11
HLT11: Urinalysis: protein
select_one yesno
htn_lt_12
HLT12: Urinalysis: glucose
select_one yesno
htn_lt_13
HLT13: Urinalysis: pH
select_one yesno
htn_lt_14
HLT14: Urinalysis: RBC/WBC
select_one yesno
htn_lt_15
HLT15: Offered any other laboratory tests?
select_one yesno
htn_d
HD: correctly diagnose hypertension?
select_one yesno
htn_t_1
HT1: Give Antihypertension (ACEI inhibitor or CCB) for 2 weeks.
select_one yesno
htn_t_2
HT2: Initiate statin treatment
select_one yesno
htn_t_3
HT3: Recheck BP in 1 months
select_one yesno
htn_con_1
HCON1: Instruct on how to drink the medicine
select_one yesno
htn_con_2
HCON2: Lifestyle modification (DASH diet-low sodium, high fruits, low saturated fat, exercise regularly, reduce salt intake, and alcohol)
select_one yesno
htn_con_3
HCON3: Instruct to return after 2 weeks
select_one yesno
htn_con_4
HCON4: Explain conditions that needs emergency care
select_one yesno
htn_referral
Did the provider make a referral?
select_one yesno
htn_t_p_1
HT1: Give Antihypertension (ACEI inhibitor or CCB) for 2 weeks.
select_one yesno
htn_t_p_2
HT2: Initiate statin treatment
select_one yesno
htn_t_p_3
HT3: Recheck BP in 1 months
select_one yesno
htn_con_p_1
HCON1: Instruct on how to drink the medicine
select_one yesno
htn_con_p_2
HCON2: Lifestyle modification (DASH diet-low sodium, high fruits, low saturated fat, exercise regularly, reduce salt intake, and alcohol)
select_one yesno
htn_con_p_3
HCON3: Instruct to return after 2 weeks
select_one yesno
htn_con_p_4
HCON4: Explain conditions that needs emergency care
select_one yesno
htn_referral_p
Did the provider make a referral?
end group

begin group
hbc
select_one yesno
hbc_h_1
HBCH1: Have you ever been diagnosed with hepatitis B?
select_one yesno
hbc_h_2
HBCH2: Have you ever taken any antiviral medications?
select_one yesno
hbc_h_3
HBCH3: Do you consume alcohol?
select_one yesno
hbc_h_4
HBCH4: Do you smoke?
select_one yesno
hbc_h_5
HBCH5: Have you had any recent weight changes?
select_one yesno
hbc_h_6
HBCH6: Has your appetite changed?
select_one yesno
hbc_h_7
HBCH7: Have you noticed any changes in your skin?
select_one yesno
hbc_h_8
HBCH8: How about your urine color?
select_one yesno
hbc_h_9
HBCH9: Since when have you experienced these symptoms?
select_one yesno
hbc_h_10
HBCH10: Do you experience any vomiting?
select_one yesno
hbc_h_11
HBCH11: Do you experience any bleeding?
select_one yesno
hbc_h_12
HBCH12: Do you experience any difficulty breathing?
select_one yesno
hbc_h_13
HBCH13: Do you have a history of chronic illnesses or liver diseases?
select_one yesno
hbc_h_14
HBCH14: Do you have a fever?
select_one yesno
hbc_h_15
HBCH15: Do you have leg swelling?
select_one yesno
hbc_h_16
HBCH16: Do you think that your belly is getting bigger?
select_one yesno
hbc_h_17
HBCH17: Do you have a history of sexually transmitted diseases (STDs)?
select_one yesno
hbc_h_18
HBCH18: Do you have a history of using unsafe injections?
select_one yesno
hbc_h_19
HBCH19: Any history of liver disease in your family?
select_one yesno
hbc_h_20
HBCH20: How about your wife or child? Do they have any hepatitis B or C?
select_one yesno
hbc_h_21
HBCH21: Any medications at home currently?
select_one yesno
hbc_ce_1
HBCCE1: Patient is Alert
select_one yesno
hbc_ce_2
HBCCE2: Weight
select_one yesno
hbc_ce_3
HBCCE3: Height
select_one yesno
hbc_ce_4
HBCCE4: Extremities
select_one yesno
hbc_ce_5
HBCCE5: Abdominal examination
select_one yesno
hbc_lt_1
HBCLT1: Liver Function: total bilirubin
select_one yesno
hbc_lt_2
HBCLT2: Liver Function: direct bilirubin
select_one yesno
hbc_lt_3
HBCLT3: Liver Function: albumin
select_one yesno
hbc_lt_4
HBCLT4: Liver Enzymes: AST/ALT
select_one yesno
hbc_lt_5
HBCLT5: Liver Enzymes: INR
select_one yesno
hbc_lt_6
HBCLT6: HBV: HBV DNA
select_one yesno
hbc_lt_7
HBCLT7: HBV: HBeAg
select_one yesno
hbc_lt_8
HBCLT8: HBV: Anti-HBe
select_one yesno
hbc_lt_9
HBCLT9: Anti-HCV
select_one yesno
hbc_lt_10
HBCLT10: Platelets
select_one yesno
hbc_lt_11
HBCLT11: AFP
select_one yesno
hbc_lt_12
HBCLT12: Creatinine
select_one yesno
hbc_lt_13
HBCLT13: Ultrasound
select_one yesno
hbc_lt_14
HBCLT14: Gastroscopy
select_one yesno
hbc_lt_15
HLT6: Offered any other laboratory tests?
select_one yesno
hbc_d_1
HBCD: correctly diagnose hepatitis B?
select_one yesno
hbc_d_2
HBCD: correctly diagnose with decompensated cirrhosis (Child-Pugh Class C)?
select_one yesno
hbc_t_1
HBCT1: Hospital admission
select_one yesno
hbc_t_2
HBCT2: Initiate TDF 300 mg/day (CrCl 72.79)
select_one yesno
hbc_t_3
HBCT3: Monitor for side effects (renal, lactic acidosis, osteoporosis)
select_one yesno
hbc_t_4
HBCT4: Improve cirrhosis status and prolong life expectancy
select_one yesno
hbc_t_5
HBCT5: Varices ligation
select_one yesno
hbc_t_6
HBCT6: Propranolol 40 mg PO daily
select_one yesno
hbc_m_1
HBCM1: Hospitalize until ascites and jaundice resolve
select_one yesno
hbc_m_2
HBCM2: Clinical and liver function monitoring every 2 weeks
select_one yesno
hbc_m_3
HBCM3: HBV DNA every 6 months
select_one yesno
hbc_m_4
HBCM4: Viral load and Anti-HBe at week 12
select_one yesno
hbc_m_5
HBCM5: Liver cancer/HCC screening every 12-24 weeks
select_one yesno
hbc_m_6
HBCM6: Fibrosis evaluation every 12-24 weeks
select_one yesno
hbc_m_7
HBCM7: Creatinine monitoring every 6 months
select_one yesno
hbc_con_1
HBCCON1: Explain hepatitis B, the risk of progression to liver cancer, and bleeding from esophageal varices and other complications
select_one yesno
hbc_con_2
HBCCON2: Importance of lifelong treatment, adherence, and follow-up
select_one yesno
hbc_con_3
HBCCON3: Screening and vaccination for family members
select_one yesno
hbc_con_4
HBCCON4: Lifestyle changes (stop alcohol, healthy diet, rest, exercise)
select_one yesno
hbc_t_p_1
HBCT1: Hospital admission
select_one yesno
hbc_t_p_2
HBCT2: Initiate TDF 300 mg/day (CrCl 72.79)
select_one yesno
hbc_t_p_3
HBCT3: Monitor for side effects (renal, lactic acidosis, osteoporosis)
select_one yesno
hbc_t_p_4
HBCT4: Improve cirrhosis status and prolong life expectancy
select_one yesno
hbc_t_p_5
HBCT5: Varices ligation
select_one yesno
hbc_t_p_6
HBCT6: Propranolol 40 mg PO daily
select_one yesno
hbc_m_p_1
HBCM1: Hospitalize until ascites and jaundice resolve
select_one yesno
hbc_m_p_2
HBCM2: Clinical and liver function monitoring every 2 weeks
select_one yesno
hbc_m_p_3
HBCM3: HBV DNA every 6 months
select_one yesno
hbc_m_p_4
HBCM4: Viral load and Anti-HBe at week 12
select_one yesno
hbc_m_p_5
HBCM5: Liver cancer/HCC screening every 12-24 weeks
select_one yesno
hbc_m_p_6
HBCM6: Fibrosis evaluation every 12-24 weeks
select_one yesno
hbc_m_p_7
HBCM7: Creatinine monitoring every 6 months
select_one yesno
hbc_con_p_1
HBCCON1: Explain hepatitis B, the risk of progression to liver cancer, and bleeding from esophageal varices and other complications
select_one yesno
hbc_con_p_2
HBCCON2: Importance of lifelong treatment, adherence, and follow-up
select_one yesno
hbc_con_p_3
HBCCON3: Screening and vaccination for family members
select_one yesno
hbc_con_p_4
HBCCON4: Lifestyle changes (stop alcohol, healthy diet, rest, exercise)
end group

begin group
hbp
select_one yesno
hbp_h_1
HBPH1: When did you find out about hepatitis B?
select_one yesno
hbp_h_2
HBPH2: How do you know about your hepatitis B status?
select_one yesno
hbp_h_3
HBPH3: Besides HBsAg, are there other laboratory tests, such as liver enzymes or virus count, that you took before?
select_one yesno
hbp_h_4
HBPH4: Have you received any antiviral treatment?
select_one yesno
hbp_h_5
HBPH5: Do you experience any symptoms?
select_one yesno
hbp_h_6
HBPH6: Do you have any fatigue?
select_one yesno
hbp_h_7
HBPH7: Do you have a loss of appetite?
select_one yesno
hbp_h_8
HBPH8: Have you ever had yellow eyes or skin?
select_one yesno
hbp_h_9
HBPH9: Do you have any bleeding?
select_one yesno
hbp_h_10
HBPH10: Do you have other health conditions or medications?
select_one yesno
hbp_h_11
HBPH11: How about your current pregnancy condition?
select_one yesno
hbp_h_12
HBPH12: Is there anyone in your family who has liver disease?
select_one yesno
hbp_h_13
HBPH13: Has your family been tested for hepatitis before?
select_one yesno
hbp_h_14
HBPH14: How about the hepatitis B status of your husband and children?
select_one yesno
hbp_h_15
HBPH15: In your first pregnancy, did you get any viral tests or other health checks?
select_one yesno
hbp_h_16
HBPH16: Do you know your HIV status?
select_one yesno
hbp_h_17
HBPH17: Have you taken a syphilis test?
select_one yesno
hbp_h_18
HBPH18: Do you consume alcohol?
select_one yesno
hbp_h_19
HBPH19: Do you smoke?
select_one yesno
hbp_ce_1
HBPCE1: Patient is Alert
select_one yesno
hbp_ce_2
HBPCE2: Extremities
select_one yesno
hbp_ce_3
HBPCE3: Abdominal examination
select_one yesno
hbp_ce_4
HBPCE4: Fetal Growth
select_one yesno
hbp_lt_1
HBPLT1: CBC: PLT
select_one yesno
hbp_lt_2
HBPLT2: CBC: HGB
select_one yesno
hbp_lt_3
HBPLT3: Hepatitis B: HBeAg
select_one yesno
hbp_lt_4
HBPLT4: Hepatitis B: HBV DNA
select_one yesno
hbp_lt_5
HBPLT5: Anti-HCV
select_one yesno
hbp_lt_6
HBPLT6: HIV
select_one yesno
hbp_lt_7
HBPLT7: Ultrasound
select_one yesno
hbp_lt_8
HBPLT8: Liver Enzyme: AST/ALT
select_one yesno
hbp_lt_9
HBPLT9: Offered any other laboratory tests?
select_one yesno
hbp_d_1
HBPD: correctly diagnose chronic hepatitis B?
select_one yesno
hbp_d_2
HBPD: correctly diagnose without fibrosis?
select_one yesno
hbp_t_1
HBPT1: Did the provider prescribe antiviral treatment?
select_one yesno
hbp_t_2
HBPT2: Did the provider prescribe prophylaxis?
select_one yesno
hbp_m_1
HBPM1: Mother -- re-evaluate 3 months after delivery or earlier if symptoms occur
select_one yesno
hbp_m_2
HBPM2: Baby -- HBV vaccine and HBIG within 24 hours after birth
select_one yesno
hbp_m_3
HBPM3: Baby -- 3 HBV doses in Expanded Program on immunization (EPI)
select_one yesno
hbp_m_4
HBPM4: Baby -- HBsAg and anti-HBs from month 7
select_one yesno
hbp_con_1
HBPCON1: Explain the current disease status and the need for monitoring
select_one yesno
hbp_con_2
HBPCON2: Infant protection protocol
select_one yesno
hbp_con_3
HBPCON3: Encourage family testing
select_one yesno
hbp_con_4
HBPCON4: Breastfeeding is safe
select_one yesno
hbp_con_5
HBPCON5: Choose to disclose status if desired
select_one yesno
hbp_t_p_1
HBPT1: Did the provider prescribe antiviral treatment?
select_one yesno
hbp_t_p_2
HBPT2: Did the provider prescribe prophylaxis?
select_one yesno
hbp_m_p_1
HBPM1: Mother -- re-evaluate 3 months after delivery or earlier if symptoms occur
select_one yesno
hbp_m_p_2
HBPM2: Baby -- HBV vaccine and HBIG within 24 hours after birth
select_one yesno
hbp_m_p_3
HBPM3: Baby -- 3 HBV doses in Expanded Program on immunization (EPI)
select_one yesno
hbp_m_p_4
HBPM4: Baby -- HBsAg and anti-HBs from month 7
select_one yesno
hbp_con_p_1
HBPCON1: Explain the current disease status and the need for monitoring
select_one yesno
hbp_con_p_2
HBPCON2: Infant protection protocol
select_one yesno
hbp_con_p_3
HBPCON3: Encourage family testing
select_one yesno
hbp_con_p_4
HBPCON4: Breastfeeding is safe
select_one yesno
hbp_con_p_5
HBPCON5: Choose to disclose status if desired
end group

begin group
hbv
select_one yesno
hbv_h_1
HBNH1: When did you find out about hepatitis B?
select_one yesno
hbv_h_2
HBNH2: How do you know about your hepatitis B status?
select_one yesno
hbv_h_3
HBNH3: Besides HBsAg, are there other laboratory tests that you took before?
select_one yesno
hbv_h_4
HBNH4: Have you received any antiviral treatment?
select_one yesno
hbv_h_5
HBNH5: Do you currently experience any symptoms?
select_one yesno
hbv_h_6
HBNH6: Do you have any fatigue?
select_one yesno
hbv_h_7
HBNH7: Do you have a loss of appetite?
select_one yesno
hbv_h_8
HBNH8: Do you have yellow eyes or skin?
select_one yesno
hbv_h_9
HBNH9: Do you have any bleeding?
select_one yesno
hbv_h_10
HBNH10: Do you have other health conditions?
select_one yesno
hbv_h_11
HBNH11: Is there anyone in your family who has liver disease?
select_one yesno
hbv_h_12
HBNH12: Has your family been tested for hepatitis before?
select_one yesno
hbv_h_13
HBNH13: Has your mother or anyone else in your family been diagnosed with HCC?
select_one yesno
hbv_h_14
HBNH14: How about the hepatitis B status of your wife and children?
select_one yesno
hbv_h_15
HBNH15: Do you know your HIV status?
select_one yesno
hbv_h_16
HBNH16: Do you know your HCV status?
select_one yesno
hbv_h_17
HBNH17: Are you taking any medications?
select_one yesno
hbv_h_18
HBNH18: Do you smoke or drink?
select_one yesno
hbv_h_19
HBNH19: Do you ever use any injection drugs?
select_one yesno
hbv_h_20
HBNH20: Do you have any history of sexually transmitted diseases (STDs)?
select_one yesno
hbv_h_21
HBNH21: Do you have a history of any risky behaviour?
select_one yesno
hbv_ce_1
HBNCE1: Patient is Alert
select_one yesno
hbv_ce_2
HBNCE2: Extremities
select_one yesno
hbv_ce_3
HBNCE3: Abdominal examination
select_one yesno
hbv_lt_1
HBNLT1: CBC: PLT
select_one yesno
hbv_lt_2
HBNLT2: CBC: HGB
select_one yesno
hbv_lt_3
HBNLT3: HBV: HBeAg
select_one yesno
hbv_lt_4
HBNLT4: HBV: HBV DNA
select_one yesno
hbv_lt_5
HBNLT5: Liver Enzyme: AST/ALT
select_one yesno
hbv_lt_6
HBNLT6: Ultrasound
select_one yesno
hbv_lt_7
HBNLT7: Offered any other laboratory tests?
select_one yesno
hbv_d_1
HBND: correctly diagnose chronic hepatitis B?
select_one yesno
hbv_d_2
HBND: correctly diagnose without fibrosis?
select_one yesno
hbv_t_1
HBNT1: Did the provider prescribe treatments?
select_one yesno
hbv_t_2
HBNT2: Did the provider prescribe additional tests?
select_one yesno
hbv_m_1
HBNM1: Follow up every 6-12 months
select_one yesno
hbv_m_2
HBNM2: Clinical exam, LFTs, fibrosis, HBV DNA, and HBeAg
select_one yesno
hbv_con_1
HBNCON1: Disease is stable, no treatment needed
select_one yesno
hbv_con_2
HBNCON2: Importance of regular monitoring
select_one yesno
hbv_con_3
HBNCON3: Screen family
select_one yesno
hbv_con_4
HBNCON4: Avoid alcohol and live a healthy lifestyle
select_one yesno
hbv_t_p_1
HBNT1: Did the provider prescribe treatments?
select_one yesno
hbv_t_p_2
HBNT2: Additional Tests
select_one yesno
hbv_m_p_1
HBNM1: Follow up every 6-12 months
select_one yesno
hbv_m_p_2
HBNM2: Clinical exam, LFTs, fibrosis, HBV DNA, and HBeAg
select_one yesno
hbv_con_p_1
HBNCON1: Disease is stable, no treatment needed
select_one yesno
hbv_con_p_2
HBNCON2: Importance of regular monitoring
select_one yesno
hbv_con_p_3
HBNCON3: Screen family
select_one yesno
hbv_con_p_4
HBNCON4: Avoid alcohol and live a healthy lifestyle
end group

begin group
hcv
select_one yesno
hcv_h_1
HCH1: How long have you been experiencing these symptoms?
select_one yesno
hcv_h_2
HCH2: What symptoms have you noticed?
select_one yesno
hcv_h_3
HCH3: Do you have shortness of breath?
select_one yesno
hcv_h_4
HCH4: Do your skin or eyes become yellow?
select_one yesno
hcv_h_5
HCH5: How about your urine color?
select_one yesno
hcv_h_6
HCH6: Do you have leg swelling?
select_one yesno
hcv_h_7
HCH7: Do you have a fever?
select_one yesno
hcv_h_8
HCH8: Do you have any history of chronic illnesses or medications?
select_one yesno
hcv_h_9
HCH9: Any history of blood transfusions or surgeries?
select_one yesno
hcv_h_10
HCH10: Have you used traditional or herbal medicine for your current symptoms?
select_one yesno
hcv_h_11
HCH11: Have your family members been tested with Hepatitis?
select_one yesno
hcv_h_12
HCH12: Do you have any past history of liver disease?
select_one yesno
hcv_h_13
HCH13: Did you get antiviral treatment?
select_one yesno
hcv_h_14
HCH14: For your current condition, have you taken any previous laboratory tests?
select_one yesno
hcv_h_15
HCH15: Have you been vaccinated against Hepatitis B?
select_one yesno
hcv_h_16
HCH16: Do you have any family members who have liver disease?
select_one yesno
hcv_h_17
HCH17: Do you drink alcohol or smoke?
select_one yesno
hcv_h_18
HCH18: Do you know your hepatitis B status?
select_one yesno
hcv_h_19
HCH19: Do you know your HIV status?
select_one yesno
hcv_h_20
HCH20: Do you have a history of using unsafe injections?
select_one yesno
hcv_ce_1
HCCE1: Patient is Alert
select_one yesno
hcv_ce_2
HCCE2: Extremities
select_one yesno
hcv_ce_3
HCCE3: Abdominal examination
select_one yesno
hcv_lt_1
HCLT1: CBC: PLT
select_one yesno
hcv_lt_2
HCLT2: CBC: HGB
select_one yesno
hcv_lt_3
HCLT3: Hepatitis B: HBeAg
select_one yesno
hcv_lt_4
HCLT4: Hepatitis C: HCV RNA
select_one yesno
hcv_lt_5
HCLT5: Liver Enzyme: AST/ALT
select_one yesno
hcv_lt_6
HCLT6: Ultrasound
select_one yesno
hcv_lt_7
HCLT7: Bilirubin
select_one yesno
hcv_lt_8
HCLT8: Albumin
select_one yesno
hcv_lt_9
HCLT9: Hepatitis C: Anti-HCV
select_one yesno
hcv_lt_10
HCLT10: Hepatitis B: Anti-HBV
select_one yesno
hcv_lt_11
HCLT11: HIV
select_one yesno
hcv_lt_12
HCLT12: Offered any other laboratory tests?
select_one yesno
hcv_d_1
HCD: correctly diagnose Chronic HCV?
select_one yesno
hcv_d_2
HCD: correctly diagnose advanced fibrosis (F3)?
select_one yesno
hcv_d_3
HCD: correctly diagnose without cirrhosis?
select_one yesno
hcv_d_4
HCD: correctly diagnose without co-infections?
select_one yesno
hcv_t_1
HCT1: Eligible for DAA therapy: SOF/VEL or SOF+DAC for 12 weeks
select_one yesno
hcv_m_1
HCM1: After 1 month: LFTs, CBC
select_one yesno
hcv_m_2
HCM2: SVR12: HCV RNA, fibrosis, AFP, ultrasound, LFT, CBC
select_one yesno
hcv_m_3
HCM3: Screen for HCC every 6 months after SVR 12 evaluation (as he has F3 fibrosis)
select_one yesno
hcv_con_1
HCCON1: Explain the disease, purpose, and benefits of treatment
select_one yesno
hcv_con_2
HCCON2: Importance of adherence and side effect awareness
select_one yesno
hcv_con_3
HCCON3: Prevent reinfection
select_one yesno
hcv_con_4
HCCON4: Screen spouse and child
select_one yesno
hcv_con_5
HCCON5: Importance of seeking health services earlier and awareness of utilizing unstandardized traditional medicine
select_one yesno
hcv_t_p_1
HCT1: Eligible for DAA therapy: SOF/VEL or SOF+DAC for 12 weeks
select_one yesno
hcv_m_p_1
HCM1: After 1 month: LFTs, CBC
select_one yesno
hcv_m_p_2
HCM2: SVR12: HCV RNA, fibrosis, AFP, ultrasound, LFT, CBC
select_one yesno
hcv_m_p_3
HCM3: Screen for HCC every 6 months after SVR 12 evaluation (as he has F3 fibrosis)
select_one yesno
hcv_con_p_1
HCCON1: Explain the disease, purpose, and benefits of treatment
select_one yesno
hcv_con_p_2
HCCON2: Importance of adherence and side effect awareness
select_one yesno
hcv_con_p_3
HCCON3: Prevent reinfection
select_one yesno
hcv_con_p_4
HCCON4: Screen spouse and child
select_one yesno
hcv_con_p_5
HCCON5: Importance of seeking health services earlier and awareness of utilizing unstandardized traditional medicine
end group

begin group
arv
select_one yesno
arv_h_1
HCAH1: Have you had any symptoms recently?
select_one yesno
arv_h_2
HCAH2: Since when have you experienced those symptoms?
select_one yesno
arv_h_3
HCAH3: Do you experience a fever?
select_one yesno
arv_h_4
HCAH4: Do you experience leg edema?
select_one yesno
arv_h_5
HCAH5: Do you experience bleeding?
select_one yesno
arv_h_6
HCAH6: How about your urine color?
select_one yesno
arv_h_7
HCAH7: How about your appetite?
select_one yesno
arv_h_8
HCAH8: Do you have diarrhea?
select_one yesno
arv_h_9
HCAH9: Do you have a chronic productive cough?
select_one yesno
arv_h_10
HCAH10: Since when have you been taking ARV treatment?
select_one yesno
arv_h_11
HCAH11: What regimen that you take?
select_one yesno
arv_h_12
HCAH12: Are you taking your HIV treatment regularly?
select_one yesno
arv_h_13
HCAH13: Do you have a history of liver disease?
select_one yesno
arv_h_14
HCAH14: Besides that, did you take other laboratory tests such as an HCV RNA test?
select_one yesno
arv_h_15
HCAH15: Did you take any antiviral or hepatitis medication?
select_one yesno
arv_h_16
HCAH16: Do you drink alcohol?
select_one yesno
arv_h_17
HCAH17: Do you have a history of using injection drugs?
select_one yesno
arv_h_18
HCAH18: Do you have any family members with a history of liver cancer or Hepatitis B, or C?
select_one yesno
arv_h_19
HCAH19: Have your family members been tested for hepatitis?
select_one yesno
arv_ce_1
HCACE1: Patient is Alert
select_one yesno
arv_ce_2
HCACE2: Extremities
select_one yesno
arv_ce_3
HCACE3: Abdominal examination
select_one yesno
arv_lt_1
HCALT1: CBC: PLT
select_one yesno
arv_lt_2
HCALT2: CBC: HGB
select_one yesno
arv_lt_3
HCALT3: Hepatitis B: HBeAg
select_one yesno
arv_lt_4
HCALT4: Hepatitis B: HBV DNA
select_one yesno
arv_lt_5
HCALT5: Liver Enzyme: AST/ALT
select_one yesno
arv_lt_6
HCALT6: Liver Function: total bilirubin
select_one yesno
arv_lt_7
HCALT7: Liver Function: albumin
select_one yesno
arv_lt_8
HCALT8: CD4
select_one yesno
arv_lt_9
HCALT9: Creatinine
select_one yesno
arv_lt_10
HCALT10: HIV
select_one yesno
arv_lt_11
HCALT11: Ultrasound
select_one yesno
arv_lt_12
HCALT11: Hepatitis C: HCV RNA
select_one yesno
arv_lt_13
HCALT12: Offered any other laboratory tests?
select_one yesno
arv_d_1
HCAD: correctly diagnose Chronic viremic HCV infection, co-infected with HBV and HIV, compensated liver cirrhosis?
select_one yesno
arv_d_2
HCAD: correctly diagnose Chronic viremic HCV infection?
select_one yesno
arv_d_3
HCAD: correctly diagnose co-infected with HBV?
select_one yesno
arv_d_4
HCAD: correctly diagnose co-infected with HIV?
select_one yesno
arv_d_5
HCAD: correctly diagnose compensated liver cirrhosis?
select_one yesno
arv_t_1
HCAT1: Continue ART (switch from TDF/3TC/EFV to TDF/3TC/DTG (TLD) regimen)
select_one yesno
arv_t_2
HCAT2: Begin SOF + DAC x 24 weeks
select_one yesno
arv_m_1
HCAM1: 4-week follow-up: LFTs, CBC, creatinine
select_one yesno
arv_m_2
HCAM2: SVR12 testing after 12 weeks post-treatment
select_one yesno
arv_m_3
HCAM3: Continue HCC screening every 6 months
select_one yesno
arv_con_1
HCACON1: Explain the disease, purpose, and benefits of treatment
select_one yesno
arv_con_2
HCACON2: Importance of adherence to ARV and DAA
select_one yesno
arv_con_3
HCACON3: Monitor for interactions and side effects
select_one yesno
arv_con_4
HCACON4: Encourage partner and family testing
select_one yesno
arv_con_5
HCACON5: Emphasize a healthy lifestyle and prevention of reinfection
select_one yesno
arv_t_p_1
HCAT1: Continue ART (switch from TDF/3TC/EFV to TDF/3TC/DTG (TLD) regimen)
select_one yesno
arv_t_p_2
HCAT2: Begin SOF + DAC x 24 weeks
select_one yesno
arv_m_p_1
HCAM1: 4-week follow-up: LFTs, CBC, creatinine
select_one yesno
arv_m_p_2
HCAM2: SVR12 testing after 12 weeks post-treatment
select_one yesno
arv_m_p_3
HCAM3: Continue HCC screening every 6 months
select_one yesno
arv_con_p_1
HCACON1: Explain the disease, purpose, and benefits of treatment
select_one yesno
arv_con_p_2
HCACON2: Importance of adherence to ARV and DAA
select_one yesno
arv_con_p_3
HCACON3: Monitor for interactions and side effects
select_one yesno
arv_con_p_4
HCACON4: Encourage partner and family testing
select_one yesno
arv_con_p_5
HCACON5: Emphasize a healthy lifestyle and prevention of reinfection
end group

begin group
ce
select_one yesno
ce_1
CE1: Temperature
select_one yesno
ce_2
CE2: Blood Pressure
select_one yesno
ce_3
CE3: Pulse
select_one yesno
ce_4
CE4: Respiration
select_one yesno
ce_5
CE5: Pulse Oximeter
select_one yesno
ce_6
CE6: Head and Neck
select_one yesno
ce_7
CE7: Respiratory Exam
end group
"""

# ==========================================
# 2. OUTPUT DIRECTORY
# ==========================================
OUTPUT_DIR = "."

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def get_variable_prefix(var_name):
    if not var_name: return None
    return var_name.split('_')[0]

def categorize_variable(var_name, prefix):
    # Special: Exclude 'referral' from standard lists (it is removed or handled specifically)
    # UNLESS it ends with _referral_p (Final Counseling)
    if "referral" in var_name and not var_name.endswith("referral_p"):
        return "skip"
    
    # Remove prefix from the check
    if len(var_name) <= len(prefix)+1:
        return "other"
    suffix = var_name[len(prefix)+1:] 
    
    # Check sections based on string patterns (Longest matches first)
    if "_t_p_" in var_name: return "t_p"
    if "_m_p_" in var_name: return "m_p"
    if "_con_p_" in var_name: return "con_p"
    if var_name.endswith("referral_p"): return "con_p" # Final Referral -> Final Counseling
    
    if "_h_" in var_name: return "h"
    if "_lt_" in var_name: return "lt"
    if "_d" in var_name or "_diag" in var_name: return "d"
    if "_t_" in var_name: return "t"
    if "_m_" in var_name: return "m"
    if "_con_" in var_name: return "con"
    
    if "_ce_" in var_name: return "ce" # Condition specific clinical exams
    
    return "other"

def clean_label(var_name, label):
    """
    Removes the ID prefix from the label text.
    Examples:
      'PH1: What symptoms?' -> 'What symptoms?'
      'CE5: Pulse Oximeter' -> 'Pulse Oximeter'
    """
    # Force fix for ce_5 specifically
    if var_name == "ce_5":
        return "Pulse Oximeter (SpO2)"

    # Regex looks for patterns like "PH1: ", "AH10: ", "HBCCE1: " at start of string
    # Matches (Start)(AlphaNumeric)(Colon)(Whitespace)
    cleaned = re.sub(r'^[A-Z0-9a-z]+:\s*', '', label)
    
    return cleaned

def parse_raw_data(raw_data):
    groups = {}
    lines = raw_data.strip().split('\n')
    current_group = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("begin group"):
            if i + 1 < len(lines):
                current_group = lines[i+1].strip()
                groups[current_group] = []
                i += 2
                continue
        
        if line == "select_one yesno":
            if i + 1 < len(lines):
                var_name = lines[i+1].strip()
                if i + 2 < len(lines):
                    label = lines[i+2].strip()
                    if current_group:
                        groups[current_group].append((var_name, label))
                    i += 3
                    continue
        
        i += 1
    return groups

# ==========================================
# 4. TEMPLATE DEFINITION
# ==========================================
PROMPT_TEMPLATE_STR = '''PROMPT_TEMPLATE = """You are an expert medical quality assurance auditor. Your task is to review a transcript of a doctor-patient interaction and evaluate whether specific clinical actions were taken based on a provided checklist.

### INSTRUCTIONS
1. **Review the Transcript:** Read the provided transcript carefully. It contains "User inputs" (the doctor's questions and orders during the consultation) and structured fields like "Diagnosis", "Treatment", and "Treatment_Post" (the final care plan).
2. **Evaluate the Checklist:** For each item in the checklist below, determine if the action was performed.
\u00A0 \u00A0- **Semantic Matching:** The exact wording does not need to match. If the provider asks a question or gives an order that carries the same meaning as the checklist item, mark it as 1 (Yes).
\u00A0 \u00A0- **History Questions (`{prefix}_h_*`):** Look primarily in the "User inputs" section for questions asked by the doctor.
\u00A0 \u00A0- **Labs/Exams (`{prefix}_lt_*`, `ce_*`):** Look in "User inputs" for tests ordered or physical exams performed.
\u00A0 \u00A0- **Diagnosis (`{prefix}_d`):** Check the "Diagnosis" field in the transcript.
\u00A0 \u00A0- **Treatment (`{prefix}_t_*`):** Check the "Treatment" field in the transcript.
\u00A0 \u00A0- **Counseling (`{prefix}_con_*`):** Check "User inputs" for verbal advice OR the "Treatment" field.
\u00A0 \u00A0- **Final Treatment (`{prefix}_t_p_*`):** Check the "Treatment_Post" field in the transcript.
\u00A0 \u00A0- **Final Counseling (`{prefix}_con_p_*`):** Check the "Treatment_Post" field or implied final advice.
3. **Output Format:** You must output strictly valid JSON. Do not include markdown formatting (like ```json).

### THE CHECKLIST
Evaluate the transcript against these variables:

{checklist_body}

**Clinical Exams (Did the provider order/check...?)**
{clinical_exams_body}

### TRANSCRIPT TO EVALUATE
{{{{INSERT_TRANSCRIPT_TEXT_HERE}}}}

### REQUIRED OUTPUT FORMAT
{{
\u00A0 "results": [
{json_output_body}
\u00A0 \u00A0 ... (repeat for all variables in checklist)
\u00A0 ]
}}
"""
'''

# ==========================================
# 5. GENERATOR LOGIC
# ==========================================

def generate_files():
    data = parse_raw_data(RAW_DATA)
    
    # Extract general clinical exams (ce)
    general_ce_items = []
    if 'ce' in data:
        # Pre-clean labels for general CE items
        general_ce_items = [(v, clean_label(v, l)) for v, l in data['ce']]
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "__init__.py"), "w") as f: pass

    # Iterate through all condition groups
    for group_name, items in data.items():
        if group_name == 'ce':
            continue 
            
        if not items:
            continue
            
        # Determine prefix from the first item
        first_var = items[0][0]
        prefix = get_variable_prefix(first_var)
        
        print(f"Generating prompt for: {group_name} (Prefix: {prefix})")
        
        # Buckets for sections
        sections = {
            "h": [], "lt": [], "d": [], 
            "t": [], "m": [], "con": [], 
            "t_p": [], "m_p": [], "con_p": [],
            "ce": [] 
        }
        
        # Sort items into sections and CLEAN LABELS
        for var_name, label in items:
            cat = categorize_variable(var_name, prefix)
            
            if cat == "skip":
                continue
                
            if cat in sections:
                cleaned_l = clean_label(var_name, label)
                sections[cat].append((var_name, cleaned_l))
        
        # --- Build Checklist Text ---
        checklist_parts = []
        
        if sections['h']:
            checklist_parts.append("**History (Did the provider ask...?)**")
            for v, l in sections['h']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")
            
        if sections['lt']:
            checklist_parts.append("**Laboratory Tests (Did the provider order...?)**")
            for v, l in sections['lt']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")

        if sections['d']:
            checklist_parts.append("**Diagnosis**")
            for v, l in sections['d']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")
            
        if sections['t']:
            checklist_parts.append("**Treatment (Did the provider order in the 'Treatment' section?)**")
            for v, l in sections['t']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")
            
        if sections['m']:
            checklist_parts.append("**Monitoring (Did the provider mention...?)**")
            for v, l in sections['m']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")
            
        if sections['con']:
            checklist_parts.append("**Counseling (Did the provider mention...?)**")
            for v, l in sections['con']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")

        if sections['t_p']:
            checklist_parts.append("**Final Treatment (Did the provider order in the 'Treatment_Post' section?)**")
            for v, l in sections['t_p']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")

        if sections['m_p']:
            checklist_parts.append("**Final Monitoring (In 'Treatment_Post' context)**")
            for v, l in sections['m_p']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")

        if sections['con_p']:
            checklist_parts.append("**Final Counseling (In 'Treatment_Post' context)**")
            for v, l in sections['con_p']: checklist_parts.append(f"- `{v}`: {l}")
            checklist_parts.append("")

        # --- Build Clinical Exams Text ---
        ce_parts = []
        # Add condition specific exams first
        for v, l in sections['ce']:
            ce_parts.append(f"- `{v}`: {l}")
        # Add general exams
        for v, l in general_ce_items:
            ce_parts.append(f"- `{v}`: {l}")
            
        # --- Build JSON Output Example ---
        # Only add the VERY FIRST variable found as the example
        # Find the first available variable from any section
        example_var = ""
        if sections['h']: example_var = sections['h'][0][0]
        elif sections['lt']: example_var = sections['lt'][0][0]
        # ... add more fallbacks if needed
        
        json_output_str = ""
        if example_var:
            json_output_str = f"""\u00A0 \u00A0 {{
\u00A0 \u00A0 \u00A0 "output_variable": "{example_var}",
\u00A0 \u00A0 \u00A0 "value_type": "select_one_yesno",
\u00A0 \u00A0 \u00A0 "value": 0 or 1
\u00A0 \u00A0 }},"""

        # Assemble File Content
        file_content = PROMPT_TEMPLATE_STR.format(
            prefix=prefix,
            checklist_body="\n".join(checklist_parts),
            clinical_exams_body="\n".join(ce_parts),
            json_output_body=json_output_str
        )
        
        # Write File
        filename = f"{prefix}_prompt.py"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

    print(f"\nSuccess! All prompts generated in '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    generate_files()