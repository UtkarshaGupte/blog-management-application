# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y netcat-openbsd gcc postgresql \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Add the rest of the code
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Execute the Django web server
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000"]
