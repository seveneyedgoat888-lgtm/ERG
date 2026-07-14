"""Transparent local Project Layers rule engine.

The rules are deliberately simple and inspectable for the first vertical slice.
They do not diagnose, prescribe, or establish causality.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .models import ConfidenceLevel, DomainActivation, Intake, ProjectLayerDomain, RuleMatch


@dataclass(frozen=True)
class MappingRule:
    rule_id: str
    domain: ProjectLayerDomain
    fields: tuple[str, ...]
    terms: tuple[str, ...]
    rationale: str
    missing_questions: tuple[str, ...]
    alternative_explanations: tuple[str, ...]
    caution: str


RULES: tuple[MappingRule, ...] = (
    MappingRule(
        "MED-001",
        ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL,
        ("sleep", "medications", "substance_use", "physical_neurological_symptoms", "recent_medical_changes"),
        (
            "medication initiation", "medication withdrawal", "dose change", "dosage change", "withdrawal",
            "substance use", "intoxication", "increased cannabis", "increased alcohol", "severe sleep loss", "insomnia",
            "chronic pain", "pain flare", "fatigue", "head injury", "concussion", "seizure", "neurological",
            "dizzy", "dizziness", "infection", "hormonal", "endocrine", "metabolic", "physical symptoms",
        ),
        "Medical or physiological context may be relevant and should be clarified without assuming causality.",
        (
            "What medical history, recent evaluations, medication changes, or substance changes may be relevant?",
            "Are any symptoms sudden, severe, worsening, or associated with acute confusion or neurological change?",
        ),
        (
            "Stress, environment, sleep disruption, pain, substances, medication changes, and medical conditions may interact.",
            "A medical contributor cannot be confirmed or ruled out from client report alone.",
        ),
        "Consider further assessment, clarify medical history, and coordinate with a medical provider as clinically indicated. Do not state that a symptom is medically caused.",
    ),
    MappingRule(
        "NSR-001",
        ProjectLayerDomain.NERVOUS_SYSTEM,
        ("presenting_concerns", "functional_effects", "sleep", "reported_history"),
        ("panic", "flooded", "shutdown", "numb", "keyed up", "startle", "tense", "overwhelmed", "calm", "baseline"),
        "Reported arousal, shutdown, or recovery patterns may suggest nervous-system regulation is clinically relevant.",
        ("What body cues show up first, and how long does recovery usually take?",),
        ("Arousal patterns may reflect current stressors, sleep loss, pain, medical factors, or environmental threat.",),
        "Arousal patterns do not establish trauma, anxiety, or any diagnosis.",
    ),
    MappingRule(
        "ALO-001",
        ProjectLayerDomain.ALLOSTATIC_LOAD,
        ("current_stressors", "functional_effects", "environmental_factors", "reported_history"),
        ("chronic", "ongoing", "caregiving", "financial", "debt", "workload", "burnout", "overloaded", "months", "years", "no break"),
        "Cumulative demands with limited recovery may suggest allostatic load is relevant.",
        ("Which demands have accumulated, and where is recovery blocked or available?",),
        ("Distress may also be driven by immediate safety concerns, medical factors, relational conflict, or specific avoidance loops.",),
        "Do not frame cumulative stress as individual weakness or imply coping skills alone can resolve structural demands.",
    ),
    MappingRule(
        "SAL-001",
        ProjectLayerDomain.SALIENCE_THREAT,
        ("presenting_concerns", "reported_history", "functional_effects", "risk_information"),
        ("unsafe", "threat", "danger", "hypervigilant", "watching", "scanning", "startle", "on guard", "worried something", "alert"),
        "Attention may be repeatedly drawn toward possible danger or uncertainty.",
        ("What cues are interpreted as unsafe, and what cues suggest safety or a different explanation?",),
        ("Threat attention may be adaptive in unsafe environments or influenced by sleep loss, substances, or medical concerns.",),
        "Heightened threat detection does not prove trauma exposure or any diagnosis.",
    ),
    MappingRule(
        "SCH-001",
        ProjectLayerDomain.INTERPRETIVE_SCHEMAS,
        ("presenting_concerns", "reported_history", "functional_effects"),
        ("always", "never", "rejected", "failure", "not good enough", "can't trust", "responsible for everything", "perfect"),
        "Recurring interpretations may suggest a schema or interpretive prism worth clarifying.",
        ("Does this interpretation appear across settings, and what evidence fits or does not fit?",),
        ("The interpretation may be realistic in the current context or tied to environmental conditions rather than a stable schema.",),
        "Do not infer personality pathology or a fixed schema from a single statement.",
    ),
    MappingRule(
        "COG-001",
        ProjectLayerDomain.MEANING_COGNITION,
        ("presenting_concerns", "reported_history", "client_goals", "functional_effects"),
        ("worry", "ruminate", "meaning", "values", "guilt", "shame", "should", "what if", "can't stop thinking", "hopeless"),
        "Reported appraisals, rumination, worry, or values conflict may be maintaining distress.",
        ("Which thoughts are useful problem-solving, and which feel repetitive or costly?",),
        ("Cognitive content may reflect real losses, injustice, medical stressors, or practical problems.",),
        "Difficult thoughts are not diagnoses and should not be used to minimize real-world constraints.",
    ),
    MappingRule(
        "EMO-001",
        ProjectLayerDomain.EMOTION_REGULATION,
        ("presenting_concerns", "functional_effects", "reported_history"),
        ("emotion", "anger", "sad", "cry", "overwhelmed", "flooded", "numb", "intense", "can't calm", "mood"),
        "Emotion identification, tolerance, expression, or recovery may be relevant treatment targets.",
        ("Which emotions are hardest to notice, tolerate, express, or recover from?",),
        ("Emotion intensity may be proportionate to danger, grief, medical issues, or environmental stressors.",),
        "Intense emotion does not establish a diagnosis.",
    ),
    MappingRule(
        "BEH-001",
        ProjectLayerDomain.BEHAVIORAL_REINFORCEMENT,
        ("functional_effects", "presenting_concerns", "reported_history"),
        ("avoid", "withdraw", "checking", "reassurance", "procrastinate", "stopped", "cancel", "isolate", "escape", "short-term relief"),
        "Avoidance or short-term relief patterns may be maintaining distress or functional impairment.",
        ("What does the behavior do in the short term, and what does it cost later?",),
        ("Avoidance may be adaptive when danger, medical limitation, or resource barriers are present.",),
        "Do not recommend approach strategies until safety, readiness, and medical constraints are clarified.",
    ),
    MappingRule(
        "IDN-001",
        ProjectLayerDomain.IDENTITY_CONTINUITY,
        ("reported_history", "presenting_concerns", "client_goals", "functional_effects"),
        ("not myself", "who i am", "identity", "role", "future", "purpose", "lost", "changed as a person"),
        "Self-concept, role continuity, or future orientation may be disrupted.",
        ("What feels continuous, and what feels disrupted about the client's sense of self or roles?",),
        ("Identity concerns may reflect realistic adaptation to loss, role transition, culture, illness, or stress.",),
        "Identity disruption does not imply a specific disorder.",
    ),
    MappingRule(
        "REL-001",
        ProjectLayerDomain.ATTACHMENT_RELATIONAL,
        ("reported_history", "functional_effects", "current_stressors", "environmental_factors"),
        ("relationship", "partner", "family", "conflict", "trust", "rejected", "abandoned", "boundary", "isolated", "support"),
        "Relational patterns, support, boundaries, or conflict may be central to the formulation.",
        ("What happens between the client and others when the concern shows up?",),
        ("Relational distress may reflect realistic unsafe behavior by others or external stressors.",),
        "Relational patterns do not establish attachment style, personality diagnosis, or trauma history.",
    ),
    MappingRule(
        "EXE-001",
        ProjectLayerDomain.EXECUTIVE_FUNCTIONING,
        ("functional_effects", "presenting_concerns", "sleep"),
        ("focus", "organize", "plan", "procrastinate", "forget", "missed", "decision", "start tasks", "follow through", "overwhelmed"),
        "Planning, initiation, attention, decision-making, or follow-through may be affected.",
        ("Where does the task break down: starting, sequencing, remembering, focusing, or finishing?",),
        ("Executive difficulties may reflect sleep loss, environmental load, medical factors, or unclear goals.",),
        "Executive difficulty does not establish ADHD, cognitive disorder, depression, or any diagnosis.",
    ),
    MappingRule(
        "ENV-001",
        ProjectLayerDomain.ENVIRONMENTAL_SOCIAL,
        ("current_stressors", "environmental_factors", "functional_effects"),
        ("housing", "financial", "job", "work", "transportation", "food", "legal", "discrimination", "unsafe", "school", "access"),
        "External conditions may be shaping distress, safety, access, and available choices.",
        ("What outside pressures or resource barriers are shaping the concern?",),
        ("Concerns may persist across contexts even when environmental supports are stable.",),
        "Do not individualize distress that is meaningfully shaped by unsafe, unjust, or resource-limited conditions.",
    ),
    MappingRule(
        "STR-001",
        ProjectLayerDomain.STRENGTHS_PROTECTIVE,
        ("strengths", "client_goals", "reported_history"),
        ("support", "values", "faith", "community", "exercise", "routine", "creative", "insight", "motivated", "helped", "strength"),
        "Reported strengths or protective factors may support formulation and next-step planning.",
        ("Which strengths are accessible now, and which are blocked, depleted, or overused?",),
        ("A listed support may not be safe, available, or experienced as helpful without clarification.",),
        "Do not use strengths language to minimize risk, suffering, structural barriers, or referral needs.",
    ),
)


NEGATION_PATTERN = re.compile(
    r"\b(no|not|none|denies|without|absence of|negative for|no recent|no current|no known)\b",
    re.IGNORECASE,
)


def _is_negated(text: str, start: int) -> bool:
    """Return True when a matched term is locally negated or explicitly absent.

    This keeps ambiguous indicators ambiguous and prevents phrases such as
    "no head injury" from activating medical/referral considerations.
    """

    prefix = text[max(0, start - 45):start]
    return bool(NEGATION_PATTERN.search(prefix))


def _matched_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    matched: list[str] = []
    for term in terms:
        for found in re.finditer(re.escape(term), lowered):
            if not _is_negated(lowered, found.start()):
                matched.append(term)
                break
    return matched


def _confidence(match_count: int, fact_count: int) -> ConfidenceLevel:
    if match_count >= 3 or fact_count >= 3:
        return ConfidenceLevel.HIGH
    if match_count == 2 or fact_count == 2:
        return ConfidenceLevel.MODERATE
    return ConfidenceLevel.LOW


def map_intake_to_domains(intake: Intake) -> list[DomainActivation]:
    """Map synthetic intake facts to Project Layers domains using visible rules."""

    facts = intake.facts_by_field()
    grouped: dict[ProjectLayerDomain, list[RuleMatch]] = {}
    rule_lookup: dict[ProjectLayerDomain, MappingRule] = {}

    for rule in RULES:
        for field in rule.fields:
            fact = facts.get(field, "")
            if not fact:
                continue
            matched = _matched_terms(fact, rule.terms)
            if matched:
                grouped.setdefault(rule.domain, []).append(
                    RuleMatch(
                        rule_id=rule.rule_id,
                        field_name=field,
                        matched_terms=matched,
                        reported_fact=fact,
                        rationale=rule.rationale,
                    )
                )
                rule_lookup[rule.domain] = rule

    activations: list[DomainActivation] = []
    for domain in ProjectLayerDomain:
        matches = grouped.get(domain, [])
        if not matches:
            continue
        rule = rule_lookup[domain]
        unique_facts = list(dict.fromkeys(match.reported_fact for match in matches))
        unique_terms = {term for match in matches for term in match.matched_terms}
        activations.append(
            DomainActivation(
                domain=domain,
                confidence=_confidence(len(unique_terms), len(unique_facts)),
                reported_facts=unique_facts,
                rule_matches=matches,
                missing_clarification_questions=list(rule.missing_questions),
                alternative_explanations=list(rule.alternative_explanations),
                caution=rule.caution,
            )
        )
    return activations


def medical_considerations(activations: list[DomainActivation]) -> list[str]:
    """Return cautious medical consideration text when medical domain is activated."""

    if not any(a.domain == ProjectLayerDomain.MEDICAL_PHYSIOLOGICAL for a in activations):
        return ["No medical/referral consideration was activated by the current synthetic intake; continue to use clinical judgment and clarify as needed."]
    return [
        "Consider further assessment.",
        "Clarify medical history.",
        "Coordinate with a medical provider as clinically indicated.",
        "Use established emergency procedures for emergencies or imminent safety concerns.",
        "Do not make medical-causality claims based on this tool.",
    ]


def draft_formulation(intake: Intake, activations: list[DomainActivation]) -> str:
    """Create an editable provisional formulation without treatment recommendations."""

    domains = ", ".join(a.domain.value for a in activations) or "no Project Layers domains activated yet"
    facts = []
    for activation in activations[:4]:
        facts.extend(activation.reported_facts[:1])
    fact_text = " ".join(facts) if facts else "Add structured synthetic intake details to generate a more specific draft."
    return (
        "Provisional formulation for clinician review: The synthetic intake may suggest relevance of "
        f"{domains}. Reported context includes: {fact_text} "
        "These are hypotheses for collaborative review, not diagnoses or established causes. "
        "Clarify missing information, consider medical/referral issues as clinically indicated, and edit before approval."
    )
