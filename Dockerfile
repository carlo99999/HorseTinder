FROM python:3.13.11-slim
WORKDIR /workspace
COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project
COPY apps/api ./apps/api
ENV PATH="/workspace/.venv/bin:$PATH" \
    PYTHONPATH="/workspace/apps/api"
