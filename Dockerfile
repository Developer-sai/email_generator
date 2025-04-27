FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create output directory with appropriate permissions
RUN mkdir -p /app/output && chmod 777 /app/output

# Copy application files
COPY app/ app/
COPY data/ data/

# Set default environment variables
ENV DATA_PATH=/app/data/sample_leads.json \
    OUTPUT_PATH=/app/output \
    OPENAI_API_KEY=""

# Create a non-root user and switch to it
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set the entrypoint
CMD ["python", "app/main.py"]