# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /home/umair/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt (if any)
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements to install"

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the script
CMD ["python", "./max_path_sum.py"]
