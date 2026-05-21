# invoice-service

A Python microservice that generates, stores, and emails PDF invoices for a SaaS billing platform.

## Install

```bash
pip install -e .
```

## Test

```bash
pytest -q
```

## Environment

Copy `.env.example` to `.env` and configure your database and email settings before running.

## CI

All pushes and pull requests run the full test suite via GitHub Actions.

## Architecture

The service exposes a REST API for invoice creation and retrieval. PDF generation uses
WeasyPrint. Email delivery uses SendGrid. All configuration is environment-variable-driven.

## Agent Workspace Notes

Agent sessions must follow `AGENTS.md`, `.cursorrules`, and `CURRENT_STATE.md` before edits.
Use the repo handoff notes to continue prior work without re-discovering architecture decisions.
