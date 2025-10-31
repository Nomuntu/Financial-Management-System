# Use a lightweight official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies for WeasyPrint (HTML → PDF rendering)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libcairo2 libgdk-pixbuf-2.0-0 shared-mime-info fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project into the container
COPY . .

# Expose the Render-assigned port
ENV PORT=10000

# Tell Python not to buffer stdout/stderr (helps with logging)
ENV PYTHONUNBUFFERED=1

# Command to start your FastAPI backend
# NOTE: main.py should be in the project root, and must define `app`
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
