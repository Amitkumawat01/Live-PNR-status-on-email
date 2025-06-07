# Dockerfile

# --- Builder Stage ---
    FROM python:3.9-slim-buster as builder

    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    
    # Set the working directory
    WORKDIR /usr/src/app
    
    # Install system dependencies required for building Python packages
    RUN apt-get update && apt-get install -y libpq-dev gcc
    
    # Copy the requirements file and install python dependencies
    COPY requirements.txt .
    RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
    
    
    # --- Final Stage ---
    FROM python:3.9-slim-buster
    
    # Create a non-root user
    RUN addgroup --system app && adduser --system --group app
    
    # Set the working directory
    WORKDIR /home/app
    
    # ----------------- THE ONLY CHANGE IS ON THE NEXT LINE -----------------
    # Install a comprehensive set of RUNTIME system dependencies for Django and OpenCV.
    # libpq5: for Postgres
    # libgl1, libglib2.0-0, libsm6, libxext6: Common dependencies for headless OpenCV
    RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        && rm -rf /var/lib/apt/lists/*
    # -----------------------------------------------------------------------
    
    # Copy pre-built wheels from the builder stage
    COPY --from=builder /usr/src/app/wheels /wheels
    COPY --from=builder /usr/src/app/requirements.txt .
    
    # Install the Python packages
    RUN pip install --no-cache /wheels/*
    
    # Copy your application code
    COPY --chown=app:app . .
    
    # Switch to the non-root user
    USER app
    
    # Set the correct CMD
    CMD ["gunicorn", "PNRStatusTracker.wsgi:application"]