# CouponHunter MVP

This repository contains an MVP implementation of CouponHunter per the project specification.

Quickstart (Windows PowerShell):

1. Install Python 3.11+ and ensure `py` launcher is available.
2. Create and activate virtual environment:

   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Install dependencies:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

4. Copy environment file and set ADMIN_TOKEN:

   copy .env.example .env
   # Edit .env and set ADMIN_TOKEN to a secure token

5. Initialize database:

   python scripts/init_db.py

6. Run the app (development):

   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

7. Open http://127.0.0.1:8000 in your browser.

Importing coupons (MVP - file upload):

- Create a Source (admin): POST /api/sources with JSON body {"name":"Manual import","source_type":"manual","url":null}
  Include header X-Admin-Token with the ADMIN_TOKEN value.
- Use the Admin UI /admin to upload a CSV or JSON file against the source_id.
- CSV example (headers): code,discount_value,min_order_value

Security notes:
- Admin endpoints require X-Admin-Token header matching ADMIN_TOKEN in .env.
- Remote syncing from arbitrary URLs is disabled in MVP to avoid SSRF and ToS issues.
- Maximum import file size: 5 MB. Maximum rows: 5000.

Tests:

- Run tests with:

  python -m pytest -q

If you need Termux instructions or deployment on a VPS, see the docs/notes section below.
