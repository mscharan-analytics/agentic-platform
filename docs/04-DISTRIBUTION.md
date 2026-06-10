# Distribution Guide

## For End Users (Developers)

### 1. Install via pip

```bash
pip install enterprise-agent-platform
```

Then start using:
```bash
agent-platform --goal "Your objective"
```

### 2. Install from source

```bash
git clone <repo>
cd enterprise-agent-platform
pip install -e .
agent-platform --goal "Your objective"
```

### 3. Use Docker (no Python needed)

```bash
docker pull enterprise-agent-platform:latest
docker run -it enterprise-agent-platform --goal "Your objective"
```

## For Package Maintainers

### Build wheel and source distribution

```bash
pip install build
python -m build
```

Outputs:
- `dist/enterprise_agent_platform-0.1.0-py3-none-any.whl` — wheel
- `dist/enterprise_agent_platform-0.1.0.tar.gz` — source

### Publish to PyPI

```bash
pip install twine
twine upload dist/*
```

### Build Docker image

```bash
docker build -f deployment/docker/Dockerfile -t enterprise-agent-platform:0.1.0 .
docker tag enterprise-agent-platform:0.1.0 enterprise-agent-platform:latest
docker push enterprise-agent-platform:latest
```

## Version bumping

Update version in `pyproject.toml`:
```toml
version = "0.2.0"
```

Then rebuild and republish.

## Testing before publish

```bash
pip install -e .[dev]
pytest
bash scripts/quality.sh
```
