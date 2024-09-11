FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port the app runs on
EXPOSE 5000

# Set the entrypoint script as the command to run on container start
ENTRYPOINT ["./entrypoint.sh"]
