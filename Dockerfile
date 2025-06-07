# Dockerfile

# --- Builder Stage ---
# Use an official Python runtime. Change the version to match yours (e.g., 3.11, 3.9)
FROM python:3.9-slim-buster as builder

# Set environment variables to prevent Python from writing .pyc files and to run in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy the requirements file and install python dependencies into a temporary location ("wheels")
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# --- Final Stage ---
# Start from a fresh, slim Python image
FROM python:3.9-slim-buster

# Create a dedicated, non-root user for security
RUN addgroup --system app && adduser --system --group app

# Set the working directory for the new user
WORKDIR /home/app

# ----------------- THE ONLY CHANGE IS ON THE NEXT LINE -----------------
# Install only the RUNTIME system dependencies.
# ADDED: libgl1 - this is a key dependency for headless OpenCV (cv2)
RUN apt-get update && apt-get install -y libpq5 libgl1 && rm -rf /var/lib/apt/lists/*
# -----------------------------------------------------------------------

# Copy the pre-built Python packages ("wheels") from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

# Install the Python packages
RUN pip install --no-cache /wheels/*

# Copy your application code into the container
# Use "app" user for ownership
COPY --chown=app:app . .

# Switch to the non-root user
USER app

# Set the correct path to your project's WSGI application
CMD ["gunicorn", "PNRStatusTracker.wsgi:application"]