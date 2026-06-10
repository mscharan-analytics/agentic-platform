# CI/CD Setup

This repository is configured for a GitHub Actions CI/CD flow using a self-hosted runner.

## Branching Flow

1. Create a feature branch from `main`.
2. Push the branch and open a pull request.
3. Let CI validate tests, linting, typing, package build, and Docker build when Docker is available on the runner.
4. Merge after CI is green.
5. Cut a `v*` tag or run the release workflow manually to publish artifacts.

## CI Workflow

The CI workflow lives in [ci.yml](../.github/workflows/ci.yml).

It runs on pull requests and branch pushes and performs:

- `pytest -q`
- `ruff check src tests`
- `mypy src --ignore-missing-imports`
- `python -m build`
- Docker image build validation using `deployment/docker/Dockerfile`

The workflow targets `runs-on: self-hosted`.

## Release Workflow

The release workflow lives in [release.yml](../.github/workflows/release.yml).

It runs on:

- tag push matching `v*`
- manual `workflow_dispatch`

It performs a quality gate first, then can publish:

- Python distributions to PyPI
- Container images to the configured registry

If publish credentials are missing, the workflow skips the publish step but still completes the build.
If Docker is not installed on the runner, container-specific steps are skipped.

## Required Secrets

Configure these repository secrets before enabling publishing:

- `PYPI_TOKEN`: PyPI API token for `twine upload`
- `CONTAINER_REGISTRY_USERNAME`: container registry username
- `CONTAINER_REGISTRY_PASSWORD`: container registry password or access token

## Optional Repository Variables

Configure these repository variables to control container publishing:

- `CONTAINER_REGISTRY`: registry hostname, for example `ghcr.io`
- `CONTAINER_IMAGE_NAME`: full image name path, for example `org/enterprise-agent-platform`

Defaults:

- registry defaults to `ghcr.io`
- image name defaults to `${{ github.repository }}` inside the workflow

## Deployment Notes

- The Dockerfile is multi-stage and installs the built wheel into a slim runtime image.
- The image runs as a non-root user.
- `.dockerignore` excludes local caches, virtual environments, and build output from image context.
- The current workflows are designed to run on a self-hosted runner registered to this repository.
- Docker-related jobs require Docker to be installed on that runner.

## Self-Hosted Runner Notes

The runner setup page in GitHub provides the registration commands.

After the runner is registered and online:

1. New pushes and pull requests will start executing instead of remaining queued.
2. Existing queued runs may still need to be re-run from the Actions UI.
3. If the runner does not have Docker installed, Python quality gates will still run and Docker steps will be skipped.

## PR Checklist

Before opening a pull request:

1. Run `pytest -q`
2. Run `python -m build`
3. If Docker is available locally, run `docker build -f deployment/docker/Dockerfile .`
4. Push your branch and verify the GitHub Actions CI workflow is green