# HelpDesk Hub API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

Internal support ticket API for categorizing, tracking, and discussing operational issues across service desk workflows.

## Overview

HelpDesk Hub API is a layered FastAPI application designed to look and evolve like a real product backend. It currently supports categories, tickets, and ticket comments, with PostgreSQL persistence through SQLAlchemy and a test suite that exercises the main flows end to end.

It is aimed at internal support and operations scenarios where teams need a structured backend for organizing issue intake, prioritization, and follow-up.

## Current Capabilities

- create, list, get, and update categories
- create, list, get, and update tickets
- filter tickets by `status`, `priority`, and `category_id`
- paginate and sort ticket listings by `id`, `title`, `priority`, and `status`
- create, list, and update comments inside a ticket
- seed default categories automatically at application startup
- validate requests with Pydantic and centralize dependency wiring with `dependency-injector`

## Prerequisites

- Python 3.11+
- `uv`
- PostgreSQL

## Run Locally

1. Install dependencies:

```bash
uv sync
```

2. Create `.env` from `.env.example` and point `DATABASE_URL` to an accessible PostgreSQL database.

3. Start the application:

```bash
uv run python main.py
```

The API runs at `http://127.0.0.1:8000` by default.

Interactive API docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Configuration

Application settings are loaded from `.env` through [settings.py](app/infrastructure/settings/settings.py).

```env
PROJECT_NAME=helpdesk-hub-api
PROJECT_TITLE=HelpDesk Hub API
PROJECT_DESCRIPTION=Technical support ticket management API
PROJECT_VERSION=0.1.0
ENVIRONMENT=development
PORT=8000
LOG_LEVEL=INFO
DATABASE_URL=postgresql+psycopg://helpdesk_user:helpdesk_password@localhost:5432/helpdesk_db
RUN_POSTGRES_TESTS=false
```

Main variables:

- `ENVIRONMENT`
- `PORT`
- `LOG_LEVEL`
- `DATABASE_URL`
- `RUN_POSTGRES_TESTS`

## Example Workflow

Create a category:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hardware",
    "description": "Incidents related to physical devices",
    "is_active": true
  }'
```

Example response:

```json
{
  "success": true,
  "message": "Categoria criada com sucesso",
  "data": {
    "id": 1,
    "name": "Hardware",
    "description": "Incidents related to physical devices",
    "is_active": true
  }
}
```

Create a ticket:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Laptop not booting",
    "description": "Device stays on black screen after startup",
    "category_id": 1,
    "priority": "high"
  }'
```

In practice, use the `id` returned by the category creation response. If seeded categories already exist, the created category may not be `1`.

List tickets with filters, sorting, and pagination:

```bash
curl "http://127.0.0.1:8000/api/v1/tickets?status=open&priority=high&sort_field=priority&sort_direction=desc&page=1&page_size=10"
```

## API Surface

Base prefix: `/api/v1`

- System health and metadata: `/`, `/live`, `/health`, `/info`, `/ping`
- Category management: `GET/POST /categories`, `GET/PATCH /categories/{category_id}`
- Ticket lifecycle: `GET/POST /tickets`, `GET/PATCH /tickets/{ticket_id}`
- Ticket discussion: `GET/POST /tickets/{ticket_id}/comments`, `PATCH /tickets/{ticket_id}/comments/{comment_id}`

## Behavior Notes

- The application creates database tables automatically at startup with `Base.metadata.create_all(...)`.
- Default categories are seeded during the FastAPI lifespan and are not recreated if they already exist.
- The active dependency container currently uses the SQLAlchemy repositories.
- In-memory repositories are still present in the codebase as historical reference and for behavior comparison.

## Testing

Integration tests derive the test database from `DATABASE_URL` by appending `_test` to the configured database name.

Example:

- app database: `helpdesk_db`
- test database: `helpdesk_db_test`

The `_test` database must already exist and should be used only for tests.

During the integration suite:

- `ENVIRONMENT` is forced to `test`
- the schema is recreated at session start
- data is cleared between tests with `TRUNCATE ... RESTART IDENTITY CASCADE`

Run the main checks:

```bash
uv run pytest -p no:cacheprovider -q
uv run ruff check .
uv run mypy .
```

`RUN_POSTGRES_TESTS=true` enables the explicit PostgreSQL connectivity test.

Note: `mypy` still reports known FastAPI router typing issues around `responses={**...}`.

## Development Quality

The project uses `pytest`, `Ruff`, `mypy`, and Import Linter to keep behavior, code quality, and architectural boundaries consistent as the codebase evolves.

## Architecture

The project follows a layered structure:

- `app/api`: HTTP layer, routers, schemas, mappers, exception handlers
- `app/application`: use cases, DTOs, and repository contracts
- `app/domain`: entities, enums, and domain exceptions
- `app/infrastructure`: settings, logging, dependency container, bootstrap, and persistence implementations

For the detailed layout, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Status

The project is currently consolidating the persistence layer and the main ticket flow. The next natural steps are authentication, formal Alembic migrations, history tracking, and deeper business rules.
