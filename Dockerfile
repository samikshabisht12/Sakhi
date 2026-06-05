# ==========================================
# Build Stage: React Frontend
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Build the frontend
COPY . .
RUN npm run build

# ==========================================
# Production Stage: FastAPI Backend
# ==========================================
FROM python:3.11-slim
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (required for bcrypt, psycopg2, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install backend dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend static files from the builder stage
COPY --from=frontend-builder /app/dist ./dist

# Expose port 8000
EXPOSE 8000

# Start the application using Gunicorn with Uvicorn workers
WORKDIR /app/backend
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
