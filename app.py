"""Streamlit intake page for the Project Layers vertical slice."""

from __future__ import annotations

import streamlit as st

from project_layers.demo_data import load_demo_cases
from project_layers.models import Intake
from project_layers.interventions import SCORING_FACTORS, match_interventions
from project_layers.models import ProjectLayerDomain
from project_layers.rules import draft_formulation, map_intake_to_domains, medical_considerations

st.set_page_config(page_title="Project Layers Prototype", layout="wide")
st.title("Project Layers Clinical Formulation Support")
st.error(
    "SYNTHETIC DATA ONLY: Do not enter real client-identifying information, PHI, names, "
    "addresses, dates of birth, phone numbers, emails, medical record numbers, or other identifiers."
)
st.warning(
    "Decision support only. Use synthetic demonstration information only. "
    "This tool does not diagnose, prescribe, replace clinical judgment, or establish medical or psychological causes."
)

cases = load_demo_cases()
case_titles = [case.title for case in cases]
selected_title = st.sidebar.selectbox("Synthetic demonstration case", case_titles)
selected_case = next(case for case in cases if case.title == selected_title)
st.sidebar.error("Synthetic data only — do not enter real client information.")
st.sidebar.info("Version 1: local rule engine, no AI model, no treatment recommendations, no secrets required.")

st.header("1. Structured synthetic intake")
st.caption("Edit these fields to test the transparent rule mapping. Do not enter real client-identifying information.")

with st.form("intake_form"):
    edited = {}
    field_labels = {
        "presenting_concerns": "Presenting concerns",
        "reported_history": "Reported history",
        "onset_duration": "Onset and duration",
        "functional_effects": "Functional effects",
        "current_stressors": "Current stressors",
        "strengths": "Strengths",
        "client_goals": "Client goals",
        "risk_information": "Risk information",
        "sleep": "Sleep",
        "medications": "Medications",
        "substance_use": "Substance use",
        "physical_neurological_symptoms": "Physical and neurological symptoms",
        "recent_medical_changes": "Recent medical changes",
        "environmental_factors": "Environmental factors",
    }
    defaults = selected_case.intake.model_dump()
    for field_name, label in field_labels.items():
        edited[field_name] = st.text_area(label, value=defaults[field_name], height=80)
    submitted = st.form_submit_button("Run Project Layers mapping")

intake = Intake.model_validate(edited if submitted else selected_case.intake.model_dump())
activations = map_intake_to_domains(intake)

st.header("2. Activated Project Layers domains")
if not activations:
    st.info("No domains activated yet. Add synthetic structured facts to run mapping.")
else:
    for activation in activations:
        with st.expander(f"{activation.domain.value} — confidence: {activation.confidence.value}", expanded=True):
            st.markdown("**Exact reported facts that activated this domain**")
            for fact in activation.reported_facts:
                st.write(f"- {fact}")
            st.markdown("**Matched transparent rules**")
            for match in activation.rule_matches:
                st.write(
                    f"- `{match.rule_id}` from `{match.field_name}`; matched terms: "
                    f"{', '.join(match.matched_terms)}. {match.rationale}"
                )
            st.markdown("**Missing clarification questions**")
            for question in activation.missing_clarification_questions:
                st.write(f"- {question}")
            st.markdown("**Alternative explanations**")
            for explanation in activation.alternative_explanations:
                st.write(f"- {explanation}")
            st.markdown("**Caution against premature conclusions**")
            st.write(activation.caution)

st.header("3. Medical consideration panel")
for item in medical_considerations(activations):
    st.write(f"- {item}")

st.header("4. Editable provisional formulation")
formulation = draft_formulation(intake, activations)
st.text_area("Clinician-editable draft", value=formulation, height=220)

st.info("The prototype provides transparent candidate-approach matching only; final treatment recommendations require clinician decision.")


def _first_fact_for(domain: ProjectLayerDomain, fallback: str) -> str:
    activation = next((item for item in activations if item.domain == domain), None)
    if activation and activation.reported_facts:
        return activation.reported_facts[0]
    return f"Hypothesis: {fallback}"


st.header("5. Working formulation and maintaining cycle")
st.subheader("Working formulation")
st.write(formulation)
st.subheader("Primary systems")
if activations:
    st.write(", ".join(activation.domain.value for activation in activations[:5]))
else:
    st.write("Hypothesis: no primary systems selected yet; add or edit intake facts.")

