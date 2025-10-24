FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

# Expose ports for FastAPI (8001) and Prefect (4201)
EXPOSE 8001

# Make script executable
RUN chmod +x bin/run_services.sh

# Run both services using the bash script
CMD ["bash", "bin/run_services.sh"]
