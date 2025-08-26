# Stage 1: Builder (has all the build tools)
FROM python:3.9-slim as builder

WORKDIR /web

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc g++ make \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY package.json package-lock.json* ./
RUN npm ci && \
    echo "Contents of working directory:" && ls -la && \
    echo "Contents of gavel/static/css:" && ls -la gavel/static/css && \
    echo "Contents of tailwind.scss:" && cat gavel/static/css/tailwind.scss && \
    npm run build

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
ENV PORT=5000
EXPOSE ${PORT}

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]