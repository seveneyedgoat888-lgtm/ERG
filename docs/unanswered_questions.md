# Unanswered Questions Requiring Human Review

## Clinical governance

1. Who is responsible for approving Project Layers domain definitions, rules, and intervention library entries?
2. What credentials or supervision structure are required for clinical reviewers?
3. How often should rules, cautions, contraindications, and evidence/source fields be reviewed?
4. What change-control process should govern updates to clinical logic?

## Safety and scope

1. What exact emergency-procedure language should be shown for the intended clinical setting?
2. Should red flags block recommendation generation, or allow recommendations with referral-first warnings?
3. Which prohibited phrases should be included in automated safety tests?
4. Should users be able to customize red-flag categories locally?
5. What should happen if a user attempts to enter real identifying information: block, warn, mask, or require acknowledgement?

## Population and setting

1. Is version 1 limited to adult individual behavioral health care?
2. Should youth, couples, families, groups, substance-use specialty care, eating-disorder specialty care, or integrated medical settings be excluded initially?
3. What assumptions should the app make about clinician training level?
4. Are there jurisdiction-specific documentation or supervision requirements to reflect?

## Intake and ontology

1. Which structured intake fields are mandatory before mapping can run?
2. Should client-reported and clinician-observed facts be modeled separately in the UI?
3. Should severity be captured categorically, numerically, or both?
4. How should cultural context, discrimination, and systemic stressors be represented to avoid individualizing environmental harms?

## Rule and ranking design

1. Should recommendation ranking use priority tiers, matched-rule counts, domain-specific decision tables, or clinician-configurable weights?
2. How should conflicting recommendations or contraindications be displayed?
3. Should unresolved medical/referral considerations suppress certain therapeutic suggestions or simply add warnings?
4. How should strengths and protective factors influence recommendations and formulation language?

## Intervention library

1. What evidence/source format is required for each approach?
2. Which contraindications and stage requirements must be mandatory for trauma-informed stabilization, exposure-like work, or intensive emotion-focused interventions?
3. Should medical referral be treated as an intervention library item, a separate referral workflow, or both?
4. Should the library include local service/resource placeholders for case-management recommendations?

## Export and audit

1. Should version 1 export Markdown only, or Markdown and JSON?
2. Should excluded recommendations appear in an audit appendix?
3. What clinician approval attestation text is required?
4. How detailed should the exported evidence appendix be?

## Technical choices

1. Should rule files be YAML, JSON, or seeded SQLite rows?
2. Should persistence use Python `sqlite3`, SQLAlchemy, SQLModel, or another lightweight layer?
3. Should migrations use plain SQL files or a migration tool?
4. Which linting, formatting, and type-checking tools should be required?
