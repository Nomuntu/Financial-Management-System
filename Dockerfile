# Use a lightweight official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system libs required by WeasyPrint (HTML → PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libcairo2 libgdk-pixbuf-2.0-0 shared-mime-info fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Render expects
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# Start FastAPI using the root main.py proxy
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
