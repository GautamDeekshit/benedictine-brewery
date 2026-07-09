# Base image for the Docker container, using Python 3.12
FROM python:3.12
# Set the working directory inside the container
WORKDIR /benedict
# Copy the requirements file into the container
COPY requirements.txt .
# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY benedict.py .
# Expose port 5050 for the Flask application
EXPOSE 5050
# Set the command to run the Flask application
CMD ["python", "benedict.py"]