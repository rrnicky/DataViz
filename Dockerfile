# Use full Python image (has build tools + libs already)
FROM python:3.11

# Set work directory
WORKDIR /app

# Copy requirements first (leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies (prebuilt wheels will be used)
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Render-required port
EXPOSE 10000

# Start app
CMD ["python", "app.py"]
