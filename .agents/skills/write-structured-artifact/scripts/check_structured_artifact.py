#!/usr/bin/env python3
"""Lightweight structural checks for docs, skills, and subagent TOML files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HIGH_LEVEL_TERMS = (
    "목적",
    "적용 범위",
    "범위",
    "책임",
    "역할",
    "소유",
    "전체 흐름",
    "문서 계층",
    "운영 모델",
    "개요",
    "Overview",
    "Purpose",
    "Scope",
    "Responsibilities",
)

LOW_LEVEL_TERMS = (
    "schema",
    "Schema",
    "YAML",
    "JSON",
    "파일명",
    "코드 스타일",
    "구현 절차",
    "명령어",
    "체크포인트 템플릿",
)

TODO_PATTERN = re.compile(r"\bTODO\b|\[TODO:", re.IGNORECASE)


def markdown_body(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("---\n", 2)
    if len(parts) == 3:
        return parts[2]
    return text


def line_number(text: str, needle: str) -> int | None:
    for index, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return index
    return None


def first_term_line(text: str, terms: tuple[str, ...]) -> int | None:
    matches = [line_number(text, term) for term in terms]
    found = [match for match in matches if match is not None]
    return min(found) if found else None


def check_markdown(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    body = markdown_body(text)
    if not re.search(r"^#\s+", body, re.MULTILINE):
        errors.append("missing top-level markdown title")

    high = first_term_line(body, HIGH_LEVEL_TERMS)
    low = first_term_line(body, LOW_LEVEL_TERMS)
    if high is None:
        errors.append("missing high-level section such as 목적/범위/책임/전체 흐름")
    if high is not None and low is not None and low < high:
        errors.append("low-level details appear before high-level structure")

    if path.name == "SKILL.md":
        if not text.startswith("---\n"):
            errors.append("SKILL.md missing YAML frontmatter")
        if "description:" not in text:
            errors.append("SKILL.md missing description frontmatter")
        if "## 검증" not in text and "## Validation" not in text:
            errors.append("SKILL.md missing validation section")

    return errors


def check_toml(text: str) -> list[str]:
    errors: list[str] = []
    required = ("name =", "description =", "developer_instructions")
    for token in required:
        if token not in text:
            errors.append(f"missing {token}")

    if "정체성:" not in text:
        errors.append("missing 정체성 section")
    if "철학:" not in text and "판단 철학:" not in text and "구현 철학:" not in text:
        errors.append("missing philosophy section")
    if "경계:" not in text and "작업 경계:" not in text and "검토 경계:" not in text:
        errors.append("missing boundary section")
    if "금지 규칙:" not in text:
        errors.append("missing prohibition rules section")
    return errors


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if TODO_PATTERN.search(text):
        errors.append("contains TODO placeholder")

    if path.suffix == ".md":
        errors.extend(check_markdown(path, text))
    elif path.suffix == ".toml":
        errors.extend(check_toml(text))
    else:
        errors.append("unsupported file type")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Markdown, SKILL.md, or subagent TOML files")
    args = parser.parse_args()

    failed = False
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"FAIL {path}: file does not exist")
            failed = True
            continue
        errors = check_file(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"- {error}")
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
