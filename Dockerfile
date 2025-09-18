FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh


# Set work directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

# Run app with Gunicorn
CMD ["uv", "run", "gunicorn", "health_booking_system.wsgi:application", "--bind", "0.0.0.0:8000"]