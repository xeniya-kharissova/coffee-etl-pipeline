# Coffee ETL Pipeline

A modular Python ETL pipeline for extracting, validating, and aggregating coffee shop order data from CSV files with structured logging, JSON configuration, CLI support, and automated tests.

## Key Features

- **Memory-efficient extraction:** Streams raw CSV rows using a Python generator (`csv.DictReader`).
- **Config-driven validation:** Business rules (valid menu items, cup limits) are decoupled from code in `config.json`.
- **Clean/Error split:** Separates valid orders (`cleaned_orders.csv`) from rejected rows with explicit error reasons (`error.csv`).
- **Analytics report:** Exports summary metrics (total/clean/error counts, revenue, top drinks, revenue by client, error breakdown) to `report.json`.
- **Observability & resilience:** Structured console/file logging and custom decorators (`@measure_time`, `@retry`).
- **CLI interface:** Configurable input, output directory, and config file paths via `argparse`.
- **Automated testing:** Unit and integration test suite built with `pytest` (fixtures, `tmp_path`, error assertions).

## Project Structure

```text
coffee-etl-pipeline/
├── coffee_etl/
│   ├── __init__.py
│   ├── decorators.py      # @measure_time and @retry decorators
│   └── pipeline.py        # Extract, validate, transform, load, and reporting logic
├── tests/
│   └── test_pipeline.py   # Unit and integration tests (pytest)
├── config.json            # Menu and validation limits
├── main.py                # CLI entry point and logging setup
├── orders.csv             # Sample raw input data
├── requirements.txt       # Project dependencies
└── .gitignore
```
## Setup

**Prerequisites:** Python 3.11+

1. Clone the repository and move into the project folder:

```powershell
git clone https://github.com/xeniya-kharissova/coffee-etl-pipeline.git
cd coffee-etl-pipeline
```

2. Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

Run with default paths (`orders.csv`, `config.json`, `output/`):

```powershell
python main.py
```

Override paths via CLI flags:

```powershell
python main.py --input path/to/orders.csv --output-dir path/to/output --config path/to/config.json
```

View all available options:

```powershell
python main.py --help
```

## Running Tests

```powershell
python -m pytest -v
```