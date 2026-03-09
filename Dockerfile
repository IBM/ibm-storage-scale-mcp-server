FROM registry.redhat.io/rhel9/python-312

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

USER root

# Install Node.js 22 and nsolid for filesystem operations support
RUN curl -fsSL https://rpm.nodesource.com/setup_22.x | bash - && \
    yum install -y nsolid && \
    yum clean all

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY config/ ./config/

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev

USER 1001
EXPOSE 8000

# To add filesystem paths, override CMD when running:
# docker run -v /host/path:/container/path scale-mcp-server \
#   --transport http --host 0.0.0.0 --port 8000 --filesystem-paths /container/path
ENTRYPOINT [".venv/bin/scale-mcp-server"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
