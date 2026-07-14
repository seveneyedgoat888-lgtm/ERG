# Data Model

## Storage and validation approach

Version 1 should use Pydantic models for validation and SQLite for local prototype persistence. Data structures must preserve traceability from intake facts to Project Layers activations, formulation content, recommendations, clinician edits, approvals, and exports.

## Primary entities

### CaseRecord

Represents one synthetic demonstration case.

Fields:

- `case_id`
- `case_label`
- `synthetic = true`
- `created_at`
- `updated_at`
- `intake_id`
- `rule_library_version`
- `intervention_library_version`

Validation:

- `synthetic` must be true.
- Case label must not contain obvious identifiers.

### Intake

Structured case input.

Fields:

- `presenting_concerns`
- `goals`
- `strengths`
- `risk_context`
- `medical_physiological_context`
- `sleep_context`
- `medication_context`
- `substance_context`
- `environmental_social_context`
- `relational_attachment_context`
- `cognition_meaning_schema_context`
- `emotion_regulation_context`
- `behavior_reinforcement_avoidance_context`
- `identity_self_continuity_context`
- `executive_functioning_context`
- `clinician_notes`

### EnteredFact

Canonical fact created from intake fields and used by the rule engine.

Fields:

- `fact_id`
- `case_id`
- `source_section`
- `field_name`
- `display_label`
- `value`
- `timeframe`
- `severity_or_salience`
- `client_reported`
- `clinician_observed`
- `safety_sensitive`
- `possible_identifier_flag`

### ProjectLayerDomain

Controlled vocabulary for the thirteen Project Layers domains.

Fields:

- `domain_id`
- `name`
- `definition`
- `display_order`

### RuleDefinition

Clinician-reviewable local rule.

Fields:

- `rule_id`
- `version`
- `description`
- `conditions`
- `activated_domains`
- `activation_label`
- `rationale_template`
- `missing_information_prompts`
- `medical_referral_consideration`
- `cautions`
- `active`

### DomainActivation

Result of applying rules to entered facts.

Fields:

- `activation_id`
- `case_id`
- `domain_id`
- `activation_label`
- `matched_rule_ids`
- `supporting_fact_ids`
- `rationale`
- `uncertainty_notes`
- `safety_notes`
- `clinician_edit`

### MissingInformationQuestion

Question generated from rules, safety checks, or intervention prerequisites.

Fields:

- `question_id`
- `case_id`
- `question_text`
- `reason_generated`
- `related_domain_ids`
- `related_rule_ids`
- `priority`: `safety_critical`, `treatment_relevant`, or `formulation_enhancing`
- `clinician_status`: `open`, `answered`, `deferred`, or `not_applicable`

### ReferralConsideration

Non-diagnostic medical or referral consideration.

Fields:

- `consideration_id`
- `case_id`
- `category`
- `supporting_fact_ids`
- `suggested_language`
- `emergency_reminder_required`
- `clinician_status`
- `clinician_notes`

### FormulationDraft

Generated and clinician-edited formulation.

Fields:

- `formulation_id`
- `case_id`
- `generated_contextual_factors`
- `generated_precipitating_factors`
- `generated_maintaining_cycles`
- `generated_protective_factors`
- `generated_initial_targets`
- `generated_scope_note`
- `clinician_revision`
- `approval_status`

### InterventionLibraryItem

Curated local therapeutic approach entry.

Fields:

- `item_id`
- `approach_name`
- `treatment_target`
- `intervention_example`
- `evidence_source`
- `indicated_domains`
- `indicated_fact_patterns`
- `stage_requirements`
- `cautions`
- `contraindications`
- `scope_notes`
- `active`

### RecommendationResult

Case-specific ranked suggestion.

Fields:

- `recommendation_id`
- `case_id`
- `library_item_id`
- `rank`
- `rank_explanation`
- `matched_domain_ids`
- `matched_fact_ids`
- `why_suggested`
- `cautions`
- `contraindications`
- `stage_requirements`
- `clinician_status`: `draft`, `edited`, `approved`, or `excluded`
- `clinician_notes`

### ClinicianApproval

Approval gate for export.

Fields:

- `approval_id`
- `case_id`
- `approved_by_label`
- `approved_at`
- `formulation_approved`
- `recommendations_approved`
- `safety_review_acknowledged`
- `scope_acknowledged`
- `export_ready`

### ExportRecord

Saved export metadata.

Fields:

- `export_id`
- `case_id`
- `exported_at`
- `format`
- `content_hash`
- `included_recommendation_ids`
- `rule_library_version`
- `intervention_library_version`

## Suggested SQLite tables

- `case_records`
- `intakes`
- `entered_facts`
- `project_layer_domains`
- `rule_definitions`
- `domain_activations`
- `domain_activation_facts`
- `missing_information_questions`
- `referral_considerations`
- `formulation_drafts`
- `intervention_library_items`
- `recommendation_results`
- `recommendation_facts`
- `clinician_approvals`
- `export_records`

## Audit requirements

- Domain activations must reference facts and rules.
- Recommendations must reference facts, domains, and library items.
- Exports must reference approved formulation and approved recommendations.
- Clinician edits must be stored separately from generated draft text.
