#!/usr/bin/env python3
"""Validate codex-playbook repository consistency.

This script is intentionally dependency-free so it can run in local shells and CI.
It checks only repository hygiene and playbook contracts, not product code.
"""

from pathlib import Path
import re
import subprocess
import sys
import urllib.parse


ROOT = Path(__file__).resolve().parents[2]

CRITICAL_PLACEHOLDERS = {
    ROOT / "AGENTS.md": [
        "{프로젝트명}",
        "{비즈니스 목표 1}",
        "{비즈니스 목표 2}",
        "{비즈니스 목표 3}",
    ],
    ROOT / "docs/PRD.md": [
        "{프로젝트명}",
        "{PRD 한 줄 요약}",
        "{배경 및 해결하려는 문제}",
        "{비즈니스 목표 목록}",
        "{핵심 성과 지표(KPI) 목록}",
        "{이번 범위에서 제외하는 항목}",
        "{사용자 유형}",
        "{인터페이스명}",
        "{진입점}",
        "{기능별 요구사항 목록}",
        "{성능, 보안, 가용성 등 비기능 요구사항}",
        "{기술적·비즈니스적 제약}",
        "{주요 마일스톤 및 일정}",
    ],
    ROOT / "docs/backend/README.md": ["{프로젝트명}"],
    ROOT / "docs/frontend/README.md": ["{프로젝트명}"],
}

REQUIRED_GITIGNORE_ENTRIES = [
    ".idea/",
    ".agents/runs/",
    "node_modules/",
    "build/",
    "dist/",
]

REVIEWER_RULE_CONTRACTS = [
    (
        ROOT / ".agents/skills/implement-backend/references/backend-architecture-reviewer-contract.md",
        "Backend Rule ID 형식",
        re.compile(r"^BACKEND-[A-Z0-9]+-[A-Z0-9]+-\d{3}$"),
        "BACKEND-APP-DTO-001",
    ),
    (
        ROOT / ".agents/skills/implement-frontend/references/frontend-architecture-reviewer-contract.md",
        "Frontend Rule ID 형식",
        re.compile(r"^FRONTEND-[A-Z0-9]+-[A-Z0-9]+-\d{3}$"),
        "FRONTEND-FSD-IMPORT-001",
    ),
]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "app://",
    "notion://",
    "plugin://",
    "collection://",
)


def read_text(path):
    return path.read_text(encoding="utf-8")


def check_critical_placeholders(errors):
    for path, placeholders in CRITICAL_PLACEHOLDERS.items():
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing critical file")
            continue
        text = read_text(path)
        for placeholder in placeholders:
            if placeholder in text:
                errors.append(
                    f"{path.relative_to(ROOT)}: unresolved placeholder {placeholder}"
                )


def check_markdown_links(errors):
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", ".agents/runs"} for part in path.parts):
            continue
        in_code_fence = False
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            if line.strip().startswith("```"):
                in_code_fence = not in_code_fence
                continue
            if in_code_fence:
                continue
            for match in LINK_RE.finditer(line):
                raw_target = match.group(1).split("#", 1)[0].strip()
                if not raw_target:
                    continue
                if "{" in raw_target or "}" in raw_target:
                    continue
                if raw_target.startswith(EXTERNAL_PREFIXES):
                    continue
                target = urllib.parse.unquote(raw_target)
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: broken link {match.group(1)}"
                    )


def check_gitignore(errors):
    gitignore = ROOT / ".gitignore"
    if not gitignore.exists():
        errors.append(".gitignore: missing")
        return
    entries = {
        line.strip()
        for line in read_text(gitignore).splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    for required in REQUIRED_GITIGNORE_ENTRIES:
        if required not in entries:
            errors.append(f".gitignore: missing required entry {required}")


def check_reviewer_rule_contracts(errors):
    common_required = [
        "rule_id",
        "severity",
        "file",
        "rule",
        "source_path",
        "line_range",
        "reason",
        "UNREGISTERED",
        "`blocker`, `major`, `minor`, `info`",
    ]
    for path, section, rule_id_re, example in REVIEWER_RULE_CONTRACTS:
        rel_path = path.relative_to(ROOT)
        if not path.exists():
            errors.append(f"{rel_path}: missing reviewer rule contract")
            continue

        text = read_text(path)
        if section not in text:
            errors.append(f"{rel_path}: missing section {section}")
        for required in common_required:
            if required not in text:
                errors.append(f"{rel_path}: missing reviewer rule field {required}")
        if example not in text:
            errors.append(f"{rel_path}: missing rule_id example {example}")

        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith("- `") or not stripped.endswith("`"):
                continue
            value = stripped.strip("- `")
            if value.endswith("-001") and not rule_id_re.match(value):
                errors.append(f"{rel_path}:{line_number}: invalid rule_id example {value}")


def check_checkpoint_contract(errors):
    script = ROOT / ".agents/scripts/validate-context-checkpoints.py"
    if not script.exists():
        errors.append(f"{script.relative_to(ROOT)}: missing")
        return
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip()
        errors.append(
            "context checkpoint contract validation failed"
            + (f": {details}" if details else "")
        )


def main():
    errors = []
    check_critical_placeholders(errors)
    check_markdown_links(errors)
    check_gitignore(errors)
    check_reviewer_rule_contracts(errors)
    check_checkpoint_contract(errors)

    if errors:
        print("FAIL playbook validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS playbook validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
