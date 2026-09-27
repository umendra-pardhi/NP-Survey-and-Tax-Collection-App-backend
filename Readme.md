## SQL Server setup

The API connects to SQL Server through SQLAlchemy, `pyodbc`, and Microsoft ODBC
Driver 18. Apply `schema.db.sql` to the target database before using the API.
Docker Compose starts only the API; SQL Server is expected to be available
separately.

```bash
docker compose up --build

```
only api : docker compose build api

Set `API_PORT` in `.env` to configure the API port. Database credentials are
provided to the register, login, connectivity, and sync endpoints in each
request.

Use the SQL Server host name (or `host,port` / `host\\instance`) as `server`.
When the API runs in Docker on Windows and SQL Server runs on the host, use
`host.docker.internal` instead of `localhost`. The target schema is `dbo`.

The `/sync/local-to-remote/stream` endpoint accepts NDJSON in the request body.
Pass the database username and password in the `X-DB-Username` and
`X-DB-Password` headers, not in the URL. Use HTTPS when calling this endpoint
outside a trusted local network.

Photo upload endpoints and request examples are documented in
[photo-uploads-api.md](photo-uploads-api.md).

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



