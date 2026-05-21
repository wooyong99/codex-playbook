#!/usr/bin/env python3
"""Validate project skills against skill-creator authoring guidance."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / ".agents/skills"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")
ROLE_COUPLING_RE = re.compile(
    r"(delivery-lead|delivery-engineer|implementation-engineer|technical-design-writer|"
    r"architecture-reviewer|software-engineer|product-planning-designer|"
    r"api-contract-designer)"
)
LEGACY_AGENT_NAMES = [
    "backend-engineering-lead",
    "backend-software-engineer",
    "frontend-engineering-lead",
    "frontend-software-engineer",
]
PLACEHOLDER_RE = re.compile(r"\bTODO\b|\[TODO:|<무엇을 하고 언제 쓰는지", re.IGNORECASE)


def strip_fenced_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return {}
    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def check_skill(errors: list[str], skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    relative_skill = skill_md.relative_to(ROOT)

    if not NAME_RE.match(name):
        errors.append(f"{relative_skill}: invalid skill name {name!r}")
    if name != skill_dir.name:
        errors.append(
            f"{relative_skill}: frontmatter name {name!r} does not match directory {skill_dir.name!r}"
        )
    if not description:
        errors.append(f"{relative_skill}: missing description")
    elif len(description) > 500:
        errors.append(f"{relative_skill}: description exceeds 500 characters")
    if ROLE_COUPLING_RE.search(description):
        errors.append(
            f"{relative_skill}: description must describe trigger conditions, not concrete subagent roles"
        )
    text_without_examples = strip_fenced_code_blocks(text)
    if PLACEHOLDER_RE.search(description) or PLACEHOLDER_RE.search(text_without_examples):
        errors.append(f"{relative_skill}: contains scaffold placeholder text")

    for legacy_name in LEGACY_AGENT_NAMES:
        if legacy_name in text:
            errors.append(f"{relative_skill}: contains legacy agent name {legacy_name!r}")

    for readme in skill_dir.rglob("README.md"):
        errors.append(
            f"{readme.relative_to(ROOT)}: skill resources should use purpose-specific names such as reference-map.md"
        )

    agents_yaml = skill_dir / "agents/openai.yaml"
    if agents_yaml.exists():
        yaml_text = agents_yaml.read_text(encoding="utf-8")
        for marker in ["display_name:", "short_description:", "default_prompt:"]:
            if marker not in yaml_text:
                errors.append(f"{agents_yaml.relative_to(ROOT)}: missing {marker}")
        for legacy_name in LEGACY_AGENT_NAMES:
            if legacy_name in yaml_text:
                errors.append(f"{agents_yaml.relative_to(ROOT)}: contains legacy agent name {legacy_name!r}")


def main() -> int:
    errors: list[str] = []
    if not SKILLS_DIR.exists():
        errors.append(".agents/skills: missing directory")
    else:
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir():
                check_skill(errors, skill_dir)

    if errors:
        print("FAIL skill authoring quality validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS skill authoring quality validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
