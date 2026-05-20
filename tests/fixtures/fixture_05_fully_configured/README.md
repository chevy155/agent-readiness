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

Agents working in this repo should read AGENTS.md before making changes.
