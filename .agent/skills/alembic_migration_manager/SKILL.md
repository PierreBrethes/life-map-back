---
name: alembic-migration-manager
description: Manage database migrations securely using Alembic and Docker. Use this after modifying SQLAlchemy models to apply changes to the database.
---

# Alembic Migration Manager

Strict guidelines for managing PostgreSQL schema changes securely.

## When to use this skill
- Every time a SQLAlchemy model (in `app/models/`) is modified, created, or deleted.
- When applying schema updates to the running database.

## How to use it
Always execute Alembic commands inside the running API Docker container to ensure the correct environment and database connections are used.

1. **Auto-generate Migration**:
   After changing your `app/models/`, run this command to generate the migration file:
   ```bash
   docker exec lifemap-api python -m alembic revision --autogenerate -m "brief description of changes"
   ```
   *Always review the generated migration file in `alembic/versions/` to verify it accurately reflects your intent before applying it.*

2. **Apply Migration**:
   Apply the changes to the database:
   ```bash
   docker exec lifemap-api python -m alembic upgrade head
   ```

3. **Rollback (If needed)**:
   If a migration needs to be undone:
   ```bash
   docker exec lifemap-api python -m alembic downgrade -1
   ```

## Rules
- Never modify the database schema manually via SQL.
- Never edit an existing migration file that has already been merged or applied in production environments; always create a new migration to fix issues.
