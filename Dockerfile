# ============================
# Stage 1: Build dependencies
# ============================
FROM python:3.12-alpine AS builder

# Install system dependencies needed for building some Python packages
RUN apk add --no-cache build-base

# Set working directory inside the image
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies into a temporary folder
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# ============================
# Stage 2: Final runtime image
# ============================
FROM python:3.12-alpine

# Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . ./app

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app/app.py \
    FLASK_ENV=production

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]

# CMD ["flask", "run", "--host=0.0.0.0"]
