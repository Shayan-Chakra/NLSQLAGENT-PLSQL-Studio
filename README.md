# NLSQLAGENT — PL/SQL Studio (HTML/CSS/JavaScript + FastAPI)

NLSQLAGENT converts natural-language requests into Oracle PL/SQL source code using Gemini. This is a generation-only tool: **it does not connect to Oracle and does not execute generated SQL/PLSQL**. `schema.py` is descriptive context only.

## UI features

- Polished responsive workspace with light/dark appearance toggle
- Prompt library for anonymous blocks, procedures, functions, packages, triggers, cursors, exceptions, and conditions
- Code type selection and options for comments, exception handling, and usage examples
- Prompt refinement, character counter, and Ctrl/Cmd+Enter shortcut
- Generated code, explanation, risk label, and preliminary structure-check message
- Copy code, copy explanation, edit locally, wrap/no-wrap, regenerate, clear, and download actions
- Schema reference panel

## Windows setup

Run in Command Prompt or the VS Code terminal from the project root:

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Create `.env` only if it does not already exist:

```cmd
copy .env.example .env
notepad .env
```

Set `GEMINI_API_KEY` and `GEMINI_MODEL` to values that work for your Google AI Studio account. Preserve an existing working `.env`. Never share or commit `.env`.

Start the app:

```cmd
python -m uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Validation and safety

The preliminary check is only a structural check; it is not a full PL/SQL parser and not Oracle compilation. Edited code is local to the page and is not revalidated. Review all generated code before using it in an Oracle environment, especially code containing DML, DDL, dynamic SQL, triggers, or calls to stored program units.

## No database integration

No Oracle driver is required. `db.py`, `db_setup.py`, `db_check.py`, Oracle credentials, and execution endpoints are not used by this app. Schema metadata is loaded from `schema.py` and does not imply the database tables exist.
