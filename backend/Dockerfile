# backend/Dockerfile
FROM python:3.11-slim

# System libs required by WeasyPrint (HTML → PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libcairo2 libgdk-pixbuf-2.0-0 shared-mime-info fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Render provides $PORT; bind to it
ENV PORT=10000
CMD ["sh","-c","uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
