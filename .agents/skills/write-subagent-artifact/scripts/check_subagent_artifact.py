#!/usr/bin/env python3
"""Lightweight structural checks for Codex subagent TOML files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TODO_PATTERN = re.compile(r"\bTODO\b|\[TODO:", re.IGNORECASE)
PAYLOAD_DETAIL_PATTERN = re.compile(r"응답에는 .+입력 규격")
FIXED_REFERENCE_PATTERN = re.compile(
    r"\.agents/skills/.+/references/|docs/backend/.+\.md|docs/frontend/.+\.md"
)


def check_toml(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if path.suffix != ".toml":
        errors.append("path must point to a .toml file")
    if TODO_PATTERN.search(text):
        errors.append("contains TODO placeholder")

    for token in ("name =", "description =", "developer_instructions"):
        if token not in text:
            errors.append(f"missing {token}")

    for section in (
        "정체성:",
        "책임:",
        "컨텍스트 원칙:",
        "판단 기준:",
        "입력·출력 원칙:",
        "완료 체크리스트:",
        "금지 규칙:",
    ):
        if section not in text:
            errors.append(f"missing {section} section")

    if "경계:" not in text and "작업 경계:" not in text and "검토 경계:" not in text:
        errors.append("missing boundary section")
    if PAYLOAD_DETAIL_PATTERN.search(text):
        errors.append("contains output payload details in subagent TOML")
    if FIXED_REFERENCE_PATTERN.search(text):
        errors.append("contains fixed Source of Truth or contract path")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="subagent TOML files to validate")
    args = parser.parse_args()

    failed = False
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"FAIL {path}: file does not exist")
            failed = True
            continue
        errors = check_toml(path)
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
