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
    "prerequisites",
    "application_guidance",
    "example_questions",
    "example_exercises",
    "cautions",
    "contraindication_or_referral_considerations",
    "setting_limitations",
    "clinician_scope_notes",
    "evidence_source_placeholder",
    "clinician_review_required",
}

EXPECTED_APPROACHES = {
    "DBT-informed interventions",
    "Mentalization-Based Treatment",
    "CBT",
    "ACT",
    "Behavioral Activation",
    "Motivational Interviewing",
    "Attachment-informed therapy",
    "Trauma-informed stabilization",
    "Family or systemic approaches",
    "Case-management and environmental interventions",
    "Medical consultation or referral",
}


def load_library():
    with LIBRARY_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def test_intervention_library_contains_required_placeholder_approaches():
    library = load_library()
    names = {entry["approach_name"] for entry in library}

    assert names == EXPECTED_APPROACHES


def test_intervention_library_entries_have_required_fields_and_review_placeholders():
    for entry in load_library():
        assert set(entry) == REQUIRED_FIELDS
        assert entry["clinician_review_required"] is True
        assert "pending human clinical review" in entry["evidence_source_placeholder"]
        assert "citation invented" in entry["evidence_source_placeholder"]
        assert entry["target_domains"]
        assert entry["target_processes"]
        assert entry["cautions"]
        assert entry["contraindication_or_referral_considerations"]
