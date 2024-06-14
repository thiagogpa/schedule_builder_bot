# Use an official Python runtime as the base image
# FROM python:3.9
FROM python:3.9-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python files to the container
COPY . .

# Set the command to run the Python program
# CMD [ "python", "bot.py" ]
CMD ["gunicorn", "-b", ":43555", "--log-level", "debug", "--access-logfile", "-", "wsgi:app"]
