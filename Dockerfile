FROM python:3.8.17

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create and set working directory
RUN mkdir /chalkmate
WORKDIR /chalkmate

# Install system dependencies (optional, if needed)
RUN apt-get update && apt-get install -y \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Add the requirements.txt file to the container
ADD requirements.txt /chalkmate/

# Create a virtual environment and install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Add the rest of the project files
ADD . /chalkmate/

# Expose the default Django port
EXPOSE 8000

# Start the Django server
CMD ["/bin/bash", "-c", "source venv/bin/activate && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
