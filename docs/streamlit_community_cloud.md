# Streamlit Community Cloud Deployment Notes

## Repository

- Repository name: `ERG`
- Branch for this work: `work`

## Entrypoint

Use this Streamlit entrypoint:

```bash
app.py
```

The app should start with:

```bash
streamlit run app.py
```

## Dependencies

Python dependencies are declared in the repository root `requirements.txt` file. Streamlit Community Cloud should install them automatically during deployment.

## Data files

The prototype uses committed synthetic demonstration data only:

```text
data/demo_cases/demo_cases.json
```

No real client-identifying information should be entered. The app displays synthetic-data-only warnings in the main page and sidebar.

## Secrets and environment variables

Version 1 does not require secrets, environment variables, cloud databases, or external AI API keys.

## Deployment limitations

- This is a prototype for synthetic demonstration data only.
- There is no user authentication.
- There is no persistent cloud database.
- Outputs are decision support only and do not diagnose, prescribe, replace clinical judgment, or establish medical or psychological causes.
- Treatment recommendations are intentionally not implemented in this vertical slice.
