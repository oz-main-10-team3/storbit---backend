FROM python:3.13-slim

# Install System Packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set WORKDIR
WORKDIR /storbit

# install uv
RUN pip install uv

# copy uv setting files
COPY pyproject.toml uv.lock ./

# install dependencies
RUN uv sync --frozen --no-dev

ENV VIRTUAL_ENV=/storbit/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# copy project files
COPY . .

