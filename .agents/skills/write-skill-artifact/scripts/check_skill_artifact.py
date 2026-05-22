#!/usr/bin/env python3
"""Lightweight structural checks for Codex skill SKILL.md files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TODO_PATTERN = re.compile(r"\bTODO\b|\[TODO:", re.IGNORECASE)
NAME_PATTERN = re.compile(r"^name:\s*([a-z0-9-]+)\s*$", re.MULTILINE)
DESCRIPTION_PATTERN = re.compile(r"^description:\s*(.+)\s*$", re.MULTILINE)
SECTION_PATTERN = re.compile(r"^##\s+", re.MULTILINE)


def frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["missing YAML frontmatter"]

    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return {}, text, ["invalid YAML frontmatter boundary"]

    raw = parts[1]
    body = parts[2]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, body, errors


def check_skill(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fields, body, errors = frontmatter(text)

    if path.name != "SKILL.md":
        errors.append("path must point to SKILL.md")
    if TODO_PATTERN.search(text):
        errors.append("contains TODO placeholder")
    if set(fields) - {"name", "description"}:
        errors.append("frontmatter must only contain name and description")
    if not NAME_PATTERN.search(text):
        errors.append("missing lowercase kebab-case name frontmatter")
    if "description" not in fields or not fields["description"]:
        errors.append("missing description frontmatter")
    elif not fields["description"].startswith("Use when"):
        errors.append("description should start with 'Use when'")

    if not re.search(r"^#\s+", body, re.MULTILINE):
        errors.append("missing top-level markdown title")
    for section in ("## 목적", "## 적용 대상", "## 책임", "## 작업 흐름", "## 검증"):
        if section not in body:
            errors.append(f"missing {section} section")
    if not SECTION_PATTERN.search(body):
        errors.append("missing markdown sections")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="SKILL.md files to validate")
    args = parser.parse_args()

    failed = False
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"FAIL {path}: file does not exist")
            failed = True
            continue
        errors = check_skill(path)
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
