# Safety Requirements

## Safety position

This application is clinician-facing decision support. It must not diagnose, prescribe, replace clinical judgment, or claim that a medical or psychological cause has been confirmed or ruled out.

## Required global language

Display these concepts throughout the app and in exports:

- Decision support only.
- For licensed or supervised behavioral health clinicians.
- Synthetic cases only in version 1.
- Not a diagnosis, prescription, or substitute for clinical judgment.
- Use established emergency procedures for emergencies or imminent safety concerns.
- Consider assessment, clarification, consultation, or referral as clinically indicated.

## Medical/referral consideration categories

The structured intake and rule library must include medical/referral consideration handling for:

- Sudden change in personality or functioning.
- Acute confusion or delirium.
- Neurological symptoms.
- Medication initiation, withdrawal, or dosage changes.
- Substance use, intoxication, or withdrawal.
- Severe or prolonged sleep loss.
- Endocrine or metabolic concerns.
- Chronic pain.
- Nutritional concerns.
- Unexplained fatigue.
- Head injury.
- Seizure-like events.
- Infection or systemic illness.
- Reproductive or hormonal changes.
- Cognitive decline.
- Physical symptoms temporally linked to emotional changes.
- Clinician-defined referral triggers.
- Emergency or imminent safety concerns.

These categories should be treated as prompts to consider clarification, assessment, coordination, or referral as clinically indicated. They are not diagnostic conclusions.

## Required medical/referral consideration behavior

When a medical/referral consideration or red flag is present, the application must:

1. Show the supporting entered facts.
2. Display cautious language such as “Consider further assessment,” “Clarify medical history,” or “Coordinate with a medical provider as clinically indicated.”
3. Avoid naming a diagnosis.
4. Avoid stating or implying “This symptom is medically caused.”
5. Avoid telling the clinician that referral is unnecessary.
6. Display emergency-procedure reminders when imminent danger or possible medical emergency is indicated.
7. Preserve the item for clinician review and approval.

## Prohibited output patterns

Generated text must not say or imply:

- “This is caused by…”
- “This symptom is medically caused.”
- “This confirms…”
- “This rules out…”
- “The client has [diagnosis].”
- “Prescribe, discontinue, increase, decrease, or change medication.”
- “No medical assessment is needed.”
- “This treatment is indicated with certainty.”
- “The client is safe” without clinician determination.

## Recommendation safeguards

- Medical referral considerations must be visibly separated from psychotherapy approach suggestions.
- Treatment suggestions must include cautions, contraindications, scope notes, and treatment-stage requirements.
- Potential trauma-processing, exposure, or intensive emotion-activation approaches must include readiness/stabilization checks.
- Recommendations must remain editable, excludable, and approval-gated.
- Rankings must be explained by visible rules and should not imply guaranteed effectiveness.

## Data safety

- Do not store real client-identifying information in version 1.
- Validate or warn on possible names, addresses, dates of birth, phone numbers, email addresses, record numbers, and other identifiers.
- Label all cases and exports as synthetic.
- Keep data local by default.
- Do not transmit case data to external services.

## Safety test requirements

Automated tests should verify that:

- Red flags trigger referral-consideration language.
- Emergency reminders appear for emergency or imminent safety items.
- Prohibited diagnostic, prescriptive, and false-reassurance phrases do not appear in generated outputs.
- Recommendations cannot be exported until clinician approval is recorded.
- Every activation and recommendation includes supporting facts and rule IDs.
- Synthetic-case validation blocks or flags obvious identifiers.