st.subheader("Maintaining cycle")
cycle_defaults = {
    "Trigger": _first_fact_for(ProjectLayerDomain.ALLOSTATIC_LOAD, "identify a trigger or contextual stressor"),
    "Nervous-system activation": _first_fact_for(ProjectLayerDomain.NERVOUS_SYSTEM, "clarify arousal, shutdown, or recovery pattern"),
    "Salience": _first_fact_for(ProjectLayerDomain.SALIENCE_THREAT, "clarify what becomes salient or threatening"),
    "Interpretive prism": _first_fact_for(ProjectLayerDomain.INTERPRETIVE_SCHEMAS, "clarify interpretive schema or expectation"),
    "Assigned meaning": _first_fact_for(ProjectLayerDomain.MEANING_COGNITION, "clarify meaning, appraisal, or value conflict"),
    "Emotion and cognition": _first_fact_for(ProjectLayerDomain.EMOTION_REGULATION, "clarify emotion and cognition pattern"),
    "Behavior": _first_fact_for(ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT, "clarify behavior, avoidance, or reinforcement loop"),
    "Relational or environmental consequence": _first_fact_for(ProjectLayerDomain.ATTACHMENT_RELATIONAL, "clarify relational or environmental consequence"),
    "Reinforcement": "Hypothesis: clarify the short-term relief, reward, cost, or feedback that may reinforce the loop.",
}
cycle_nodes = {}
for label, default in cycle_defaults.items():
    cycle_nodes[label] = st.text_input(label, value=default, key=f"cycle_node_{selected_case.case_id}_{label}")
st.markdown(" → ".join(f"**{label}:** {value}" for label, value in cycle_nodes.items()))

st.subheader("Missing information")
missing_questions = [question for activation in activations for question in activation.missing_clarification_questions]
for question in missing_questions or ["Hypothesis: add intake details to identify missing clarification questions."]:
    st.write(f"- {question}")

st.subheader("Medical considerations")
for item in medical_considerations(activations):
    st.write(f"- {item}")

st.subheader("Initial treatment priorities")
st.write(
    "Prototype priorities: clarify missing information, address safety and medical/referral considerations, "
    "confirm readiness and feasibility, and use clinician judgment before selecting any approach."
)

st.header("6. Candidate approaches for clinician decision")
st.caption("Transparent matching only. Scores never override hard prerequisites, priority-shifting conditions, scope limits, or clinician judgment.")

with st.form("recommendation_context"):
    treatment_stage = st.selectbox("Treatment stage", ["Stabilization", "Formulation", "Engagement", "Skills-building", "Action planning", "Comprehensive program"])
    st.markdown("**Universal review gates and confirmations**")
    informed_choice_confirmed = st.checkbox("Client preference and informed choice discussed")
    readiness_confirmed = st.checkbox("Readiness confirmed by clinician — not inferred from symptoms or diagnosis")
    safety_review_completed = st.checkbox("Safety/stabilization reviewed; use established procedures as indicated")
    medical_considerations_reviewed = st.checkbox("Medical/referral considerations reviewed as potentially concurrent")
    feasibility_confirmed = st.checkbox("Feasibility confirmed with client and setting")
    environmental_barriers_addressed = st.checkbox("Environmental barriers addressed or planned for")
    clinician_scope_confirmed = st.checkbox("Clinician competence, supervision, setting, and resource availability confirmed")
    collaborative_goal_confirmed = st.checkbox("Collaborative target or purpose identified")
    st.markdown("**Approach-specific confirmations**")
    comprehensive_dbt_available = st.checkbox("Comprehensive DBT program/team is available")
    trauma_processing_readiness_confirmed = st.checkbox("Trauma-processing readiness, stabilization, consent, and scope confirmed")
    relational_safety_clarified = st.checkbox("Relational safety, coercion, consent, and confidentiality boundaries clarified")
    pacing_choice_confirmed = st.checkbox("Client choice and pacing for stabilization confirmed")
    medical_referral_reason_confirmed = st.checkbox("Medical/referral reason or clarification need confirmed")
    st.markdown("**Priority-shifting conditions**")
    acute_safety_concerns_present = st.checkbox("Acute safety concerns may require established clinical procedures now")
    urgent_medical_referral_needed = st.checkbox("Urgent medical/referral consultation may be needed now")
    preferred = st.multiselect(
        "Client preference, if stated",
        [
            "DBT-informed skills",
            "Comprehensive DBT",
            "Mentalization-Based Treatment or MBT-informed work",
            "CBT",
            "ACT",
            "Behavioral Activation",
            "Motivational Interviewing",
            "Attachment-informed therapy",
            "Trauma-informed stabilization",
            "Family or systemic approaches",
            "Trauma-focused psychotherapy",
            "Case-management/environmental interventions",
            "Medical consultation or referral",
        ],
    )
    st.form_submit_button("Update candidate approach matching")

