#!/usr/bin/env python3
"""Validate agent workflow architecture and naming rules."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_AGENTS = {
    ".codex/agents/backend-delivery-engineer.toml": [
        "Backend Delivery Engineer",
        "backend-technical-design-writing-rules",
        "backend-code-implementation-rules",
        "backend-architecture-review-rules",
        "직접 수행",
        "아키텍처 리뷰 독립성",
        "아키텍처 리뷰 Source of Truth",
        "리뷰 재작업 루프",
        "violation bundle",
        "max review iterations",
    ],
    ".codex/agents/frontend-delivery-engineer.toml": [
        "Frontend Delivery Engineer",
        "frontend-technical-design-writing-rules",
        "frontend-code-implementation-rules",
        "frontend-architecture-review-rules",
        "직접 수행",
        "아키텍처 리뷰 독립성",
        "아키텍처 리뷰 Source of Truth",
        "리뷰 재작업 루프",
        "violation bundle",
        "max review iterations",
    ],
}


REQUIRED_ROLE_AGENTS = [
    ".codex/agents/product-planning-designer.toml",
    ".codex/agents/api-contract-designer.toml",
]


REQUIRED_SKILLS = {
    ".agents/skills/feature-delivery-orchestration-rules/SKILL.md": [
        "목적",
        "적용 대상",
        "작업 흐름",
        "Readiness 판단",
        "Dispatch 루프",
        "orchestration_result",
        "backend-delivery-engineer",
        "frontend-delivery-engineer",
        "dispatch_requests",
        "stable_for_parallel",
        "security_sensitive_blocker",
        "cross_cutting_risks",
    ],
    ".agents/skills/backend-technical-design-writing-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/backend-code-implementation-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "리뷰 재작업 입력",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/backend-architecture-review-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "Violation payload",
        "기본 Source of Truth 후보",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/frontend-technical-design-writing-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/frontend-code-implementation-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "리뷰 재작업 입력",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/frontend-architecture-review-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "Violation payload",
        "기본 Source of Truth 후보",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/product-requirements-planning-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "안티패턴",
        "금지사항",
    ],
    ".agents/skills/api-contract-design-rules/SKILL.md": [
        "목표",
        "성공 기준",
        "핵심 규칙",
        "안티패턴",
        "금지사항",
    ],
}


REQUIRED_SKILL_CONFIGS = {
    ".codex/agents/backend-delivery-engineer.toml": [
        "backend-technical-design-writing-rules/SKILL.md",
        "backend-code-implementation-rules/SKILL.md",
        "backend-architecture-review-rules/SKILL.md",
    ],
    ".codex/agents/frontend-delivery-engineer.toml": [
        "frontend-technical-design-writing-rules/SKILL.md",
        "frontend-code-implementation-rules/SKILL.md",
        "frontend-architecture-review-rules/SKILL.md",
    ],
    ".codex/agents/product-planning-designer.toml": [
        "product-requirements-planning-rules/SKILL.md",
    ],
    ".codex/agents/api-contract-designer.toml": [
        "api-contract-design-rules/SKILL.md",
    ],
}


REMOVED_COMPONENTS = [
    ".codex/agents/feature-delivery-lead.toml",
    ".codex/agents/backend-delivery-lead.toml",
    ".codex/agents/frontend-delivery-lead.toml",
    "docs/review/README.md",
    ".agents/skills/feature-delivery-readiness-rules/SKILL.md",
    ".codex/agents/backend-technical-design-writer.toml",
    ".codex/agents/backend-implementation-engineer.toml",
    ".codex/agents/backend-architecture-reviewer.toml",
    ".codex/agents/frontend-technical-design-writer.toml",
    ".codex/agents/frontend-implementation-engineer.toml",
    ".codex/agents/frontend-architecture-reviewer.toml",
    ".codex/agents/implementation-orchestrator.toml",
    ".codex/agents/infra-implementation-engineer.toml",
    ".codex/agents/fullstack-implementation-orchestrator.toml",
    ".codex/agents/backend-implementation-orchestrator.toml",
    ".codex/agents/frontend-implementation-orchestrator.toml",
    ".codex/agents/backend-engineering-lead.toml",
    ".codex/agents/backend-software-engineer.toml",
    ".codex/agents/frontend-engineering-lead.toml",
    ".codex/agents/frontend-software-engineer.toml",
    ".codex/agents/documentation-governance-reviewer.toml",
    ".codex/agents/security-policy-reviewer.toml",
    ".agents/skills/implement/SKILL.md",
    ".agents/skills/implement-backend/SKILL.md",
    ".agents/skills/implement-frontend/SKILL.md",
    ".agents/skills/fullstack-contract-coordination-rules/SKILL.md",
    ".agents/skills/plan-implementation-requirements/SKILL.md",
    ".agents/skills/write-api-spec/SKILL.md",
    ".agents/skills/write-backend-tech-design-doc/SKILL.md",
    ".agents/skills/write-frontend-tech-design-doc/SKILL.md",
    ".agents/skills/product-requirements-planning-rules/references/product-requirements-artifact-contract.md",
    ".agents/skills/api-contract-design-rules/references/api-contract-artifact-contract.md",
]


FORBIDDEN_SKILL_PHRASES = [
    "subagent lifecycle",
    "서브에이전트 lifecycle",
    "오케스트레이션 스킬",
    "workflow orchestration을 수행",
    "다른 skill을 실행",
    "다른 Skill을 실행",
]


FORBIDDEN_SKILL_REFERENCE_PHRASES = [
    "artifact contract",
    "artifact-contract",
    "실행 checkpoint",
    "체크포인트 파일",
    "CONTEXT_CHECKPOINT",
]


FORBIDDEN_DOMAIN_DOC_PHRASES = [
    ".agents/skills",
    ".codex/agents",
    "subagent://",
]


def read(relative: str) -> str | None:
    path = ROOT / relative
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def require_file(errors: list[str], relative: str) -> str | None:
    text = read(relative)
    if text is None:
        errors.append(f"{relative}: missing file")
    elif not text.strip():
        errors.append(f"{relative}: empty file")
    return text


def require_markers(errors: list[str], relative: str, markers: list[str]) -> None:
    text = require_file(errors, relative)
    if text is None:
        return
    for marker in markers:
        if marker not in text:
            errors.append(f"{relative}: missing marker {marker!r}")


def forbid_file(errors: list[str], relative: str) -> None:
    if (ROOT / relative).exists():
        errors.append(f"{relative}: removed component still exists")


def check_agents(errors: list[str]) -> None:
    for relative, markers in REQUIRED_AGENTS.items():
        require_markers(errors, relative, markers)
    for relative in REQUIRED_ROLE_AGENTS:
        require_file(errors, relative)
    for relative, skill_paths in REQUIRED_SKILL_CONFIGS.items():
        text = require_file(errors, relative)
        if text is None:
            continue
        for skill_path in skill_paths:
            if skill_path not in text:
                errors.append(f"{relative}: missing skills.config for {skill_path!r}")
        if "[[skills.config]]" not in text:
            errors.append(f"{relative}: missing [[skills.config]] block")
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped.startswith("path = "):
                continue
            raw_path = stripped.split("=", 1)[1].strip().strip('"')
            if ".agents/skills/" not in raw_path:
                continue
            if raw_path.startswith("/"):
                errors.append(f"{relative}: skills.config path must be repo-relative {raw_path!r}")
                continue
            skill_path = ROOT / raw_path
            resolved = skill_path.resolve()
            if ROOT not in resolved.parents:
                errors.append(f"{relative}: skills.config path escapes repository {raw_path!r}")
                continue
            if not resolved.exists():
                errors.append(f"{relative}: skills.config path does not exist {raw_path!r}")


def check_skills(errors: list[str]) -> None:
    for relative, markers in REQUIRED_SKILLS.items():
        require_markers(errors, relative, markers)
        text = read(relative) or ""
        for phrase in FORBIDDEN_SKILL_PHRASES:
            if phrase in text and "금지사항" not in text:
                errors.append(f"{relative}: forbidden orchestration phrase {phrase!r}")
        for phrase in FORBIDDEN_SKILL_REFERENCE_PHRASES:
            if phrase in text:
                errors.append(f"{relative}: forbidden execution contract phrase {phrase!r}")


def check_removed_components(errors: list[str]) -> None:
    for relative in REMOVED_COMPONENTS:
        forbid_file(errors, relative)


def check_docs(errors: list[str]) -> None:
    require_markers(
        errors,
        "AGENTS.md",
        ["Superpowers working artifacts"],
    )
    for path in [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / "docs/superpowers/README.md"]:
        text = path.read_text(encoding="utf-8")
        if "docs/review/README.md" in text or "Review routing" in text:
            errors.append(f"{path.relative_to(ROOT)}: central review routing doc reference remains")
    for root in ["docs/backend", "docs/frontend"]:
        for path in (ROOT / root).rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for phrase in FORBIDDEN_DOMAIN_DOC_PHRASES:
                if phrase in text:
                    errors.append(
                        f"{path.relative_to(ROOT)}: domain docs must not depend on runtime component {phrase!r}"
                    )


def main() -> int:
    errors: list[str] = []
    check_agents(errors)
    check_skills(errors)
    check_removed_components(errors)
    check_docs(errors)

    if errors:
        print("FAIL agent workflow architecture validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS agent workflow architecture validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
