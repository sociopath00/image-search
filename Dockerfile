FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_CACHE_DIR="/root/.cache/uv"
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files early
COPY pyproject.toml uv.lock ./

# Install uv and use it immediately
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv pip compile pyproject.toml > requirements.txt && \
    uv venv && \
    uv pip install -r requirements.txt

# Copy all application code
COPY . .

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisord.conf

# Expose FastAPI and Streamlit ports
EXPOSE 8000 8501

# Launch both apps
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
