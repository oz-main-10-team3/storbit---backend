FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /storbit

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv pip install -e . --system
COPY . .
