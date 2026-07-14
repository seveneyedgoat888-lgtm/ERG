# Product Requirements: Project Layers Clinical Formulation Support

## Purpose

Create a local clinician-facing prototype that uses the **Project Layers** systems model to convert structured, synthetic client-reported information into a transparent provisional formulation and ranked therapeutic approach suggestions.

The application is **decision support only**. It must not diagnose, prescribe, replace clinical judgment, or state that a medical or psychological cause has been confirmed or ruled out.

## Intended users

- Licensed behavioral health clinicians.
- Supervised behavioral health clinicians using the tool within their scope and supervision requirements.
- Clinical reviewers evaluating the prototype with synthetic demonstration cases.

## Version 1 constraints

- Synthetic cases only; no real client-identifying information.
- Runs locally.
- Uses explicit clinician-reviewable rule-based logic.
- Uses local storage only.
- Does not call external AI APIs.
- Requires clinician review and approval before export.

## Core outcomes

Version 1 must enable the clinician to:

1. Enter structured case information using synthetic examples.
2. See which Project Layers domains were activated.
3. See the entered facts and rules behind each activation.
4. Identify missing information needed for safety, formulation, or treatment planning.
5. Surface medical and referral considerations using cautious, non-diagnostic language.
6. Review a provisional maintaining-cycle formulation.
7. Review ranked therapeutic approaches with transparent rationales, cautions, contraindications, treatment-stage requirements, and scope notes.
8. Edit and approve formulation and recommendation content.
9. Export a clinician-approved formulation summary.

## Core Project Layers domains

The system must represent these domains:

- Medical and physiological contributors
- Nervous-system regulation
- Allostatic load
- Salience and threat detection
- Interpretive prism and schemas
- Meaning and cognition
- Emotion regulation
- Behavioral reinforcement and avoidance
- Identity and self-continuity
- Attachment and relational functioning
- Executive functioning
- Environmental and social conditions
- Strengths and protective factors

## Functional requirements

### Structured intake

The intake must capture:

- Presenting concerns in client language.
- Client goals and preferred outcomes.
- Strengths, resources, values, and protective factors.
- Current risks and clinician safety concerns.
- Medical and physiological factors, including sudden change in personality or functioning, acute confusion or delirium, neurological symptoms, head injury, seizure-like events, infection or systemic illness, endocrine or metabolic concerns, reproductive or hormonal changes, cognitive decline, chronic pain, nutritional concerns, unexplained fatigue, and physical symptoms temporally linked to emotional changes.
- Sleep, pain, appetite, energy, movement, and somatic concerns, including severe or prolonged sleep loss.
- Medication initiation, withdrawal, dosage changes, substance use, intoxication, possible withdrawal, and relevant medical care context.
- Environmental and social stressors or supports.
- Relationship, attachment, family, and community context.
- Cognition, meaning-making, schemas, identity, and self-continuity themes.
- Emotion regulation, behavior patterns, avoidance, reinforcement loops, and executive-functioning concerns.

### Project Layers mapping

For every activated domain, the application must show:

- Domain name.
- Activation label.
- Supporting entered facts.
- Matched rule IDs.
- Plain-language rationale.
- Uncertainty or missing-context notes.
- Safety or referral notes when applicable.

The system must not use hidden scoring. If an ordering or rank is shown, the rule contributions and ordering method must be visible.

### Provisional formulation

The formulation summary must include:

- Contextual or predisposing factors.
- Current precipitating stressors.
- Maintaining cycles.
- Strengths, protective factors, and exceptions.
- Medical/referral considerations.
- Missing-information questions.
- Initial treatment targets.
- Clinician edits and approval status.

All generated wording must be provisional and editable.

### Therapeutic approach suggestions

The recommendation library must include at minimum:

- DBT
- CBT
- ACT
- MBT
- Motivational interviewing
- Behavioral activation
- Attachment-informed therapy
- Trauma-informed stabilization
- Family/systemic approaches
- Case-management/environmental interventions
- Medical referral or consultation consideration

Each suggestion must separate:

- Treatment target.
- Approach.
- Intervention example.
- Evidence/source field.
- Why it was suggested.
- Matched Project Layers domains and facts.
- Cautions.
- Contraindications.
- Treatment-stage requirements.
- Scope notes.
- Clinician approval status.

### Export

The export must include:

- Synthetic-case label.
- Decision-support disclaimer.
- Rule-library version.
- Clinician-approved formulation.
- Approved recommendations only, unless a reviewer option includes excluded items as an audit appendix.
- Medical/referral considerations.
- Missing-information questions.
- Cautions, contraindications, and scope notes.

## Out of scope

- Diagnosing medical, psychiatric, or psychological conditions.
- Prescribing or changing medication.
- Determining causality.
- Stating that any cause has been ruled in or ruled out.
- Emergency triage as a standalone function.
- Real client records, PHI, cloud sync, EHR integration, billing, or scheduling.
- External AI calls in version 1.
