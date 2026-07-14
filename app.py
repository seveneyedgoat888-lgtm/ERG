"""Streamlit intake page for the Project Layers vertical slice."""

from __future__ import annotations

import streamlit as st

from project_layers.demo_data import load_demo_cases
from project_layers.models import Intake
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

st.info("Treatment recommendations are intentionally not implemented in this vertical slice.")
