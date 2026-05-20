# AGENTS.md

## Project Purpose
invoice-service generates, stores, and emails PDF invoices.

## Allowed Changes
- Fix bugs in existing invoice generation logic
- Add new tests to tests/

## Forbidden Changes
- Do not modify database migration files without review
- Do not change the PDF generation library
- Do not add network calls outside of the designated HTTP client module
- Do not commit .env or any file with real credentials

## Test Commands
```bash
pytest -q
```

## Boundaries
- Allowed scope: src/, tests/
- Off-limits: infra/, migrations/ without explicit approval
- Guardrails: all external calls must go through src/http_client.py
