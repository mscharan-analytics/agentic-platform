FROM python:3.11-slim AS builder

WORKDIR /build

ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE MANIFEST.in setup.py ./
COPY src/ ./src
COPY docs/ ./docs
COPY scripts/ ./scripts
COPY deployment/ ./deployment

RUN python -m pip install --upgrade pip build \
    && python -m build

FROM python:3.11-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OLLAMA_BASE_URL=http://localhost:11434

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /usr/sbin/nologin appuser

COPY --from=builder /build/dist/*.whl /tmp/package.whl

# Install with ollama support. If ollama not available, platform still runs
# in degraded mode with cloud provider fallback or stub responses.
RUN python -m pip install /tmp/package.whl \
    && python -m pip install ollama>=0.1.0 httpx>=0.24.0 --no-deps || true \
    && rm /tmp/package.whl

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import agent_platform; print('ok')" || exit 1

ENTRYPOINT ["agent-platform"]
CMD ["--goal", "Initialize platform with Ollama support (optional)"]
