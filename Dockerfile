# Use an official lightweight Python image as the base image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create and set the working directory inside the container
WORKDIR /app

# Install system dependencies required for Rasa and the application
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rasa explicitly
RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir rasa==3.6.20

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the German language model for spaCy
RUN python -m spacy download de_core_news_sm

# Copy the entire Rasa application into the container
COPY . /app/

# Copy the start_services.sh script into the container
COPY start_services.sh /app/start_services.sh

# Ensure the script is executable
RUN chmod +x /app/start_services.sh

# Use the script as the container's default command
CMD ["/app/start_services.sh"]
