FROM python:3.9-slim

# Install necessary Python packages
RUN pip install fastapi uvicorn[standard] kubernetes jinja2

# Set the working directory
WORKDIR /app

# Copy application code and templates
COPY main.py /app
COPY templates /app/templates

# Expose port 80
EXPOSE 80

# Set the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

