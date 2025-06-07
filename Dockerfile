# Dockerfile

# --- Builder Stage ---
# CHANGE 1: Match your local Python version
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
# CHANGE 1 (Again): Match your local Python version
FROM python:3.9-slim-buster

# Create a dedicated, non-root user for security
RUN addgroup --system app && adduser --system --group app

# Set the working directory for the new user
WORKDIR /home/app

# Install only the RUNTIME system dependencies.
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

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

# CHANGE 2: Set the correct path to your project's WSGI application
CMD ["gunicorn", "PNRStatusTracker.wsgi:application"]