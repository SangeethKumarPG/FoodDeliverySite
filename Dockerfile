# Use official slim Python base image as requested
FROM python:3.12.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r django && useradd -r -g django -s /sbin/nologin -d /app django

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=django:django . .

# Ensure necessary directories exist and have correct permissions
# Create static and media folders to avoid Django warnings/errors
RUN mkdir -p /app/static /app/media /app/staticfiles && \
    chown -R django:django /app/static /app/media /app/staticfiles /app

# SQLite security: Ensure the database folder is writable by the django user
# (SQLite requires write permission on the parent directory to create journal files)
RUN if [ -f db.sqlite3 ]; then \
        chown django:django db.sqlite3 && \
        chmod 664 db.sqlite3; \
    fi && \
    chmod 775 /app

# Add and setup entrypoint script
COPY --chown=django:django docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh && \
    sed -i 's/\r$//' /app/docker-entrypoint.sh

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
