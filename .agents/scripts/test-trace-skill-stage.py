#!/usr/bin/env python3
"""Smoke tests for trace-skill-stage.py."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/scripts/trace-skill-stage.py"


def run_trace(*args: str, trace_dir: Path) -> str:
    env = os.environ.copy()
    env["CODEX_PLAYBOOK_TRACE_DIR"] = str(trace_dir)
    result = subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=True,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    return result.stdout


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        trace_dir = Path(directory)
        start = run_trace(
            "start",
            "--agent",
            "backend-delivery-engineer",
            "--skill",
            "backend-code-implementation-rules",
            "--input",
            "backend_design_basis,비밀번호=1234",
            "--new-run",
            trace_dir=trace_dir,
        )
        assert "1번째 호출 시작" in start
        assert "backend_design_basis" in start
        assert "비밀번호=1234" not in start
        assert "비표시" in start

        end = run_trace(
            "end",
            "--agent",
            "backend-delivery-engineer",
            "--skill",
            "backend-code-implementation-rules",
            "--output",
            "implementation_result",
            "--status",
            "완료",
            trace_dir=trace_dir,
        )
        assert "1번째 호출 종료" in end
        assert "implementation_result" in end

        second_start = run_trace(
            "start",
            "--agent",
            "backend-delivery-engineer",
            "--skill",
            "backend-code-implementation-rules",
            "--input",
            "remediation_input",
            trace_dir=trace_dir,
        )
        assert "2번째 호출 시작" in second_start

        summary = run_trace(
            "summary",
            "--agent",
            "backend-delivery-engineer",
            trace_dir=trace_dir,
        )
        assert "[스킬 요약]" in summary
        assert "backend-code-implementation-rules: 2회 호출" in summary

    print("PASS trace skill stage smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
