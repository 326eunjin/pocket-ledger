# PocketLedger

PocketLedger is an independently owned personal side project by Eunjin Jang
([326eunjin](https://github.com/326eunjin)). Its long-term goal is expense tracking,
monthly budgeting, and credit card payment planning. This initial MVP is a small
local backend prepared for a Labelbox Bring Your Own Project (BYOP) application.

## Implemented features

- Create, list, and retrieve expenses with SQLite persistence.
- Fields: ID, amount, category, description, expense date, and UTC creation timestamp.
- Positive amounts with up to two decimal places and 12 total digits; nonblank
  categories (up to 100 characters), descriptions (up to 1,000 characters), and
  valid dates. Description defaults to an empty string.
- HTTP 201 on creation, 200 on reads, 422 for invalid input, and 404 for missing IDs.
- Isolated automated API tests, including persistence across application restarts.

Amounts are stored as integer hundredths to avoid floating-point rounding and
returned as decimal strings (for example, `"12.50"`). The MVP assumes one currency
with two fractional digits; currency selection and conversion are not implemented.
Categories are free text. Dates may be past or future.

## Technology stack

Python 3.11+, FastAPI, SQLite, SQLAlchemy 2, Pydantic 2, and Pytest.
Uvicorn runs the server; HTTPX supports the API tests.

## Local setup

From the repository root, on macOS or Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, use `py -3.11 -m venv .venv` and activate with
`.venv\Scripts\Activate.ps1` in PowerShell.

Start the development server from the repository root:

```sh
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

SQLite tables are created on startup in `pocket_ledger.db` in the working directory.
The database persists across restarts and is excluded from Git. Interactive API
documentation is available at <http://127.0.0.1:8000/docs>.

## Example API requests

All examples use fictional data:

```sh
curl -X POST http://127.0.0.1:8000/expenses \
  -H 'Content-Type: application/json' \
  -d '{"amount":"12.50","category":"Food","description":"Fictional lunch","expense_date":"2026-11-01"}'

curl 'http://127.0.0.1:8000/expenses?offset=0&limit=100'
curl http://127.0.0.1:8000/expenses/1
```

The list endpoint returns records by ascending ID, with default `offset=0` and
`limit=100` (maximum 100). A newly created record resembles:

```json
{
  "id": 1,
  "amount": "12.50",
  "category": "Food",
  "description": "Fictional lunch",
  "expense_date": "2026-11-01",
  "created_at": "2026-11-04T12:00:00Z"
}
```

The timestamp above is illustrative; the server generates the actual timestamp.

## Tests

```sh
python -m pytest -q
```

Each test receives its own temporary SQLite file through Pytest's `tmp_path`.
Tests do not read or write the local application database.

## Planned work and limitations

Expense editing/deletion, category management, monthly budgets, credit card billing
cycles, installment calculations, analytics, a React frontend, expanded tests, and
Docker/deployment work remain unimplemented. See [ROADMAP.md](ROADMAP.md) for an
estimated 46 hours of future work. Estimates are planning guidance, not logged work.

This MVP has no authentication, banking integrations, frontend, or production
deployment. Use it locally with fictional data only. Schema migrations and
production operational hardening are future work; automatic table creation does
not migrate existing schemas.

## Ownership, data, and license

This is Eunjin Jang's personally owned, independent project, licensed under the
existing [MIT License](LICENSE). No employer code or confidential information is
intended for this repository. Use only fictional sample data; do not add personal,
customer, banking, or regulated financial data, credentials, or API keys.
Local databases, environment files, virtual environments, and generated caches
are ignored by Git. No real banking service is integrated.

BYOP acceptance and eligibility must be confirmed against the program's current
requirements. This repository does not claim approval, prior releases, users,
or deployment history.
