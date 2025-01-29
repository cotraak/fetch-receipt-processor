# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install required Python dependencies
RUN pip install flask

# Expose the Flask application port
EXPOSE 8080

# Run the Flask application
CMD ["python", "app.py"]
