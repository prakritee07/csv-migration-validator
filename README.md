

\# CSV Migration Validator



A Python command-line tool that compares two CSV exports and creates a report of data changes. It is designed as a learning project for validating data during system migrations.



\## Features



\- Identify records added to or removed from the new export.

\- Detect changed field values for matching records.

\- Report unchanged records.

\- Detect duplicate record IDs in each file.

\- Validate required ID columns and blank record IDs.

\- Detect columns added or removed between exports.

\- Generate a structured JSON report.

\- Handle common file and CSV input errors.

\- Include automated tests with pytest.



\## Technologies



\- Python 3

\- CSV, JSON, argparse, and pathlib from the Python standard library

\- pytest

\- Git and GitHub



\## Project Structure



```text

csv-migration-validator/

├── validator.py

├── old\_data.csv

├── new\_data.csv

├── test\_validator.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Setup



Clone the repository and enter its folder:



```bash

git clone <your-repository-url>

cd csv-migration-validator

```



Create and activate a virtual environment on Windows:



```cmd

python -m venv .venv

.venv\\Scripts\\activate

```



Install the test dependency:



```bash

python -m pip install -r requirements.txt

```



\## Run the Validator



Compare the sample CSV files:



```bash

python validator.py old\_data.csv new\_data.csv

```



The program prints a summary and creates `migration\_report.json`.



To use a different record ID column:



```bash

python validator.py old\_data.csv new\_data.csv --id-column employee\_id

```



To choose a different report path:



```bash

python validator.py old\_data.csv new\_data.csv --output report.json

```



\## Run Automated Tests



```bash

python -m pytest -v

```



The test suite checks record changes, duplicate IDs, missing ID columns, blank record IDs, and column changes.



\## Report Contents



The JSON report includes:



\- Counts of old and new records

\- Added, removed, changed, and unchanged record IDs

\- Field-level old and new values for changed records

\- Duplicate IDs in each file

\- Columns added or removed in the new export



\## Current Limitations



This project compares CSV exports using a selected record ID and exact text values after trimming surrounding whitespace. It does not directly connect to databases or verify database transactions. Duplicate IDs are reported, while comparisons use the first occurrence of each ID. Review the report before making migration decisions.



\## Purpose



This project demonstrates Python programming, file processing, input validation, data comparison, JSON reporting, error handling, and automated testing.



