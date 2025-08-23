FROM python:3.12.11-slim-trixie

# Install build-essential for C-extensions and clean up to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /web

# Copy and install requirements first to leverage Docker cache
COPY requirements.txt .
RUN python -m pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application
COPY . .

# Set environment variable for port
ENV PORT=5000
EXPOSE ${PORT}

# Copy and make entrypoint executable
COPY entrypoint.sh /web/entrypoint.sh
RUN chmod +x /web/entrypoint.sh

# Run entrypoint
CMD ["/web/entrypoint.sh"]