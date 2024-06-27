FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y vim && apt-get install -y curl

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the health check script into the container
COPY healthcheck-script.sh /usr/local/bin/healthcheck-script.sh

# Make the health check script executable
RUN chmod +x /usr/local/bin/healthcheck-script.sh

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your Flask app
CMD ["python", "cloud-alert.py"]

# Define the health check instruction
HEALTHCHECK --interval=30s --timeout=10s CMD /usr/local/bin/healthcheck-script.sh http://localhost:8080/alerts 200

#test
# FROM python:3.12-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y vim && apt-get install -y curl

# COPY . /app

# COPY healthcheck-test.sh /usr/local/bin/healthcheck-test.sh

# RUN chmod +x /usr/local/bin/healthcheck-test.sh

# RUN pip install --upgrade pip

# RUN pip install -r requirements.txt

# CMD ["python", "cloud-alert.py"]

# HEALTHCHECK --interval=10s --timeout=10s --start-period=20s CMD /usr/local/bin/healthcheck-test.sh

