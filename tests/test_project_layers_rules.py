from project_layers.demo_data import load_demo_cases
from project_layers.models import ConfidenceLevel, Intake, ProjectLayerDomain
from project_layers.rules import RULES, map_intake_to_domains, medical_considerations


def domains_for(intake: Intake) -> set[ProjectLayerDomain]:
    return {activation.domain for activation in map_intake_to_domains(intake)}


def test_demo_cases_are_synthetic_and_loadable():
    cases = load_demo_cases()

    assert len(cases) == 3
    assert all(case.synthetic for case in cases)


def test_demo_cases_activate_expected_domains():
    case_domains = {case.case_id: domains_for(case.intake) for case in load_demo_cases()}

    assert ProjectLayerDomain.ALLOSTATIC_LOAD in case_domains["demo-001"]
    assert ProjectLayerDomain.EXECUTIVE_FUNCTIONING in case_domains["demo-001"]
    assert ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL in case_domains["demo-002"]
    assert ProjectLayerDomain.SALIENCE_THREAT in case_domains["demo-002"]
    assert ProjectLayerDomain.IDENTITY_CONTINUITY in case_domains["demo-003"]
    assert ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT in case_domains["demo-003"]


def test_every_rule_maps_to_its_domain_with_required_transparency_fields():
    for rule in RULES:
        payload = {field: "" for field in Intake.model_fields}
        payload[rule.fields[0]] = f"Synthetic fact mentioning {rule.terms[0]}."
        activations = map_intake_to_domains(Intake.model_validate(payload))
        activation = next((item for item in activations if item.domain == rule.domain), None)

        assert activation is not None, rule.rule_id
        assert activation.confidence in {ConfidenceLevel.LOW, ConfidenceLevel.MODERATE, ConfidenceLevel.HIGH}
        assert activation.reported_facts == [payload[rule.fields[0]]]
        assert activation.missing_clarification_questions
        assert activation.alternative_explanations
        assert activation.caution
        assert any(match.rule_id == rule.rule_id for match in activation.rule_matches)


def test_confidence_increases_with_multiple_facts_and_terms():
    intake = Intake(
        sleep="Severe sleep loss and insomnia.",
        medications="Medication dose change.",
        physical_neurological_symptoms="Head injury and seizure-like event.",
    )

    activation = next(
        item for item in map_intake_to_domains(intake)
        if item.domain == ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL
    )

    assert activation.confidence == ConfidenceLevel.HIGH
    assert len(activation.reported_facts) == 3


def test_medical_considerations_use_cautious_language_without_causality_claim():
    intake = Intake(medications="Recent medication initiation and dose change.")
    activations = map_intake_to_domains(intake)
    panel = " ".join(medical_considerations(activations))

    assert "Consider further assessment." in panel
    assert "Clarify medical history." in panel
    assert "Coordinate with a medical provider as clinically indicated." in panel
    assert "is medically caused" not in panel
