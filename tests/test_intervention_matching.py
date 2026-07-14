from project_layers.interventions import SCORING_FACTORS, match_interventions
from project_layers.models import Intake, ProjectLayerDomain
from project_layers.rules import map_intake_to_domains


def base_ready_context(**overrides):
    context = {
        "treatment_stage": "Stabilization",
        "informed_choice_confirmed": True,
        "readiness_confirmed": True,
        "safety_review_completed": True,
        "medical_considerations_reviewed": True,
        "feasibility_confirmed": True,
        "environmental_barriers_addressed": True,
        "clinician_scope_confirmed": True,
        "collaborative_goal_confirmed": True,
        "pacing_choice_confirmed": True,
        "medical_referral_reason_confirmed": True,
        "client_preferred_approaches": [],
    }
    context.update(overrides)
    return context


def candidate_named(candidates, name):
    return next(candidate for candidate in candidates if candidate["approach_name"] == name)


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
        assert "prerequisites_met" in candidate
        assert "conditional_considerations" in candidate


def test_strong_domain_match_but_missing_clinician_scope_is_outside_scope():
    intake = Intake(
        presenting_concerns="Intense emotion and overwhelmed with emotion regulation skills requested.",
        client_goals="increase coping options",
    )
    activations = map_intake_to_domains(intake)

    dbt_skills = candidate_named(
        match_interventions(intake, activations, base_ready_context(clinician_scope_confirmed=False)),
        "DBT-informed skills",
    )

    assert dbt_skills["raw_score_before_prerequisites"] > 0
    assert dbt_skills["total_score"] == 0
    assert dbt_skills["eligibility_status"] == "outside_current_scope_or_setting"


def test_strong_match_with_all_prerequisites_met_is_eligible():
    intake = Intake(
        presenting_concerns="Avoid applications and feel lost after transition.",
        functional_effects="Avoids networking and stopped exercise routine.",
        client_goals="rebuild routine and increase meaningful action",
        strengths="prior routine helped",
    )
    activations = map_intake_to_domains(intake)

    behavioral_activation = candidate_named(
        match_interventions(
            intake,
            activations,
            base_ready_context(client_preferred_approaches=["Behavioral Activation"]),
        ),
        "Behavioral Activation",
    )

    assert behavioral_activation["eligibility_status"] == "eligible_for_clinician_consideration"
    assert ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT.value in behavioral_activation["why_matched"]["domains"]
    assert behavioral_activation["scoring_breakdown"]["client_preference"]["points"] == 2
    assert all(item["evidence"] for item in behavioral_activation["prerequisites_met"])


def test_medical_and_psychological_recommendations_are_shown_concurrently():
    intake = Intake(
        presenting_concerns="Worry and intense emotion while avoiding activity.",
        medications="Recent medication initiation and dosage change.",
        physical_neurological_symptoms="Chronic pain and unexplained fatigue.",
        client_goals="clarify medical context and increase coping options",
    )
    activations = map_intake_to_domains(intake)
    candidates = match_interventions(intake, activations, base_ready_context())

    medical = candidate_named(candidates, "Medical consultation or referral")
    dbt_skills = candidate_named(candidates, "DBT-informed skills")

    assert medical["why_matched"]["domains"]
    assert dbt_skills["why_matched"]["domains"]
    assert medical["eligibility_status"] in {
        "eligible_for_clinician_consideration",
        "consultation_or_referral_required",
    }
    assert dbt_skills["eligibility_status"] == "eligible_for_clinician_consideration"


def test_trauma_stabilization_available_while_trauma_processing_needs_more_information():
    intake = Intake(
        presenting_concerns="Feels unsafe, hypervigilant, overwhelmed, and needs grounding.",
        client_goals="increase present-moment safety and build regulation options",
    )
    activations = map_intake_to_domains(intake)
    candidates = match_interventions(intake, activations, base_ready_context(trauma_processing_readiness_confirmed=False))

    stabilization = candidate_named(candidates, "Trauma-informed stabilization")
    processing = candidate_named(candidates, "Trauma-focused psychotherapy")

    assert stabilization["eligibility_status"] == "eligible_for_clinician_consideration"
    assert processing["eligibility_status"] == "more_information_needed"
    assert processing["prerequisites_missing"]


def test_family_intervention_deferred_because_relational_safety_is_unclear():
    intake = Intake(
        reported_history="Family conflict and partner relationship stress.",
        environmental_factors="Home support is unclear.",
        client_goals="improve communication and reduce relational cycles",
    )
    activations = map_intake_to_domains(intake)

    family = candidate_named(
        match_interventions(intake, activations, base_ready_context(relational_safety_clarified=False)),
        "Family or systemic approaches",
    )

    assert family["eligibility_status"] == "more_information_needed"
    assert any("Relational safety" in item["label"] for item in family["prerequisites_missing"])


def test_mi_matched_only_when_specific_change_target_and_ambivalence_exist():
    no_ambivalence = Intake(client_goals="clarify priorities")
    no_ambivalence_candidates = match_interventions(no_ambivalence, map_intake_to_domains(no_ambivalence), base_ready_context())
    mi_without = candidate_named(no_ambivalence_candidates, "Motivational Interviewing")

    with_ambivalence = Intake(
        presenting_concerns="Part of me wants to change avoidance and part of me is torn because it is hard to change.",
        client_goals="specific change target is to reduce avoidance while respecting ambivalence",
    )
    with_ambivalence_candidates = match_interventions(with_ambivalence, map_intake_to_domains(with_ambivalence), base_ready_context())
    mi_with = candidate_named(with_ambivalence_candidates, "Motivational Interviewing")

    assert mi_without["eligibility_status"] == "more_information_needed"
    assert mi_with["eligibility_status"] == "eligible_for_clinician_consideration"


def test_comprehensive_dbt_blocked_when_only_dbt_informed_skills_are_available():
    intake = Intake(
        presenting_concerns="Intense emotion and repeated crisis patterns; wants skills.",
        client_goals="increase coping options",
    )
    activations = map_intake_to_domains(intake)
    candidates = match_interventions(intake, activations, base_ready_context(comprehensive_dbt_available=False))

    dbt_skills = candidate_named(candidates, "DBT-informed skills")
    comprehensive = candidate_named(candidates, "Comprehensive DBT")

    assert dbt_skills["eligibility_status"] == "eligible_for_clinician_consideration"
    assert comprehensive["eligibility_status"] == "more_information_needed"
    assert comprehensive["total_score"] == 0


def test_missing_information_displayed_rather_than_treated_as_contraindication():
    intake = Intake(presenting_concerns="Worry and avoidance are present.")
    activations = map_intake_to_domains(intake)

    cbt = candidate_named(match_interventions(intake, activations, context={}), "CBT")

    assert cbt["eligibility_status"] in {"outside_current_scope_or_setting", "more_information_needed"}
    assert cbt["prerequisites_missing"]
    assert cbt["clarification_questions"]
    assert not any("contraindication" in question.lower() for question in cbt["clarification_questions"])
