# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files
COPY pyproject.toml poetry.lock /app/

# Install dependencies (no dev, no virtualenv inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy the source code
COPY src/ /app/src/

# Expose port
EXPOSE 8000

# Start server
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
