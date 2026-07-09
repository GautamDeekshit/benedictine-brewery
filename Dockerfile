# Base image for the Docker container, using Python 3.12-slim for a lightweight environment
FROM python:3.12-slim AS builder
# Set the working directory inside the container
WORKDIR /benedict
# Copy the requirements file into the container
COPY requirements.txt .
# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt
# Final stage of the Docker build process, using the same base image
FROM python:3.12-slim
# Set the working directory inside the container
WORKDIR /benedict
# Copy installed Python packages from the builder stage into the final container
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# Copy the installed binaries from the builder stage into the final container
COPY --from=builder /usr/local/bin /usr/local/bin
# Copy the rest of the application code into the container
COPY app.py .
# Expose port 5050 for the Flask application
EXPOSE 5050
# Set the command to run the Flask application
CMD ["python", "app.py"]