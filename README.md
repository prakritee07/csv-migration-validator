
# CSV Migration Validator
[![CSV Validator Tests](https://github.com/prakritee07/csv-migration-validator/actions/workflows/tests.yml/badge.svg)](https://github.com/prakritee07/csv-migration-validator/actions/workflows/tests.yml)

A Python command-line tool that compares two CSV exports and generates a report of data changes. This learning project demonstrates data validation techniques that can be useful during system migrations.

## Features

- Identify records added to or removed from a new export.
- Detect changed field values for matching records.
- Count unchanged records.
- Detect duplicate record IDs.
- Validate required ID columns and blank record IDs.
- Report columns added or removed between files.
- Generate a structured JSON report.
- Handle common file and input errors.
- Include automated tests with pytest.
- Run tests automatically through GitHub Actions.

## Technologies

- Python 3
- CSV and JSON processing
- `argparse` and `pathlib`
- pytest
- Git and GitHub
- GitHub Actions

## Project Structure

```text
csv-migration-validator/
├── .github/
│   └── workflows/
│       └── tests.yml
├── old_data.csv
├── new_data.csv
├── validator.py
├── test_validator.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/prakritee07/csv-migration-validator.git
cd csv-migration-validator
```

Create and activate a virtual environment on Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Install the test dependency:

```bash
python -m pip install -r requirements.txt
```

## Run the Validator

Compare the sample files:

```bash
python validator.py old_data.csv new_data.csv
```

The program prints a summary and creates `migration_report.json`.

To use a different ID column:

```bash
python validator.py old_data.csv new_data.csv --id-column employee_id
```

To specify a different report filename:

```bash
python validator.py old_data.csv new_data.csv --output report.json
```

## Run Automated Tests

```bash
python -m pytest -v
```

The tests cover record additions, removals, changes, duplicate IDs, missing ID columns, blank record IDs, and column changes.

GitHub Actions is configured to run the tests when code is pushed to `main` or a pull request targets `main`.

## Report Contents

The JSON report contains:

- Counts of old and new rows
- Added and removed records
- Changed field values, including old and new values
- Unchanged record counts
- Duplicate IDs in each file
- Columns added or removed in the new export

## Current Limitations

This project compares CSV exports using a selected record ID and exact text values after trimming surrounding whitespace. It does not connect directly to databases or verify database transactions. Duplicate IDs are reported, while comparisons use the first occurrence of each ID. Review the report before making migration decisions.

## Purpose

This project demonstrates Python programming, CSV processing, input validation, data comparison, JSON reporting, error handling, automated testing, and a basic continuous integration workflow.
