FROM ghcr.io/astral-sh/uv:0.12.10 AS uv
FROM python:3.12-slim
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock alembic.ini ./
RUN uv sync --frozen --no-dev --no-install-project
COPY app ./app
COPY migrations ./migrations
COPY docker-entrypoint.py ./docker-entrypoint.py
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --no-create-home app
EXPOSE 8000
CMD [".venv/bin/python", "docker-entrypoint.py"]
