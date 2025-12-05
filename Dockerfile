# Multi-stage build for Flask app
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port (Render sets PORT dynamically)
EXPOSE 5001

# Run the application with increased timeout for MongoDB connection
# Use PORT from environment (Render sets this automatically)
CMD gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 --graceful-timeout 30 app:app

