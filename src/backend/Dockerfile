# Use a lightweight Python base image
FROM python:3.11-slim
 
# Set the working directory inside the container
WORKDIR /app
 
# Install system dependencies needed by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
 
# Copy requirements first (Docker caches this layer if requirements don't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the rest of the application code
COPY . .
 
# Create the uploads folder
RUN mkdir -p /app/uploads
 
# Expose the port FastAPI will run on
EXPOSE 5000
 
# Run the FastAPI server with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
 
