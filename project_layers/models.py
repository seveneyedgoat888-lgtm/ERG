"""Pydantic models for the first Project Layers vertical slice."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class ProjectLayerDomain(str, Enum):
    MEDICAL_PHYSIOLOGICAL = "Medical and physiological contributors"
    NERVOUS_SYSTEM = "Nervous-system regulation"
    ALLOSTATIC_LOAD = "Allostatic load"
    SALIENCE_THREAT = "Salience and threat detection"
    INTERPRETIVE_SCHEMAS = "Interpretive prism and schemas"
    MEANING_COGNITION = "Meaning and cognition"
    EMOTION_REGULATION = "Emotion regulation"
    BEHAVIORAL_REINFORCEMENT = "Behavioral reinforcement and avoidance"
    IDENTITY_CONTINUITY = "Identity and self-continuity"
    ATTACHMENT_RELATIONAL = "Attachment and relational functioning"
    EXECUTIVE_FUNCTIONING = "Executive functioning"
    ENVIRONMENTAL_SOCIAL = "Environmental and social conditions"
    STRENGTHS_PROTECTIVE = "Strengths and protective factors"


class Intake(BaseModel):
    """Synthetic structured intake information for a clinician-reviewed demo case."""

    model_config = ConfigDict(extra="forbid")

    presenting_concerns: str = ""
    reported_history: str = ""
    onset_duration: str = ""
    functional_effects: str = ""
    current_stressors: str = ""
    strengths: str = ""
    client_goals: str = ""
    risk_information: str = ""
    sleep: str = ""
    medications: str = ""
    substance_use: str = ""
    physical_neurological_symptoms: str = ""
    recent_medical_changes: str = ""
    environmental_factors: str = ""

    def facts_by_field(self) -> dict[str, str]:
        return {
            name: value.strip()
            for name, value in self.model_dump().items()
            if isinstance(value, str) and value.strip()
        }


class DemoCase(BaseModel):
    """A synthetic case included for demonstration only."""

    model_config = ConfigDict(extra="forbid")

    case_id: str
    title: str
    synthetic: Literal[True] = True
    intake: Intake

    @model_validator(mode="after")
    def require_synthetic_label(self) -> "DemoCase":
        if not self.synthetic:
            raise ValueError("Version 1 only supports synthetic demonstration cases.")
        return self


class RuleMatch(BaseModel):
    rule_id: str
    field_name: str
    matched_terms: list[str]
    reported_fact: str
    rationale: str


class DomainActivation(BaseModel):
    domain: ProjectLayerDomain
    confidence: ConfidenceLevel
    reported_facts: list[str] = Field(default_factory=list)
    rule_matches: list[RuleMatch] = Field(default_factory=list)
    missing_clarification_questions: list[str] = Field(default_factory=list)
    alternative_explanations: list[str] = Field(default_factory=list)
    caution: str
