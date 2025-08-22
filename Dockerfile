FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (needed for pandas/scipy/sklearn sometimes)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libatlas-base-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Render requires 10000)
EXPOSE 10000

# Start app
CMD ["python", "app.py"]
