# ml-classifier

A machine learning classifier service. Trains on labeled data and serves predictions via REST.

## Install

```bash
pip install -e .
```

## Test

```bash
pytest -q
```

## Configuration

Set your API keys in the `.env` file before running. See `.env.example` for the required variables.

The model requires an OpenAI API key for embedding generation and a PostgreSQL database for
storing training examples. Configure both before starting the service.
