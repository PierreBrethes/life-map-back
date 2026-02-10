# Dockerfile

# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies required for building some python packages (e.g. pgvector/asyncpg usually need gcc/headers if pre-built wheels aren't matched, but mostly fine)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root --without dev --no-interaction --no-ansi

# Stage 2: Run
FROM python:3.11-slim

WORKDIR /app

# Install runtime libs like libpq if needed for asyncpg (usually needed)
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy installed packages and executables
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# Make entrypoint executable (and fix Windows line endings)
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Entrypoint runs migrations, then CMD starts the server
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