recommendation_context = {
    "treatment_stage": treatment_stage,
    "informed_choice_confirmed": informed_choice_confirmed,
    "readiness_confirmed": readiness_confirmed,
    "safety_review_completed": safety_review_completed,
    "medical_considerations_reviewed": medical_considerations_reviewed,
    "feasibility_confirmed": feasibility_confirmed,
    "environmental_barriers_addressed": environmental_barriers_addressed,
    "clinician_scope_confirmed": clinician_scope_confirmed,
    "collaborative_goal_confirmed": collaborative_goal_confirmed,
    "comprehensive_dbt_available": comprehensive_dbt_available,
    "trauma_processing_readiness_confirmed": trauma_processing_readiness_confirmed,
    "relational_safety_clarified": relational_safety_clarified,
    "pacing_choice_confirmed": pacing_choice_confirmed,
    "medical_referral_reason_confirmed": medical_referral_reason_confirmed,
    "acute_safety_concerns_present": acute_safety_concerns_present,
    "urgent_medical_referral_needed": urgent_medical_referral_needed,
    "client_preferred_approaches": preferred,
}
candidates = match_interventions(intake, activations, recommendation_context)

if "recommendation_decisions" not in st.session_state:
    st.session_state.recommendation_decisions = {}

for candidate in candidates:
    title = f"{candidate['approach_name']} — {candidate['eligibility_status']} — score {candidate['total_score']} (raw {candidate['raw_score_before_prerequisites']})"
    with st.expander(title):
        st.markdown(f"**Current eligibility status:** `{candidate['eligibility_status']}`")
        if candidate["priority_shifting_or_referral_conditions"]:
            st.error("Priority-shifting or referral conditions are present. A high score cannot override these conditions.")
            for condition in candidate["priority_shifting_or_referral_conditions"]:
                st.write(f"- {condition['label']}")
                st.write({"evidence": condition["evidence"]})
        if candidate["prerequisites_missing"]:
            st.warning("Missing information or unmet hard prerequisites are shown for clinician clarification; this is not automatically a contraindication.")
        st.markdown("**Prerequisites met with exact evidence**")
        for prerequisite in candidate["prerequisites_met"] or [{"label": "None documented yet", "evidence": []}]:
            st.write(f"- {prerequisite['label']}")
            st.write({"evidence": prerequisite["evidence"]})
        st.markdown("**Prerequisites missing**")
        for prerequisite in candidate["prerequisites_missing"] or [{"label": "No missing hard prerequisites documented", "clarification_questions": []}]:
            st.write(f"- {prerequisite['label']}")
        st.markdown("**Clarification questions that could resolve missing items**")
        for question in candidate["clarification_questions"] or ["No additional prerequisite clarification questions generated."]:
            st.write(f"- {question}")
        st.markdown("**Conditional considerations**")
        for consideration in candidate["conditional_considerations"]:
            st.write(f"- {consideration['label']}")
            st.write({"evidence": consideration["evidence"], "questions": consideration["clarification_questions"]})
        st.markdown("**Scope or setting requirements**")
        for item in candidate["scope_or_setting_requirements"]:
            st.write(f"- {item}")
        st.markdown("**Why this approach matched**")
        st.write(candidate["why_matched"])
        st.markdown("**Complete scoring breakdown**")
        for factor in SCORING_FACTORS:
            detail = candidate["scoring_breakdown"][factor]
            st.write(f"- {factor}: {detail['points']} point(s); details: {detail['details']}")
        st.markdown("**Example in-session applications**")
        for item in candidate["intervention"]["example_questions"]:
            st.write(f"- {item}")
        st.markdown("**Between-session options**")
        for item in candidate["intervention"]["example_exercises"]:
            st.write(f"- {item}")
        st.markdown("**Cautions and referral/scope considerations**")
        for item in candidate["intervention"]["cautions"]:
            st.write(f"- {item}")
        for item in candidate["intervention"]["contraindication_or_referral_considerations"]:
            st.write(f"- Referral/scope consideration: {item}")
        st.markdown("**Clinician decision and override**")
        decision_key = f"decision_{selected_case.case_id}_{candidate['approach_name']}"
        rationale_key = f"rationale_{selected_case.case_id}_{candidate['approach_name']}"
        override_key = f"override_{selected_case.case_id}_{candidate['approach_name']}"
        decision = st.radio(
            "Decision",
            ["needs more information", "accepted", "modified", "declined"],
            key=decision_key,
            horizontal=True,
        )
        override = st.checkbox("Clinician override of displayed eligibility status", key=override_key)
        rationale = st.text_area("Mandatory clinician rationale for decision or override", key=rationale_key)
        if override and not rationale.strip():
            st.error("Override requires a documented rationale.")
        st.session_state.recommendation_decisions[candidate["approach_name"]] = {
            "decision": decision,
            "override": override,
            "rationale": rationale,
            "eligibility_status": candidate["eligibility_status"],
        }

undecided = [name for name, value in st.session_state.recommendation_decisions.items() if not value.get("decision")]
if undecided:
    st.warning("Every candidate approach requires a clinician decision before prototype session review is complete.")
else:
    st.success("Clinician decisions are stored in Streamlit session state for this prototype session.")
