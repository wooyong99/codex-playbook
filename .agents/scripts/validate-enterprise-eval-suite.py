#!/usr/bin/env python3
"""Validate enterprise-scale agent collaboration evaluation coverage."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_EVAL_DOC = ROOT / "docs/evals/enterprise-agent-collaboration.md"

REQUIRED_EVAL_MARKERS = [
    "setup-project-context",
    "reverse-engineer-backend-docs inspect",
    "10만~100만",
    "feature-delivery-lead",
    "backend-delivery-lead",
    "frontend-delivery-lead",
    "backend-implementation-engineer",
    "frontend-implementation-engineer",
    "backend-architecture-reviewer",
    "frontend-architecture-reviewer",
    "security-policy-reviewer",
    "모호",
    "conflicting request",
    "Jira-style",
    "Slack-style",
    "구현 검증 evidence",
    "architecture review 판정",
    "census",
    "sampling",
    "confidence",
]

AGENT_MARKERS = {
    ".codex/agents/feature-delivery-lead.toml": [
        "backend-delivery-lead",
        "frontend-delivery-lead",
        "product-planning-designer",
        "api-contract-designer",
    ],
    ".codex/agents/backend-delivery-lead.toml": [
        "backend-implementation-engineer",
        "backend-architecture-reviewer",
        "구현 검증 evidence",
        "architecture review 판정",
    ],
    ".codex/agents/frontend-delivery-lead.toml": [
        "frontend-implementation-engineer",
        "frontend-architecture-reviewer",
        "구현 검증 evidence",
        "architecture review 판정",
    ],
    ".codex/agents/backend-implementation-engineer.toml": [
        "독립적으로 실행 가능한 역할 subagent",
        "구현 검증 evidence",
        "architecture pass/violation 판정",
    ],
    ".codex/agents/frontend-implementation-engineer.toml": [
        "독립적으로 실행 가능한 역할 subagent",
        "구현 검증 evidence",
        "architecture pass/violation 판정",
    ],
    ".codex/agents/backend-technical-design-writer.toml": [
        "독립적으로 실행 가능한 역할 subagent",
    ],
    ".codex/agents/frontend-technical-design-writer.toml": [
        "독립적으로 실행 가능한 역할 subagent",
    ],
    ".codex/agents/backend-architecture-reviewer.toml": [
        "독립적으로 실행 가능한 역할 subagent",
    ],
    ".codex/agents/frontend-architecture-reviewer.toml": [
        "독립적으로 실행 가능한 역할 subagent",
    ],
}

SKILL_MARKERS = {
    ".agents/skills/setup-project-context/SKILL.md": [
        "사용자에게 필수 프로젝트 사실을 질문",
        "임의 생성",
    ],
    ".agents/skills/reverse-engineer-backend-docs/SKILL.md": [
        "inspect",
        "대형 저장소",
        "샘플링",
        "confidence",
    ],
    ".agents/skills/backend-code-implementation-rules/SKILL.md": [
        "구현 검증 evidence",
        "architecture review나 security review를 구현 검증 evidence로 대체하지 않는다",
    ],
    ".agents/skills/frontend-code-implementation-rules/SKILL.md": [
        "구현 검증 evidence",
        "architecture review나 security review를 구현 검증 evidence로 대체하지 않는다",
    ],
}

FORBIDDEN_ACTIVE_NAMES = [
    "backend-engineering-lead",
    "backend-software-engineer",
    "frontend-engineering-lead",
    "frontend-software-engineer",
]


def read(relative: str) -> str | None:
    path = ROOT / relative
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def require_markers(errors: list[str], relative: str, markers: list[str]) -> None:
    text = read(relative)
    if text is None:
        errors.append(f"{relative}: missing file")
        return
    for marker in markers:
        if marker not in text:
            errors.append(f"{relative}: missing marker {marker!r}")


def check_eval_doc(errors: list[str]) -> None:
    if not REQUIRED_EVAL_DOC.exists():
        errors.append(f"{REQUIRED_EVAL_DOC.relative_to(ROOT)}: missing file")
        return
    text = REQUIRED_EVAL_DOC.read_text(encoding="utf-8")
    for marker in REQUIRED_EVAL_MARKERS:
        if marker not in text:
            errors.append(
                f"{REQUIRED_EVAL_DOC.relative_to(ROOT)}: missing marker {marker!r}"
            )

    case_count = sum(1 for line in text.splitlines() if line.startswith("| EAC-"))
    if case_count < 10:
        errors.append(
            f"{REQUIRED_EVAL_DOC.relative_to(ROOT)}: expected at least 10 EAC cases, found {case_count}"
        )


def check_active_references(errors: list[str]) -> None:
    paths = [
        ROOT / "docs/evals/enterprise-agent-collaboration.md",
        ROOT / "docs/evals/scenarios.md",
        ROOT / "docs/customization-checklist.md",
        ROOT / "docs/superpowers/specs/2026-05-21-agent-oriented-implementation-architecture-design.md",
        ROOT / "docs/superpowers/plans/2026-05-21-agent-oriented-implementation-architecture.md",
        ROOT / ".codex/agents/feature-delivery-lead.toml",
    ]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for name in FORBIDDEN_ACTIVE_NAMES:
            if name in text:
                errors.append(f"{path.relative_to(ROOT)}: forbidden old name {name!r}")


def main() -> int:
    errors: list[str] = []
    check_eval_doc(errors)
    for relative, markers in AGENT_MARKERS.items():
        require_markers(errors, relative, markers)
    for relative, markers in SKILL_MARKERS.items():
        require_markers(errors, relative, markers)
    check_active_references(errors)

    if errors:
        print("FAIL enterprise eval suite validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS enterprise eval suite validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
