# data-pipeline

A Python ETL pipeline that ingests CSV files, validates schema, and writes to a database.

## Install

```bash
pip install -e .
```

## Usage

```bash
python -m pipeline.main --input data/raw.csv --output data/clean.csv
```

## Testing

```bash
pytest -q
```

This pipeline handles date normalization, null imputation, and schema enforcement.
It is designed to run on a daily schedule via cron or GitHub Actions.
