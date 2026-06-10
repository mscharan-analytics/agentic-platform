# How To Use

This document explains the practical ways to use this repository from install to deployment.

## 1. Install the Package

If you want to use the packaged CLI:

```bash
pip install enterprise-agent-platform
```

If you are working from source inside the repository:

```bash
pip install -e .[dev]
```

## 2. Choose How To Work

There are two main usage modes.

### Mode A: CLI package usage

Use this when you want to run the autonomous runner directly from the terminal.

```bash
agent-platform --goal "Implement feature X safely"
```

What happens:

1. The CLI entrypoint in `main.py` starts.
2. MCP tools are registered.
3. The default agent registry is built.
4. The autonomous runner executes the goal.
5. A JSON summary is printed.

### Mode B: IDE slash-agent usage

Use this when you are inside the repository in VS Code and want guided agent workflows.

Primary commands:

```text
/solver-agent
/worker-agent
```

Use `/solver-agent` when:

- the task is unclear
- you want planning or repo analysis
- you want the system to choose the path

Use `/worker-agent` when:

- the task is already clear
- you want code changes immediately
- you want focused execution and validation

## 3. Typical IDE Workflow

### Start with analysis

```text
/solver-agent Add deployment hardening for this repo
```

What it does:

1. Reads the repository.
2. Gathers only relevant files.
3. Applies context, token, and session controls internally.
4. Decides whether planning is needed.
5. Hands off to `worker-agent` only when execution is ready.

### Start with execution

```text
/worker-agent Add a CI workflow for tests, lint, build, and Docker validation
```

What it does:

1. Reads the relevant files.
2. Makes focused edits.
3. Runs validation.
4. Summarizes what changed and any remaining blockers.

## 4. Local Validation Commands

Before opening a PR, run:

```bash
pytest -q
python -m build
ruff check src tests
mypy src --ignore-missing-imports
```

If Docker is installed locally, also run:

```bash
docker build -f deployment/docker/Dockerfile .
```

## 5. Git and Pull Request Flow

Typical flow:

```bash
git switch -c feat/your-change
git add .
git commit -m "Describe the change"
git push -u origin feat/your-change
```

Then open a pull request.

What happens next:

1. CI runs on the configured self-hosted runner.
2. Tests, lint, typing, build, and optional Docker validation run.
3. If CI fails, fix the code and push again.
4. If CI passes, merge to `main`.

## 6. Release and Deployment Flow

After merge:

1. The release workflow can run on a version tag like `v0.1.0` or by manual dispatch.
2. The workflow builds the Python package.
3. The workflow builds the Docker image.
4. If secrets are configured, it publishes artifacts.
5. Deployment adapters can trigger GitHub Actions, Azure DevOps, or Jenkins.

## 7. What To Use First

Use this quick rule:

- Use the CLI when you want one-shot autonomous execution from terminal.
- Use `/solver-agent` when you need analysis or planning.
- Use `/worker-agent` when you already know the task and want implementation.

## 8. Important Notes

- `/solver-agent` and `/worker-agent` are IDE slash commands, not terminal commands.
- `agent-platform` is the terminal command exposed by the installed Python package.
- CI will not run unless a self-hosted runner is registered and online.
- Docker-related CI steps require Docker to be installed on that runner.