# Project Structure

The project follows a Clean Architecture-oriented layout, with HTTP concerns in `app/api` and technical details in `app/infrastructure`.

```text
app/
  api/
    docs/
    exception_handlers/
    mappers/
    routers/
    schemas/

  application/
    bootstrap/
    use_cases/

  domain/
    entities/
    enums/
    exceptions/

  infrastructure/
    bootstrap/
    db/
      repositories/
    logging/
    settings/

  main.py
```

## `app/api`

HTTP layer. Contains FastAPI routers, request/response schemas, exception handlers, mappers, and OpenAPI response helpers.

This layer can depend on `application` and `domain`, but business rules should stay outside routers and schemas.

## `app/application`

Application layer. Contains use cases and application flow.

This layer should not depend on FastAPI, SQLAlchemy, or HTTP schemas.

## `app/domain`

Domain layer. Contains the core business concepts: entities, enums, exceptions, and repository contracts when needed.

This layer should not depend on outer layers.

## `app/infrastructure`

Technical layer. Contains dependency injection setup, settings, logging, persistence implementations, in-memory database helpers, and future integrations.

Concrete repositories live here because they are implementation details of application contracts.
