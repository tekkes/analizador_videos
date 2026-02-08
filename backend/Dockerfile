# Use an official lightweight Python image.
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
# We need ffmpeg for audio processing and git for some python packages if needed.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
