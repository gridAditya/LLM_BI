# Use the official Python 3.10 image as a base
FROM python:3.10-slim

# Set environment variables to ensure non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install additional dependencies
RUN apt-get update \
    && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment
RUN python3 -m venv /venv

# Use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python packages
RUN pip install --upgrade pip \
    && pip install mysqlclient \
    && pip install -r requirements.txt

# Define the command to run your application
CMD ["uvicorn", "api:app", "--reload", "--host=0.0.0.0", "--port=8000"]
