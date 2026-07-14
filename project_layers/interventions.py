"""Transparent intervention matching for prototype session review.

This module ranks candidate approaches with explicit, inspectable factors. It does
not make treatment recommendations automatically: hard prerequisites and
priority-shifting conditions determine eligibility status before score display.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import DomainActivation, Intake, ProjectLayerDomain

INTERVENTION_LIBRARY_PATH = Path(__file__).resolve().parents[1] / "data" / "intervention_library.json"

ELIGIBILITY_STATUSES = (
    "eligible_for_clinician_consideration",
    "eligible_with_conditions",
    "more_information_needed",
    "defer_while_priority_needs_are_addressed",
    "consultation_or_referral_required",
    "outside_current_scope_or_setting",
)

SCORING_FACTORS = (
    "match_to_impacted_domains",
    "match_to_maintaining_processes",
    "client_stated_goal",
    "treatment_stage",
    "readiness",
    "safety_and_stabilization_requirements",
    "client_preference",
    "feasibility",
    "environmental_barriers",
    "clinician_setting_and_scope",
)

PROCESS_TERMS_BY_DOMAIN = {
    ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL.value: {"medical", "physiological", "sleep", "pain", "fatigue", "substance", "medication", "referral"},
    ProjectLayerDomain.NERVOUS_SYSTEM.value: {"arousal", "grounding", "stabilization", "distress tolerance", "regulation"},
    ProjectLayerDomain.ALLOSTATIC_LOAD.value: {"load reduction", "recovery", "routine", "resource", "stress"},
    ProjectLayerDomain.SALIENCE_THREAT.value: {"safety", "threat", "grounding", "stabilization", "attention"},
    ProjectLayerDomain.INTERPRETIVE_SCHEMAS.value: {"appraisal", "schema", "interpretation", "defusion"},
    ProjectLayerDomain.MEANING_COGNITION.value: {"appraisal", "values", "defusion", "problem solving", "rumination"},
    ProjectLayerDomain.EMOTION_REGULATION.value: {"emotion", "distress tolerance", "regulation", "grounding"},
    ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT.value: {"activity", "avoidance", "reinforcement", "committed action", "ambivalence", "change target"},
    ProjectLayerDomain.IDENTITY_CONTINUITY.value: {"identity", "values", "self", "committed action"},
    ProjectLayerDomain.ATTACHMENT_RELATIONAL.value: {"relational", "attachment", "communication", "mental-state", "repair", "family"},
    ProjectLayerDomain.EXECUTIVE_FUNCTIONING.value: {"task", "planning", "problem solving", "routine"},
    ProjectLayerDomain.ENVIRONMENTAL_SOCIAL.value: {"resource", "access", "barrier", "care coordination", "environmental"},
    ProjectLayerDomain.STRENGTHS_PROTECTIVE.value: {"strength", "values", "support", "community", "routine"},
}

CONTEXT_EVIDENCE_LABELS = {
    "readiness_confirmed": "Clinician confirmed readiness; not inferred from symptoms or diagnosis.",
    "safety_review_completed": "Clinician confirmed safety/stabilization review; app does not declare safe or unsafe.",
    "medical_considerations_reviewed": "Clinician confirmed medical/referral considerations reviewed as potentially concurrent.",
    "feasibility_confirmed": "Clinician confirmed feasibility with client and setting.",
    "environmental_barriers_addressed": "Clinician confirmed environmental barriers addressed or planned for.",
    "clinician_scope_confirmed": "Clinician confirmed competence, supervision, setting, and resource fit.",
    "informed_choice_confirmed": "Clinician confirmed informed choice discussion.",
    "collaborative_goal_confirmed": "Clinician confirmed a collaborative target or purpose.",
    "comprehensive_dbt_available": "Clinician confirmed comprehensive DBT program/team availability.",
    "trauma_processing_readiness_confirmed": "Clinician confirmed trauma-processing readiness, stabilization, consent, and scope without requiring diagnosis.",
    "relational_safety_clarified": "Clinician confirmed relational safety, coercion, consent, and confidentiality boundaries clarified.",
    "pacing_choice_confirmed": "Clinician confirmed client choice and pacing for stabilization.",
    "medical_referral_reason_confirmed": "Clinician confirmed a medical/referral reason or need for clarification.",
}

PREREQUISITE_CONTEXT_KEYS = {
    "informed_choice": "informed_choice_confirmed",
    "safety_review": "safety_review_completed",
    "medical_review": "medical_considerations_reviewed",
    "scope_setting_resources": "clinician_scope_confirmed",
    "collaborative_goal": "collaborative_goal_confirmed",
    "comprehensive_dbt_available": "comprehensive_dbt_available",
    "trauma_processing_readiness": "trauma_processing_readiness_confirmed",
    "relational_safety_clarified": "relational_safety_clarified",
    "pacing_choice": "pacing_choice_confirmed",
    "medical_referral_reason": "medical_referral_reason_confirmed",
}

PRIORITY_CONTEXT_KEYS = {
    "acute_safety_priority": "acute_safety_concerns_present",
    "urgent_medical_priority": "urgent_medical_referral_needed",
}


def load_intervention_library(path: Path = INTERVENTION_LIBRARY_PATH) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _activated_domain_names(activations: list[DomainActivation]) -> set[str]:
    return {activation.domain.value for activation in activations}


def _all_intake_facts(intake: Intake) -> list[dict[str, str]]:
    return [{"source": "intake fact", "field": field, "text": value} for field, value in intake.facts_by_field().items() if value]


def _evidence_from_intake(intake: Intake, terms: list[str] | set[str]) -> list[dict[str, str]]:
    evidence: list[dict[str, str]] = []
    for fact in _all_intake_facts(intake):
        lowered = fact["text"].lower()
        matched = [term for term in terms if term.lower() in lowered]
        if matched:
            evidence.append({**fact, "matched_terms": ", ".join(sorted(matched))})
    return evidence


def _domain_evidence(activations: list[DomainActivation], target_domains: list[str] | set[str]) -> list[dict[str, str]]:
    target_set = set(target_domains)
    return [
        {
            "source": "domain activation",
            "domain": activation.domain.value,
            "text": "; ".join(activation.reported_facts),
        }
        for activation in activations
        if activation.domain.value in target_set
    ]


def _client_preference_evidence(item: dict[str, Any], context: dict[str, Any]) -> list[dict[str, str]]:
    preferred = set(context.get("client_preferred_approaches", []))
    if item["approach_name"] in preferred:
        return [{"source": "client preference", "text": f"Client preference includes {item['approach_name']}."}]
    if context.get("informed_choice_confirmed", False):
        return [{"source": "client preference", "text": CONTEXT_EVIDENCE_LABELS["informed_choice_confirmed"]}]
    return []


def _clinician_confirmation(key: str, context: dict[str, Any]) -> list[dict[str, str]]:
    if context.get(key, False):
        return [{"source": "clinician confirmation", "text": CONTEXT_EVIDENCE_LABELS.get(key, f"Clinician confirmed {key}.")}]
    return []


def _prerequisite_evidence(
    prerequisite: dict[str, Any],
    item: dict[str, Any],
    intake: Intake,
    activations: list[DomainActivation],
    context: dict[str, Any],
) -> list[dict[str, str]]:
    prereq_id = prerequisite["id"]
    if prereq_id == "specific_change_target":
        return _evidence_from_intake(intake, {"change", "reduce", "increase", "stop", "start", "rebuild", "clarify", "goal", "target"})
    if prereq_id == "ambivalence_present":
        return _evidence_from_intake(intake, {"ambivalence", "ambivalent", "part of me", "pros and cons", "torn", "mixed", "want to", "hard to change"})
    if prereq_id == "collaborative_goal":
        return _evidence_from_intake(intake, set(item["client_goals"]) | set(item["target_processes"])) or _clinician_confirmation("collaborative_goal_confirmed", context)
    if prereq_id == "medical_referral_reason":
        return _domain_evidence(activations, {ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL.value}) or _clinician_confirmation("medical_referral_reason_confirmed", context)
    if prerequisite["required_evidence_source"] == "domain activation":
        return _domain_evidence(activations, item["target_domains"])
    if prerequisite["required_evidence_source"] == "client preference":
        return _client_preference_evidence(item, context)
    context_key = PREREQUISITE_CONTEXT_KEYS.get(prereq_id)
    if context_key:
        return _clinician_confirmation(context_key, context)
    return []


def _evaluate_prerequisites(
    prerequisites: list[dict[str, Any]],
    item: dict[str, Any],
    intake: Intake,
    activations: list[DomainActivation],
    context: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    met: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for prerequisite in prerequisites:
        evidence = _prerequisite_evidence(prerequisite, item, intake, activations, context)
        result = {**prerequisite, "evidence": evidence}
        if evidence:
            met.append(result)
        else:
            missing.append(result)
    return met, missing


def _process_matches(item: dict[str, Any], activated_domains: set[str], intake: Intake) -> list[str]:
    candidate_terms = set(item["target_processes"])
    for domain in activated_domains:
        candidate_terms.update(PROCESS_TERMS_BY_DOMAIN.get(domain, set()))
    text = " ".join(intake.facts_by_field().values()).lower()
    return sorted({term for term in candidate_terms if term.lower() in text or any(term.lower() in process.lower() for process in item["target_processes"])})


def _goal_matches(item: dict[str, Any], intake: Intake) -> list[str]:
    goal_text = intake.client_goals.lower()
    return [goal for goal in item["client_goals"] if any(word in goal_text for word in goal.lower().split() if len(word) > 4)]


def _priority_conditions(
    item: dict[str, Any],
    intake: Intake,
    activations: list[DomainActivation],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    present: list[dict[str, Any]] = []
    for condition in item["priority_shifting_or_referral_conditions"]:
        key = PRIORITY_CONTEXT_KEYS.get(condition["id"])
        evidence = _clinician_confirmation(key, context) if key else []
        if condition["id"] == "urgent_medical_priority" and not evidence and item["approach_name"] == "Medical consultation or referral":
            evidence = _domain_evidence(activations, {ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL.value})
        if evidence:
            present.append({**condition, "evidence": evidence})
    return present


def _conditional_considerations(
    item: dict[str, Any],
    intake: Intake,
    activations: list[DomainActivation],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    considerations = []
    for consideration in item["conditional_considerations"]:
        evidence = []
        if "client preference" in consideration["evidence_sources"]:
            evidence.extend(_client_preference_evidence(item, context))
        if "domain activation" in consideration["evidence_sources"]:
            evidence.extend(_domain_evidence(activations, item["target_domains"]))
        if "intake fact" in consideration["evidence_sources"]:
            evidence.extend(_evidence_from_intake(intake, item["target_processes"]))
        if "clinician confirmation" in consideration["evidence_sources"]:
            evidence.extend(_clinician_confirmation("feasibility_confirmed", context))
        considerations.append({**consideration, "evidence": evidence})
    return considerations


def _eligibility_status(
    item: dict[str, Any],
    missing_hard: list[dict[str, Any]],
    priority_conditions: list[dict[str, Any]],
    context: dict[str, Any],
) -> str:
    if not context.get("clinician_scope_confirmed", False):
        return "outside_current_scope_or_setting"
    if priority_conditions:
        statuses = {condition["status_if_present"] for condition in priority_conditions}
        if "consultation_or_referral_required" in statuses:
            return "consultation_or_referral_required"
        return "defer_while_priority_needs_are_addressed"
    if missing_hard:
        return "more_information_needed"
    if not context.get("feasibility_confirmed", False) or not context.get("informed_choice_confirmed", False):
        return "eligible_with_conditions"
    return "eligible_for_clinician_consideration"


def match_interventions(
    intake: Intake,
    activations: list[DomainActivation],
    context: dict[str, Any] | None = None,
    library: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return transparent candidate approach matches with prerequisites and score breakdown."""

    context = context or {}
    library = library or load_intervention_library()
    activated_domains = _activated_domain_names(activations)
    preferred = set(context.get("client_preferred_approaches", []))
    stage = str(context.get("treatment_stage", "")).lower()

    results: list[dict[str, Any]] = []
    for item in library:
        domain_matches = sorted(activated_domains.intersection(item["target_domains"]))
        process_matches = _process_matches(item, activated_domains, intake)
        goal_matches = _goal_matches(item, intake)
        stage_match = bool(stage and stage in item["treatment_stage"].lower())
        preference_match = item["approach_name"] in preferred

        universal_met, universal_missing = _evaluate_prerequisites(item["universal_review_gates"], item, intake, activations, context)
        approach_met, approach_missing = _evaluate_prerequisites(item["approach_specific_prerequisites"], item, intake, activations, context)
        all_missing = universal_missing + approach_missing
        missing_hard = [entry for entry in all_missing if entry.get("hard_prerequisite", True)]
        priority_conditions = _priority_conditions(item, intake, activations, context)
        status = _eligibility_status(item, missing_hard, priority_conditions, context)

        breakdown = {
            "match_to_impacted_domains": {"points": len(domain_matches) * 2, "details": domain_matches},
            "match_to_maintaining_processes": {"points": len(process_matches), "details": process_matches},
            "client_stated_goal": {"points": len(goal_matches) * 2, "details": goal_matches},
            "treatment_stage": {"points": 1 if stage_match else 0, "details": [context.get("treatment_stage", "")] if stage_match else []},
            "readiness": {"points": 1 if context.get("readiness_confirmed", False) else 0, "details": [CONTEXT_EVIDENCE_LABELS["readiness_confirmed"]] if context.get("readiness_confirmed", False) else []},
            "safety_and_stabilization_requirements": {"points": 1 if context.get("safety_review_completed", False) else 0, "details": [CONTEXT_EVIDENCE_LABELS["safety_review_completed"]] if context.get("safety_review_completed", False) else []},
            "client_preference": {"points": 2 if preference_match else 0, "details": [item["approach_name"]] if preference_match else []},
            "feasibility": {"points": 1 if context.get("feasibility_confirmed", False) else 0, "details": [CONTEXT_EVIDENCE_LABELS["feasibility_confirmed"]] if context.get("feasibility_confirmed", False) else []},
            "environmental_barriers": {"points": 1 if context.get("environmental_barriers_addressed", False) else 0, "details": [CONTEXT_EVIDENCE_LABELS["environmental_barriers_addressed"]] if context.get("environmental_barriers_addressed", False) else []},
            "clinician_setting_and_scope": {"points": 1 if context.get("clinician_scope_confirmed", False) else 0, "details": [CONTEXT_EVIDENCE_LABELS["clinician_scope_confirmed"]] if context.get("clinician_scope_confirmed", False) else []},
        }
        raw_total = sum(factor["points"] for factor in breakdown.values())
        eligible = status in {"eligible_for_clinician_consideration", "eligible_with_conditions"}
        results.append({
            "approach_name": item["approach_name"],
            "status": status,
            "eligibility_status": status,
            "total_score": raw_total if eligible else 0,
            "raw_score_before_prerequisites": raw_total,
            "scoring_breakdown": breakdown,
            "universal_review_gates": item["universal_review_gates"],
            "approach_specific_prerequisites": item["approach_specific_prerequisites"],
            "prerequisites_met": universal_met + approach_met,
            "prerequisites_missing": all_missing,
            "missing_prerequisites": all_missing,
            "clarification_questions": [question for missing in all_missing for question in missing.get("clarification_questions", [])],
            "conditional_considerations": _conditional_considerations(item, intake, activations, context),
            "priority_shifting_or_referral_conditions": priority_conditions,
            "scope_or_setting_requirements": item["scope_or_setting_requirements"],
            "why_matched": {"domains": domain_matches, "processes": process_matches, "goals": goal_matches},
            "intervention": item,
        })
    status_order = {status: index for index, status in enumerate(ELIGIBILITY_STATUSES)}
    return sorted(results, key=lambda result: (status_order[result["status"]], -result["raw_score_before_prerequisites"], result["approach_name"]))
