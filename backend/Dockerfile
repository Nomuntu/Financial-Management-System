# Dockerfile (root of the repo)

FROM python:3.11-slim

# System libs required by WeasyPrint (HTML → PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libcairo2 libgdk-pixbuf-2.0-0 shared-mime-info fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# Helpful defaults for logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# App lives here
WORKDIR /app

# Install Python deps first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Ensure absolute imports like "from backend.routers ..." work
ENV PYTHONPATH=/app

# Healthcheck (optional but nice on Render)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD \
  python - <<'PY' || exit 1
import urllib.request, os
url = f"http://127.0.0.1:{os.environ.get('PORT','10000')}/"
with urllib.request.urlopen(url, timeout=3) as r:
    exit(0 if r.status == 200 else 1)
PY

# Start FastAPI from backend/main.py
# Render injects $PORT. Locally it will default to 10000.
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
