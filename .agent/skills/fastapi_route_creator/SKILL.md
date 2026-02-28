---
name: fastapi-route-creator
description: Generates a complete FastAPI endpoint. Use this whenever you need to add a new route or resource to the backend API.
---

# FastAPI Route Creator

Strict guidelines for creating new FastAPI endpoints and resources in the `life-map-back` project.

## When to use this skill
- When adding a new feature that requires an API endpoint.
- When creating a new data entity that needs CRUD operations.

## How to use it
To maintain the hexagonal architecture, you must NEVER write business logic or database queries directly in the API router. Always follow this 4-step process:

1. **SQLAlchemy Model (`app/models/`)**: Create or update the database model representing the SQL table. Ensure it inherits from the declarative base.
2. **Pydantic Schemas (`app/schemas/`)**: Create `Create`, `Update`, and `Read` (Response) schemas to validate input/output data.
3. **Service Layer (`app/services/`)**: Create or update the service class (e.g., `MyEntityService`). This class takes an `AsyncSession` in its `__init__` and contains all the business logic, database queries (`select`, `insert`, etc.), and transactions.
4. **FastAPI Router (`app/api/endpoints/`)**: Create the route handler. It must inject the database session `Depends(get_db)`, instantiate the Service, and call the service method. Return the Pydantic schema.

## Coding Standards
- Always use `async`/`await` for database operations.
- Handle HTTP Exceptions (e.g., `404 Not Found`) properly in the router if the service returns `None`.
- Register the new router in `app/api/v1/api.py` or the main `server.py` file.
