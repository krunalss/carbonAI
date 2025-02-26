# Use Python 3.12.7 slim version for a lightweight image
FROM python:3.12.7-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install system dependencies (for FastAPI & Groq API)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 7860 (FastAPI default)
EXPOSE 7860

# Command to run FastAPI using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
