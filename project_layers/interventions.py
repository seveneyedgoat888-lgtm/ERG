"""Transparent intervention matching for prototype session review.

This module ranks candidate approaches with explicit, inspectable factors. It does
not make treatment recommendations automatically: approaches with missing
prerequisites are blocked and all outputs require clinician decision.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import DomainActivation, Intake, ProjectLayerDomain

INTERVENTION_LIBRARY_PATH = Path(__file__).resolve().parents[1] / "data" / "intervention_library.json"

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
    ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT.value: {"activity", "avoidance", "reinforcement", "committed action", "ambivalence"},
    ProjectLayerDomain.IDENTITY_CONTINUITY.value: {"identity", "values", "self", "committed action"},
    ProjectLayerDomain.ATTACHMENT_RELATIONAL.value: {"relational", "attachment", "communication", "mental-state", "repair"},
    ProjectLayerDomain.EXECUTIVE_FUNCTIONING.value: {"task", "planning", "problem solving", "routine"},
    ProjectLayerDomain.ENVIRONMENTAL_SOCIAL.value: {"resource", "access", "barrier", "care coordination", "environmental"},
    ProjectLayerDomain.STRENGTHS_PROTECTIVE.value: {"strength", "values", "support", "community", "routine"},
}


def load_intervention_library(path: Path = INTERVENTION_LIBRARY_PATH) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _contains_any(text: str, options: list[str] | set[str]) -> list[str]:
    lowered = text.lower()
    return [option for option in options if option.lower() in lowered]


def _activated_domain_names(activations: list[DomainActivation]) -> set[str]:
    return {activation.domain.value for activation in activations}


def _process_matches(item: dict[str, Any], activated_domains: set[str], intake: Intake) -> list[str]:
    candidate_terms = set(item["target_processes"])
    for domain in activated_domains:
        candidate_terms.update(PROCESS_TERMS_BY_DOMAIN.get(domain, set()))
    text = " ".join(intake.facts_by_field().values()).lower()
    return sorted({term for term in candidate_terms if term.lower() in text or any(term.lower() in process.lower() for process in item["target_processes"])})


def _goal_matches(item: dict[str, Any], intake: Intake) -> list[str]:
    goal_text = intake.client_goals.lower()
    return [goal for goal in item["client_goals"] if any(word in goal_text for word in goal.lower().split() if len(word) > 4)]


def _missing_prerequisites(
    item: dict[str, Any],
    activated_domains: set[str],
    context: dict[str, Any],
) -> list[str]:
    missing: list[str] = []
    if not context.get("readiness_confirmed", False):
        missing.append("Readiness has not been confirmed for this prototype session.")
    if not context.get("safety_review_completed", False):
        missing.append("Safety, stabilization, and medical/referral considerations have not been reviewed.")
    if not context.get("feasibility_confirmed", False):
        missing.append("Feasibility has not been confirmed with the client and setting.")
    if not context.get("clinician_scope_confirmed", False):
        missing.append("Clinician setting, competence, and scope have not been confirmed.")
    if ProjectLayerDomain.ENVIRONMENTAL_SOCIAL.value in activated_domains and not context.get("environmental_barriers_addressed", False):
        missing.append("Environmental barriers are active and have not yet been addressed or planned for.")
    if "Medical consultation or referral" != item["approach_name"] and ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL.value in activated_domains and not context.get("medical_considerations_reviewed", False):
        missing.append("Medical/referral considerations are active and have not been reviewed for this non-medical approach.")
    return missing


def match_interventions(
    intake: Intake,
    activations: list[DomainActivation],
    context: dict[str, Any] | None = None,
    library: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return transparent candidate approach matches with full scoring breakdown."""

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
        missing = _missing_prerequisites(item, activated_domains, context)

        breakdown = {
            "match_to_impacted_domains": {"points": len(domain_matches) * 2, "details": domain_matches},
            "match_to_maintaining_processes": {"points": len(process_matches), "details": process_matches},
            "client_stated_goal": {"points": len(goal_matches) * 2, "details": goal_matches},
            "treatment_stage": {"points": 1 if stage_match else 0, "details": [context.get("treatment_stage", "")] if stage_match else []},
            "readiness": {"points": 1 if context.get("readiness_confirmed", False) else 0, "details": ["readiness confirmed"] if context.get("readiness_confirmed", False) else []},
            "safety_and_stabilization_requirements": {"points": 1 if context.get("safety_review_completed", False) else 0, "details": ["safety/stabilization reviewed"] if context.get("safety_review_completed", False) else []},
            "client_preference": {"points": 2 if preference_match else 0, "details": [item["approach_name"]] if preference_match else []},
            "feasibility": {"points": 1 if context.get("feasibility_confirmed", False) else 0, "details": ["feasibility confirmed"] if context.get("feasibility_confirmed", False) else []},
            "environmental_barriers": {"points": 1 if context.get("environmental_barriers_addressed", False) else 0, "details": ["environmental barriers addressed/planned"] if context.get("environmental_barriers_addressed", False) else []},
            "clinician_setting_and_scope": {"points": 1 if context.get("clinician_scope_confirmed", False) else 0, "details": ["scope confirmed"] if context.get("clinician_scope_confirmed", False) else []},
        }
        total = sum(factor["points"] for factor in breakdown.values())
        status = "missing_prerequisites" if missing else "candidate"
        results.append({
            "approach_name": item["approach_name"],
            "status": status,
            "total_score": total if not missing else 0,
            "raw_score_before_prerequisites": total,
            "scoring_breakdown": breakdown,
            "missing_prerequisites": missing,
            "why_matched": {
                "domains": domain_matches,
                "processes": process_matches,
                "goals": goal_matches,
            },
            "intervention": item,
        })
    return sorted(results, key=lambda result: (result["status"] != "candidate", -result["total_score"], result["approach_name"]))
