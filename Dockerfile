# Take 139 Backend — Dockerfile for Railway deployment
# Uses Debian slim with full WeasyPrint system dependencies

FROM python:3.11-slim

# System packages WeasyPrint needs (Pango, Cairo, GDK-Pixbuf, GObject, fonts)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi8 \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose the port Railway will set
ENV PORT=8000
EXPOSE 8000

# Start the server
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
