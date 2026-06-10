from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass(slots=True)
class StaticAnalysisResult:
    tool: str
    status: str
    findings: int


class StaticAnalysisAdapter:
    """Executes static analysis tools (ruff, mypy, eslint) against the workspace."""

    TOOL_COMMANDS: dict[str, list[str]] = {
        "ruff": ["ruff", "check", "."],
        "mypy": ["mypy", "src"],
        "eslint": ["eslint", "."],
    }

    async def _run_command(self, command: list[str]) -> tuple[int, str]:
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout, _ = await proc.communicate()
        output = stdout.decode("utf-8", errors="replace") if stdout else ""
        return proc.returncode or 0, output

    @staticmethod
    def _estimate_findings(output: str) -> int:
        lines = [line for line in output.splitlines() if line.strip()]
        return max(0, len(lines))

    async def run(self, tools: list[str]) -> list[StaticAnalysisResult]:
        results: list[StaticAnalysisResult] = []
        for tool in tools:
            normalized = tool.lower()
            command = self.TOOL_COMMANDS.get(normalized)
            if not command:
                results.append(StaticAnalysisResult(tool=normalized, status="unknown_tool", findings=0))
                continue

            try:
                rc, output = await self._run_command(command)
                if rc == 0:
                    results.append(StaticAnalysisResult(tool=normalized, status="pass", findings=0))
                else:
                    results.append(
                        StaticAnalysisResult(
                            tool=normalized,
                            status="fail",
                            findings=self._estimate_findings(output),
                        )
                    )
            except FileNotFoundError:
                results.append(StaticAnalysisResult(tool=normalized, status="tool_missing", findings=0))
            except OSError:
                results.append(StaticAnalysisResult(tool=normalized, status="execution_error", findings=0))
        return results
