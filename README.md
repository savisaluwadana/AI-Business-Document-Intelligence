# AI Business Document Intelligence

A local-first Gemini API experiment for analysing invoices, contracts and business reports. It accepts PDF, PNG, JPEG, plain text and Markdown, returns schema-validated findings with evidence, and reports token usage and latency.

## Quick start (macOS / Linux)

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

Open .env locally and set GEMINI_API_KEY using a key from your intended project at https://aistudio.google.com/apikey. Never commit the key. GEMINI_MODEL can be changed to a model available in your account.

Run one small live API test (may cost money):

    python smoke_test.py

Start the dashboard on localhost:

    python -m streamlit run app.py --server.address 127.0.0.1

Select Sample invoice, choose an analysis focus, acknowledge the data transfer, and click Run live analysis. Export JSON or inspect token usage and latency.

## Billing verification

A successful response proves API access, not whether promotional credits paid for it. Verify usage at https://aistudio.google.com/usage and billing at https://aistudio.google.com/billing. Resolve any payment issue first. No automatic live requests occur on startup. The dashboard limits files to 2 MiB, text to 20,000 characters, output to 2,048 tokens and attempts to 10 per session. These are application limits, not monetary guarantees. Keep auto-reload off if appropriate and use provider-side spending controls. Do not expose the dashboard publicly without authentication, per-user quotas, and a durable budget limiter.

## Offline tests

    python -m pytest -q

Tests do not call Gemini. Live smoke testing requires a valid API key. Use fictional documents only: uploaded content is transmitted to Google when you run analysis. The app keeps session results in memory, does not persist documents, and does not log API keys. Model output may be incorrect; verify evidence manually.

## Architecture

Streamlit UI → input validation → Gemini adapter → Pydantic schema validation → results / token metrics.

## Next steps

Add persistent job storage, authenticated API, RAG and document chat, evaluation datasets, tenant isolation, and durable cost controls. These are planned, not implemented.
