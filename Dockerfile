FROM registry.redhat.io/rhel9/python-312

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

USER root

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY config/ ./config/

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev

USER 1001
EXPOSE 8000

ENTRYPOINT [".venv/bin/scale-mcp-server"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
