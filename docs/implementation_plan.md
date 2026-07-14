# Implementation Plan

## Recommended local prototype architecture

### Recommendation

Use **Streamlit with a small Python package, SQLite, Pydantic, local YAML/JSON rule files, and pytest** for the first local prototype. This is the simplest architecture that satisfies the requirements: beginner-friendly setup, Python-based implementation, browser interface, no cloud deployment, no external AI API, synthetic data only, local rule engine, editable intervention library, and automated tests.

### Why Streamlit is the recommended choice

- **Easiest for a beginner to run:** one Python environment and one command such as `streamlit run app.py`.
- **Python-only application logic:** intake validation, rule matching, formulation generation, recommendation ranking, SQLite persistence, and tests can all stay in Python.
- **Simple browser interface:** Streamlit provides forms, tables, expanders, sidebars, and download buttons without requiring frontend build tooling.
- **Local-only by default:** the app can run on the clinician reviewer’s machine with local SQLite storage and no cloud deployment.
- **No external AI API required:** all outputs can come from deterministic local rules and curated intervention-library files.
- **Editable libraries:** rules and interventions can be stored in versioned YAML or JSON files that are loaded and validated by Pydantic.
- **Testing remains straightforward:** core logic can be kept outside Streamlit page code and tested with pytest.

### Brief comparison: Streamlit vs FastAPI plus React

| Option | Benefits | Tradeoffs for this prototype |
| --- | --- | --- |
| Streamlit | Fastest path to a local browser UI; Python-only; minimal setup; well suited to forms, review screens, evidence tables, and export previews. | Less flexible for highly customized production UX; page state needs careful organization as the workflow grows. |
| FastAPI plus React | More production-like separation of backend API and frontend; better for complex custom interactions or future multi-user web deployment. | Requires backend server, frontend app, package manager/build tooling, API contracts, CORS/dev-server coordination, and more files for a beginner to run. This is unnecessary for version 1. |

### Architecture shape

```txt
app.py                         # Streamlit entry point
pages/                         # Streamlit workflow pages
project_layers/
  models.py                    # Pydantic models
  database.py                  # SQLite setup and simple repository functions
  rules.py                     # Local rule loading and matching
  safety.py                    # Medical/referral consideration checks
  formulation.py               # Maintaining-cycle draft assembly
  recommendations.py           # Transparent local ranking logic
  exports.py                   # Markdown/JSON export helpers
data/
  rules/*.yaml                 # Editable local rule files
  interventions/*.yaml         # Editable intervention library
  demo_cases/*.json            # Synthetic cases only
tests/                         # pytest tests for logic and safety checks
```

### Implementation guardrails

- Keep Streamlit files thin; put clinical logic in testable Python modules.
- Load rules and interventions from local editable files, then validate them with Pydantic before use.
- Store only synthetic demonstration cases in SQLite.
- Keep all recommendation ranking deterministic and explainable.
- Do not add FastAPI, React, cloud deployment, authentication, or external AI calls in version 1 unless a later human review changes the scope.

## Milestone 1: Human review of planning documents

- Review product requirements, ontology, safety requirements, data model, user flow, implementation plan, and unanswered questions.
- Confirm clinical governance for rule and intervention-library review.
- Confirm exact emergency-procedure language for the intended setting.

## Milestone 2: Python project scaffold

- Create Python package structure.
- Add Streamlit entry point.
- Add pytest configuration.
- Add local SQLite database initialization.
- Add README setup instructions.

## Milestone 3: Pydantic models

- Implement models for case records, intake, entered facts, Project Layers domains, rules, activations, missing questions, referral considerations, formulations, interventions, recommendations, approvals, and exports.
- Add validation for synthetic-only cases and possible identifiers.
- Add unit tests for model validation.

## Milestone 4: Local data libraries

- Create local Project Layers domain definitions.
- Create clinician-reviewable rule files.
- Create red-flag rule files.
- Create missing-information rule files.
- Create curated intervention library with DBT, CBT, ACT, MBT, motivational interviewing, behavioral activation, attachment-informed therapy, trauma-informed stabilization, family/systemic approaches, case-management/environmental interventions, and medical referral considerations.

## Milestone 5: SQLite persistence

- Create schema migrations.
- Persist synthetic cases, intakes, entered facts, rules, activations, recommendations, approvals, and export records.
- Add repository-layer tests.

## Milestone 6: Rule engine and evidence display

- Convert structured intake into canonical entered facts.
- Apply explicit rules to Project Layers domains.
- Generate evidence records showing which facts activated each domain.
- Test deterministic mapping and evidence completeness.

## Milestone 7: Safety engine

- Implement red-flag detection.
- Generate cautious medical/referral consideration language.
- Add emergency-procedure reminders.
- Add prohibited-output tests for diagnostic, prescriptive, and false-reassurance language.

## Milestone 8: Missing-information engine

- Generate questions from safety rules, formulation rules, and intervention prerequisites.
- Group questions by priority.
- Add clinician status tracking.

## Milestone 9: Formulation generator

- Generate provisional maintaining-cycle formulations.
- Preserve generated draft and clinician revision separately.
- Add tests for provisional language and evidence references.

## Milestone 10: Recommendation engine

- Match activated domains and facts to intervention library items.
- Rank suggestions using visible rule-based logic.
- Show why each approach was suggested.
- Require clinician approval before export.

## Milestone 11: Streamlit workflow

- Build screens for structured intake, mapping, evidence, medical/referral considerations, missing information, formulation, recommendations, session guidance, cautions, clinician approval, and export.
- Add persistent disclaimers and synthetic-case labeling.

## Milestone 12: Export

- Implement Markdown export.
- Optionally implement JSON export if approved during design review.
- Block export until clinician approval is complete.

## Milestone 13: Demo cases and review

- Add synthetic demonstration cases only.
- Include cases that exercise red flags, missing-information prompts, protective factors, and multiple therapeutic approaches.
- Conduct clinical safety review before broader prototype use.

## Milestone 14: Hardening

- Add linting and type checking if selected.
- Expand tests.
- Document how to update rules and intervention library entries.
- Prepare reviewer checklist.
