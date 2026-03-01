FROM ghcr.io/astral-sh/uv:debian-slim

# Copy the project into the image
COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

ENV STATIC_ROOT /static
CMD ["/app/entrypoint.sh"]
