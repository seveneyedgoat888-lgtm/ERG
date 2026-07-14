# User Flow

## Persistent interface elements

Every screen should show:

- Synthetic-case badge.
- Decision-support disclaimer.
- Current case label.
- Rule-library version.
- Safety sidebar with emergency-procedure reminder.
- Clinician approval progress.

## Flow 1: Start or load synthetic case

1. Clinician selects a synthetic demonstration case or creates a new synthetic case.
2. The app displays a reminder not to enter real identifying information.
3. Clinician confirms that the case is synthetic.

## Flow 2: Structured intake

1. Clinician completes structured fields across concerns, goals, strengths, risks, medical/physiological context, environment, relationships, cognition, emotion regulation, behavior patterns, identity, and executive functioning.
2. App validates required fields.
3. App flags possible identifiers.
4. Clinician saves intake and starts Project Layers mapping.

## Flow 3: Project Layers system-impact mapping

1. App converts intake fields into entered facts.
2. Explicit rules map facts to Project Layers domains.
3. Clinician sees the thirteen domains with activation status.
4. Clinician expands each activated domain to inspect supporting facts, matched rules, rationale, and uncertainty notes.

## Flow 4: Evidence review

1. Clinician reviews evidence grouped by domain, rule, or intake section.
2. Clinician can mark evidence as clinically relevant, needs clarification, or not applicable.
3. App preserves the original fact-to-rule trace.

## Flow 5: Medical/referral considerations

1. App displays red-flag categories and any triggered referral considerations.
2. Each item uses cautious language such as “consider assessment,” “clarify,” or “consult/refer as clinically indicated.”
3. Emergency or imminent safety concerns display established emergency-procedure reminders.
4. Clinician can add a clinician-defined referral trigger.

## Flow 6: Missing information

1. App lists missing-information questions from safety rules, formulation rules, and intervention prerequisites.
2. Questions are grouped as safety-critical, treatment-relevant, or formulation-enhancing.
3. Clinician marks each as answered, deferred, not applicable, or open.

## Flow 7: Provisional maintaining-cycle formulation

1. App drafts a provisional formulation using activated domains and evidence.
2. Clinician reviews contextual factors, current stressors, maintaining cycles, protective factors, medical/referral considerations, and initial targets.
3. Clinician edits the formulation directly.

## Flow 8: Ranked therapeutic approaches

1. App matches activated domains and facts to curated intervention library items.
2. App ranks suggestions using visible rule-based logic.
3. Clinician reviews each suggestion’s target, approach, example intervention, evidence/source field, why suggested, cautions, contraindications, stage requirements, and scope notes.
4. Clinician edits, reorders, approves, or excludes suggestions.

## Flow 9: Session-use guidance

1. App provides clinician-facing guidance for discussing the formulation collaboratively.
2. Guidance highlights unresolved safety questions, stage requirements, and suggested sequencing.
3. Clinician adapts or removes guidance.

## Flow 10: Clinician review and approval

1. App shows generated content beside clinician-edited content.
2. Clinician confirms evidence review, safety/referral review, scope acknowledgement, and recommendation approval.
3. Export remains disabled until required approvals are complete.

## Flow 11: Export formulation summary

1. Clinician previews the export.
2. App includes disclaimers, synthetic-case label, approved formulation, approved recommendations, medical/referral considerations, missing questions, cautions, contraindications, and scope notes.
3. Clinician exports Markdown and, if approved for version 1, JSON.
