# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Copy the .env file into the container
COPY .env /app/.env

# Apply migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
