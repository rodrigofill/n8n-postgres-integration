FROM python:3.11-slim

# Install system dependencies for build and Postgres client libs
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy Poetry files first (for dependency resolution)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies without creating a virtualenv inside container
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main --no-root

# Copy the rest of the code
COPY . .

# Default command will be overridden by docker-compose