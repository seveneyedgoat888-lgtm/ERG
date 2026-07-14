from project_layers.interventions import SCORING_FACTORS, match_interventions
from project_layers.models import Intake, ProjectLayerDomain
from project_layers.rules import map_intake_to_domains


def base_ready_context(**overrides):
    context = {
        "treatment_stage": "Stabilization",
        "readiness_confirmed": True,
        "safety_review_completed": True,
        "medical_considerations_reviewed": True,
        "feasibility_confirmed": True,
        "environmental_barriers_addressed": True,
        "clinician_scope_confirmed": True,
        "client_preferred_approaches": [],
    }
    context.update(overrides)
    return context


def test_matching_displays_complete_scoring_breakdown_for_each_candidate():
    intake = Intake(
        presenting_concerns="Overwhelmed with intense emotion and worry.",
        client_goals="increase coping options and reconnect with values",
        strengths="support and values are important",
    )
    activations = map_intake_to_domains(intake)

    candidates = match_interventions(intake, activations, base_ready_context())

    assert candidates
    for candidate in candidates:
        assert set(candidate["scoring_breakdown"]) == set(SCORING_FACTORS)
        assert candidate["why_matched"]
        assert "intervention" in candidate


def test_missing_prerequisites_block_recommendation_and_show_missing_items():
    intake = Intake(
        medications="Recent medication initiation and dosage change.",
        physical_neurological_symptoms="Chronic pain and unexplained fatigue.",
        client_goals="clarify medical context",
    )
    activations = map_intake_to_domains(intake)

    candidates = match_interventions(intake, activations, context={})

    assert all(candidate["status"] == "missing_prerequisites" for candidate in candidates)
    assert all(candidate["total_score"] == 0 for candidate in candidates)
    assert all(candidate["missing_prerequisites"] for candidate in candidates)


def test_domain_goal_and_preference_increase_matching_score_when_prerequisites_met():
    intake = Intake(
        presenting_concerns="Avoid applications and feel lost after transition.",
        functional_effects="Avoids networking and stopped exercise routine.",
        client_goals="rebuild routine and increase meaningful action",
        strengths="prior routine helped",
    )
    activations = map_intake_to_domains(intake)

    candidates = match_interventions(
        intake,
        activations,
        base_ready_context(client_preferred_approaches=["Behavioral Activation"]),
    )
    behavioral_activation = next(candidate for candidate in candidates if candidate["approach_name"] == "Behavioral Activation")

    assert behavioral_activation["status"] == "candidate"
    assert ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT.value in behavioral_activation["why_matched"]["domains"]
    assert behavioral_activation["scoring_breakdown"]["client_preference"]["points"] == 2
    assert behavioral_activation["scoring_breakdown"]["client_stated_goal"]["points"] > 0
