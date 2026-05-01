#!/usr/bin/env python3
"""Validate implement skill context-checkpoint contracts.

This script intentionally uses only Python 3.9 standard-library features.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]

AGENTS = {
    "design-writer": {
        "agent": ROOT / ".codex/agents/design-writer.toml",
        "contract": ROOT / ".agents/skills/implement/references/design-writer-contract.md",
        "title": "# Design Writer Checkpoint",
        "sections": [
            "## 체크포인트 사유",
            "## 현재 목표",
            "## 완료된 작업",
            "## 진행중 작업",
            "## 남은 작업",
            "## 주의사항",
            "## 실패 패턴",
            "## 최근 결정",
            "## 진행 상태",
        ],
    },
    "code-writer": {
        "agent": ROOT / ".codex/agents/code-writer.toml",
        "contract": ROOT / ".agents/skills/implement/references/code-writer-contract.md",
        "title": "# Code Writer Checkpoint",
        "sections": [
            "## 체크포인트 사유",
            "## 현재 목표",
            "## 완료된 작업",
            "## 진행중 작업",
            "## 남은 작업",
            "## 발견한 버그",
            "## 주의사항",
            "## 실패 패턴",
            "## 최근 결정",
            "## 검증 상태",
            "## 관련 파일",
            "## 진행 상태",
        ],
    },
    "architecture-reviewer": {
        "agent": ROOT / ".codex/agents/architecture-reviewer.toml",
        "contract": ROOT / ".agents/skills/implement/references/architecture-reviewer-contract.md",
        "title": "# Architecture Reviewer Checkpoint",
        "sections": [
            "## 체크포인트 사유",
            "## 현재 목표",
            "## 완료된 작업",
            "## 진행중 작업",
            "## 남은 작업",
            "## 발견한 버그",
            "## 주의사항",
            "## 실패 패턴",
            "## 최근 결정",
            "## 완료된 결과",
            "## 관련 파일",
            "## 진행 상태",
        ],
    },
}


def read(path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def require(errors, path, text, needle, reason):
    if text is None:
        errors.append(f"{path}: missing file")
    elif needle not in text:
        errors.append(f"{path}: missing {reason}: {needle}")


def main():
    errors = []

    implement_path = ROOT / ".agents/skills/implement/SKILL.md"
    implement = read(implement_path)
    for needle, reason in [
        ("### 체크포인트 공통 처리", "common checkpoint handling"),
        ("### 마일스톤 분할 기준", "milestone split criteria"),
        ("역할별 체크포인트 판단 기준은 D/A/B 계약 문서와 서브에이전트 정의가 가진다", "sub-agent-owned checkpoint criteria"),
        ("존재하고 비어 있지 않은지 확인한다", "checkpoint existence validation"),
        ("체크포인트 복구를 위해", "orchestrator read exception"),
    ]:
        require(errors, implement_path, implement, needle, reason)

    banned = [
        "65%",
        "[컨텍스트 체크포인트 테스트]",
        "force",
        "forced_test",
        "threshold",
        "compact",
        "/compact",
        "체크포인트 동작 검증",
        "테스트 모드",
        "### 체크포인트 기준",
        "공통 트리거",
        "D 전용 트리거",
        "A 전용 트리거",
        "B 전용 트리거",
        "[작업 단위 제한]",
        "[체크포인트 타이밍]",
        "[호출 범위]",
        "[체크포인트 기준]",
        "기본값과 호출별 조정값",
        "호출별 조정값",
        "scope_boundary",
        "범위 해석:",
        "처리 대상:",
        "제외 대상:",
    ]

    all_paths = [implement_path]
    all_paths.extend(spec["agent"] for spec in AGENTS.values())
    all_paths.extend(spec["contract"] for spec in AGENTS.values())

    for path in all_paths:
        text = read(path)
        if text is None:
            errors.append(f"{path}: missing file")
            continue
        for needle in banned:
            if needle in text:
                errors.append(f"{path}: banned final-contract text remains: {needle}")

    for name, spec in AGENTS.items():
        agent = read(spec["agent"])
        contract = read(spec["contract"])

        for path, text in [(spec["agent"], agent), (spec["contract"], contract)]:
            require(errors, path, text, spec["title"], f"{name} checkpoint title")
            require(errors, path, text, "CONTEXT_CHECKPOINT:", f"{name} checkpoint signal")
            require(errors, path, text, "역할별 체크포인트 기준", f"{name} role checkpoint criteria")
            require(
                errors,
                path,
                text,
                "신호만 반환하고 파일을 남기지 않는 것은 실패",
                f"{name} save-before-signal guard",
            )
            for section in spec["sections"]:
                require(errors, path, text, section, f"{name} checkpoint section")

        require(
            errors,
            spec["agent"],
            agent,
            "응답을 생략하지 않는다",
            f"{name} must respond to orchestrator",
        )
        require(
            errors,
            spec["agent"],
            agent,
            "현재 진행 상태",
            f"{name} agent must use progress state",
        )

        require(
            errors,
            spec["contract"],
            contract,
            "체크포인트 파일은 아래 섹션을 포함한다",
            f"{name} contract checkpoint schema",
        )
        require(
            errors,
            spec["contract"],
            contract,
            "정상 완료 포맷",
            f"{name} checkpoint output must not masquerade as completion",
        )

    for name in ["design-writer", "code-writer"]:
        spec = AGENTS[name]
        contract = read(spec["contract"])
        require(
            errors,
            spec["contract"],
            contract,
            "[명시적 제외사항]",
            f"{name} contract explicit exclusions field",
        )

    if errors:
        print("FAIL context checkpoint contract validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS context checkpoint contract validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
