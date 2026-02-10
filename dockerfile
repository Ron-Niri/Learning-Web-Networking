FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app
# Copy the simple python web server
COPY main.py .

# Copy the static files
COPY static/ ./static/

# Expose port Coolify will route
EXPOSE 8080
# Runnnnnnn
CMD ["python", "main.py"]
