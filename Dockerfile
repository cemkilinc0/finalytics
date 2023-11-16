# Use the latest official Python runtime as a base image
FROM python:3.11

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install the requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd
RUN apt-get update && apt-get install -y postgresql-client

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run gunicorn when the container launches
CMD ["gunicorn", "router.wsgi:application", "--bind", "0.0.0.0:8000"]

COPY docker_run.sh /usr/src/app/docker_run.sh
