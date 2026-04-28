FROM python:3.11-slim

WORKDIR /app

# Install system deps for common PDF libs (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app sources
COPY . /app

# Default port (Render injects $PORT at runtime)
ENV PORT=8000

# Use shell form so we can expand $PORT when container starts
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
