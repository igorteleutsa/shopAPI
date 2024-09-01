# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to avoid buffering and ensure that the application outputs logs in real-time
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
