# Nagar Panchayat App — API Overview

This document explains the API structure and how to run and interact with the backend in `app/`.

## Quick start

- Create a virtual environment and install dependencies from the top-level `requirements.txt`:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

- Run the server with Uvicorn from the project root:

```bash
uvicorn app.main:app --reload
```

## Important files

- [app/main.py](app/main.py#L1) — FastAPI application entrypoint.
- [app/routes.py](app/routes.py#L1-L200) — API routes: `/register`, `/login`, `/initial-connect`.
- [app/schemas.py](app/schemas.py#L1-L200) — Pydantic request/response schemas used by routes.
- [app/database.py](app/database.py#L1) — Dynamic session creation helpers.
- [app/services.py](app/services.py#L1) — Helper functions, e.g., `connect_to_gramdb`.
- [app/models.py](app/models.py#L1) — SQLAlchemy models (e.g., `User`).
- [app/auth.py](app/auth.py#L1) — Password hashing and JWT token helpers.

## Overview

This backend uses FastAPI and dynamically creates SQLAlchemy sessions for a target database provided in each API request. Requests include database credentials (server, database, username, password) because the app connects to different databases per client.

Important note: endpoints expect DB credentials in each request body (see schema reference below).

## API Endpoints

1) POST /register

- Purpose: Create a new user record in the target database.
- Request schema: `UserRegister` (extends `DBCredentials`) — fields:
  - `server` (str)
  - `database` (str)
  - `db_username` (str)
  - `db_password` (str)
  - `UserName` (str)
  - `Mobile` (optional str)
  - `EMail` (email)
  - `LoginID` (str)
  - `Password` (str)
  - `UserRole` (optional str)
  - `UserLocation` (optional bool)
  - `ClientID` (optional int)

- Success response: JSON with `success: True`, `message`, and `user_id`.

Example curl:

```bash
curl -X POST http://localhost:8000/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "server":"db-host",
    "database":"GramDB",
    "db_username":"dbuser",
    "db_password":"dbpass",
    "UserName":"Alice",
    "EMail":"alice@example.com",
    "LoginID":"alice01",
    "Password":"s3cret"
  }'
```

2) POST /login

- Purpose: Authenticate a user and return a bearer access token.
- Request schema: `UserLogin` (extends `DBCredentials`) — fields:
  - `server`, `database`, `db_username`, `db_password`
  - `LoginID` (str)
  - `Password` (str)

- Success response: `access_token`, `token_type`, and `user` info.

Example curl:

```bash
curl -X POST http://localhost:8000/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "server":"db-host",
    "database":"GramDB",
    "db_username":"dbuser",
    "db_password":"dbpass",
    "LoginID":"alice01",
    "Password":"s3cret"
  }'
```

3) POST /initial-connect

- Purpose: Validate given DB credentials and check connectivity to a target DB (helper used by clients before register/login).
- Request schema: `InitialDBConnectRequest` — fields:
  - `server` (str)
  - `database` (str, default "GramDB")
  - `db_username` (str)
  - `db_password` (str)

- Success response: HTTP 200 with connection details; failures return HTTP 400.

Example curl:

```bash
curl -X POST http://localhost:8000/initial-connect \\
  -H "Content-Type: application/json" \\
  -d '{
    "server":"db-host",
    "database":"GramDB",
    "db_username":"dbuser",
    "db_password":"dbpass"
  }'
```

## Security considerations

- Credentials are passed in request bodies; transport must use TLS in production.
- Passwords are hashed by `auth.hash_password` before being stored.
- JWT tokens are created by `auth.create_access_token`.

## Where to look next

- Inspect [app/routes.py](app/routes.py#L1-L200) for route behavior.
- Inspect [app/schemas.py](app/schemas.py#L1-L200) for exact request fields.
- Inspect [app/database.py](app/database.py#L1) and [app/services.py](app/services.py#L1) for connection logic.

