# HelpDesk Hub API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)
![Project](https://img.shields.io/badge/Project-Portfolio%20Project-6f42c1)

Backend API for internal support ticket management, built as a portfolio project during the Backend with Python mentorship.

## Overview

The goal of this project is to build a realistic backend application to handle internal support requests such as IT demands, system access issues, operational problems, and internal service workflows.

The project is being developed incrementally, starting with the application skeleton, architectural boundaries, and system endpoints before moving into business features.

## Current Features

- FastAPI application entrypoint
- initial HTTP router for system endpoints
- environment-based application settings
- architectural boundaries enforced with Import Linter
- development tooling with Ruff and pre-commit

## Available Endpoints

- `GET /` returns a simple entry message
- `GET /health` returns the current API health status
- `GET /info` returns service metadata from application settings
- `GET /ping` returns the current server timestamp

## Project Scope

The system is expected to include features such as:

- user registration
- login
- ticket creation
- ticket listing and filtering
- comments on tickets
- ticket assignment
- status updates
- history tracking
- metrics exposure
- simple automations
- simulated AI-based classification suggestions

## Planned Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- PostgreSQL
- SQLAlchemy
- Alembic
- python-dotenv
- Docker
- GitHub Actions

## Configuration

Application settings are centralized under `app/infrastructure/settings`.

Use a local `.env` file in the project root for environment-specific values and keep `.env.example` as the versioned reference.

Current environment variables:

- `APP_NAME`
- `APP_ENV`
- `APP_VERSION`

## Project Structure

The project follows an initial Clean Architecture-oriented layout:

```text
app/
  application/
    use_cases/
  api/
    docs/
    exception_handlers/
    mappers/
    routers/
    schemas/
  domain/
    entities/
  infrastructure/
    bootstrap/
    db/
    logging/
    settings/
  main.py
```

See [Project Structure](PROJECT_STRUCTURE.md) and [Clean Architecture Map](docs/dev/clean-architecture-map.md) for a more detailed explanation of the current structure and responsibilities.

## Running Locally

Install dependencies and run the API locally:

```bash
uv sync
uv run python main.py
```

The development server runs with reload enabled.

## Development Quality

![Ruff](https://img.shields.io/badge/Lint-Ruff-black)
![Pre-commit](https://img.shields.io/badge/Pre--commit-enabled-brightgreen)
![Import Linter](https://img.shields.io/badge/Architecture-Import%20Linter-blue)

Quality tooling is configured from the beginning of the project to keep the codebase consistent, enforce basic checks early, and protect architectural boundaries.

## Status

Project in progress, currently focused on foundation, structure, and first operational endpoints.
