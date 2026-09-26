## PostgreSQL setup

The API uses PostgreSQL through SQLAlchemy and psycopg. Docker Compose starts
PostgreSQL, loads `schema.postgres.sql` when the data volume is first created,
and exposes PostgreSQL on port 5432 by default.

```bash
docker compose up --build

```
only api : docker compose build api

Set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`, and
`API_PORT` in `.env` to configure the services. The schema file is only applied
when PostgreSQL initializes an empty data volume.

The register, login, connectivity, and sync endpoints still accept database
credentials in their request bodies. For an API running on the host, use
`localhost` as `server`; for an API container connecting to this Compose
database, use `postgres`. PostgreSQL listens on port 5432.

The `/sync/local-to-remote/stream` endpoint accepts NDJSON in the request body.
Pass the database username and password in the `X-DB-Username` and
`X-DB-Password` headers, not in the URL. Use HTTPS when calling this endpoint
outside a trusted local network.

To run the API directly from the host:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

User Credentials
Admin User
Login ID: admin
Password: Admin@123
Role: ADMIN

Numbering User
Login ID: numbering
Password: Numbering@123
Role: NUMBERING

Survey User
Login ID: survey
Password: Survey@123
Role: SURVEY

Tax User
Login ID: tax
Password: Tax@123
Role: TAX



