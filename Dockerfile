# Stage 1: Builder (has all the build tools)
FROM python:3.9-slim AS builder

WORKDIR /web

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc g++ make \
    postgresql-client \  
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Install Node deps
COPY package.json package-lock.json* ./
RUN npm ci

# 🔑 Copy the rest of the app (including gavel/static/css/tailwind.scss)
COPY . .

# Now that source files are present, run the build
RUN npm run build


# Stage 2: Final Runtime Image (slim, no build tools)
FROM python:3.9-slim

WORKDIR /web

# Copy only the installed Python packages from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy the built static assets from the builder stage
COPY --from=builder /web/gavel/static/generated.scss /web/gavel/static/
# Copy the application source code
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PORT=5001
EXPOSE ${PORT}

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]
