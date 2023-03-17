# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the rest of the application code into the container
COPY requirements.txt .
COPY shipgame .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create dir and file for logger
RUN mkdir -p /app/logs
RUN touch /app/logs/request_logs.json

# Set environment variables for Django settings
ENV DJANGO_SETTINGS_MODULE=shipgame.settings
ENV PYTHONUNBUFFERED 1

# Pass environment variables from a local .env file to the Docker container
ENV ENV_FILE_PATH=/app/.env
COPY .env $ENV_FILE_PATH

# Expose port 8000 for the Django application
EXPOSE 8000

# Run migrations and crate db
RUN python /app/manage.py migrate

# Start the Django application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "shipgame.wsgi:application", "--workers=4"]
