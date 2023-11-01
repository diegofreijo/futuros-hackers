# Use an official Python runtime as a parent image
# FROM python:3.9.18-slim
FROM python:3

# Configure apt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get -y install --no-install-recommends sqlite3 2>&1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose a port to run the Flask application (default is 5000)
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_ENV=production
ENV FLASK_ENV=development

# Command to run the Flask application
CMD ["flask", "run"]
