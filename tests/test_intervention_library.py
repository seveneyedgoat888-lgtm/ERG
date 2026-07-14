import json
from pathlib import Path

LIBRARY_PATH = Path("data/intervention_library.json")

REQUIRED_FIELDS = {
    "approach_name",
    "description",
    "target_domains",
    "target_processes",
    "treatment_stage",
    "client_goals",
    "universal_review_gates",
    "approach_specific_prerequisites",
    "conditional_considerations",
    "priority_shifting_or_referral_conditions",
    "scope_or_setting_requirements",
    "application_guidance",
    "example_questions",
    "example_exercises",
    "cautions",
    "contraindication_or_referral_considerations",
    "setting_limitations",
    "clinician_scope_notes",
    "evidence_source_placeholder",
    "clinical_review_status",
    "clinician_review_required",
}

EXPECTED_APPROACHES = {
    "DBT-informed skills",
    "Comprehensive DBT",
    "Mentalization-Based Treatment or MBT-informed work",
    "CBT",
    "ACT",
    "Behavioral Activation",
    "Motivational Interviewing",
    "Attachment-informed therapy",
    "Trauma-informed stabilization",
    "Trauma-focused psychotherapy",
    "Family or systemic approaches",
    "Case-management/environmental interventions",
    "Medical consultation or referral",
}

FRAMEWORK_KEYS = {
    "universal_review_gates",
    "approach_specific_prerequisites",
    "conditional_considerations",
    "priority_shifting_or_referral_conditions",
}


def load_library():
    with LIBRARY_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def test_intervention_library_contains_required_placeholder_approaches():
    library = load_library()
    names = {entry["approach_name"] for entry in library}

    assert names == EXPECTED_APPROACHES


def test_intervention_library_entries_have_transparent_prerequisite_framework():
    for entry in load_library():
        assert set(entry) == REQUIRED_FIELDS
        assert FRAMEWORK_KEYS.issubset(entry)
        assert entry["clinician_review_required"] is True
        assert entry["clinical_review_status"] == "pending qualified clinical review"
        assert "pending qualified clinical review" in entry["evidence_source_placeholder"]
        assert "citation invented" in entry["evidence_source_placeholder"]
        assert entry["target_domains"]
        assert entry["target_processes"]
        assert entry["scope_or_setting_requirements"]
        assert entry["conditional_considerations"]
        assert entry["priority_shifting_or_referral_conditions"]
        for prerequisite in entry["universal_review_gates"] + entry["approach_specific_prerequisites"]:
            assert prerequisite["required_evidence_source"] in {
                "intake fact",
                "domain activation",
                "clinician confirmation",
                "client preference",
            }
            assert prerequisite["clarification_questions"]
