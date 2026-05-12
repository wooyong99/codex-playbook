#!/usr/bin/env python3
"""Validate implement skill context-checkpoint contracts.

This script intentionally uses only Python 3.9 standard-library features.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[4]

AGENTS = {
    "technical-design-writer": {
        "agent": ROOT / ".codex/agents/technical-design-writer.toml",
        "contract": ROOT / ".agents/skills/implement/references/technical-design-writer-contract.md",
        "title": "# Technical Design Writer Checkpoint",
        "sections": [
            "## 체크포인트 사유",
            "## 현재 목표",
            "## 핵심 규칙",
            "## 금지 규칙",
            "## 안티패턴",
            "## 완료된 작업",
            "## 진행중 작업",
            "## 남은 작업",
            "## 주의사항",
            "## 실패 패턴",
            "## 최근 결정",
            "## 진행 상태",
        ],
    },
    "implementation-engineer": {
        "agent": ROOT / ".codex/agents/implementation-engineer.toml",
        "contract": ROOT / ".agents/skills/implement/references/implementation-engineer-contract.md",
        "title": "# Implementation Engineer Checkpoint",
        "sections": [
            "## 체크포인트 사유",
            "## 현재 목표",
            "## 핵심 규칙",
            "## 금지 규칙",
            "## 안티패턴",
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
    "backend-architecture-reviewer": {
        "agent": ROOT / ".codex/agents/backend-architecture-reviewer.toml",
        "contract": ROOT / ".agents/skills/implement/references/backend-architecture-reviewer-contract.md",
        "title": "# Backend Architecture Reviewer Checkpoint",
        "sections": [
            "## 체크포인트 사유",
            "## 현재 목표",
            "## 핵심 규칙",
            "## 금지 규칙",
            "## 안티패턴",
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
    boundaries_path = ROOT / ".agents/skills/implement/references/orchestration-boundaries.md"
    planning_path = ROOT / ".agents/skills/implement/references/milestone-planning.md"
    protocol_path = ROOT / ".agents/skills/implement/references/handoff-checkpoint-protocol.md"
    workflow_path = ROOT / ".agents/skills/implement/references/milestone-execution-workflow.md"

    implement = read(implement_path)
    for needle, reason in [
        ("## 역할", "top-level role section"),
        ("## 기본 범위", "top-level scope section"),
        ("## 참조 문서", "top-level reference section"),
        ("## 프로세스", "top-level process section"),
        ("references/orchestration-boundaries.md", "orchestration boundary reference"),
        ("references/milestone-planning.md", "milestone planning reference"),
        ("references/handoff-checkpoint-protocol.md", "handoff checkpoint protocol reference"),
        ("references/milestone-execution-workflow.md", "milestone execution workflow reference"),
    ]:
        require(errors, implement_path, implement, needle, reason)

    for path, expected in [
        (
            planning_path,
            [
                ("## 마일스톤 분할 기준", "milestone split criteria"),
                ("명시적 제외사항", "explicit exclusions planning"),
                ("예상 변경 파일 3~8개 권장", "recommended changed file range"),
            ],
        ),
        (
            protocol_path,
            [
                ("## Handoff Artifact 공통 처리", "common handoff handling"),
                ("## 체크포인트 공통 처리", "common checkpoint handling"),
                ("역할별 체크포인트 판단 기준은 D/A/B 계약 문서가 단일 출처로 가진다", "contract-owned checkpoint criteria"),
                ("존재하고 비어 있지 않은지 확인한다", "checkpoint existence validation"),
                ("정상 완료 경로에서도 이번 호출의 `[체크포인트 파일]`", "orchestrator normal-result checkpoint validation"),
                ("python3 .agents/skills/implement/scripts/validate-context-checkpoints.py", "validation command"),
            ],
        ),
        (
            boundaries_path,
            [
                ("체크포인트 복구를 위해", "orchestrator read exception"),
                ("정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다", "normal-completion checkpoint guarantee"),
                ("D/A/B는 서로 호출하지 않는다", "subagent communication boundary"),
            ],
        ),
        (
            workflow_path,
            [
                ("## Step 2. Agent D 위임", "D workflow step"),
                ("## Step 3. Agent A 위임", "A workflow step"),
                ("## Step 4. Agent B 위임", "B workflow step"),
                ("## Escalation", "escalation workflow"),
            ],
        ),
    ]:
        text = read(path)
        for needle, reason in expected:
            require(errors, path, text, needle, reason)

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

    all_paths = [implement_path, boundaries_path, planning_path, protocol_path, workflow_path]
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

        require(errors, spec["contract"], contract, spec["title"], f"{name} checkpoint title")
        require(errors, spec["contract"], contract, "CONTEXT_CHECKPOINT:", f"{name} checkpoint signal")
        require(errors, spec["contract"], contract, "역할별 체크포인트 기준", f"{name} role checkpoint criteria")
        require(errors, spec["contract"], contract, "단일 출처", f"{name} contract single source")
        require(
            errors,
            spec["contract"],
            contract,
            "신호만 반환하고 파일을 남기지 않는 것은 실패",
            f"{name} save-before-signal guard",
        )
        require(
            errors,
            spec["contract"],
            contract,
            "정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다",
            f"{name} normal completion checkpoint requirement",
        )
        require(
            errors,
            spec["contract"],
            contract,
            "normal_completion",
            f"{name} normal completion checkpoint reason",
        )
        require(
            errors,
            spec["contract"],
            contract,
            "{normal_completion |",
            f"{name} normal completion checkpoint reason in template",
        )
        require(
            errors,
            spec["contract"],
            contract,
            "완료 snapshot",
            f"{name} normal completion checkpoint snapshot",
        )
        require(
            errors,
            spec["contract"],
            contract,
            "`CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다",
            f"{name} normal completion must not use checkpoint signal",
        )
        for section in spec["sections"]:
            require(errors, spec["contract"], contract, section, f"{name} checkpoint section")

        require(
            errors,
            spec["agent"],
            agent,
            "계약 문서 단일 출처",
            f"{name} agent single source reference",
        )
        require(errors, spec["agent"], agent, "CONTEXT_CHECKPOINT:", f"{name} checkpoint signal")
        require(errors, spec["agent"], agent, "역할별 체크포인트 기준", f"{name} role checkpoint criteria reference")
        require(
            errors,
            spec["agent"],
            agent,
            "체크포인트 파일 템플릿을 재정의하지 않는다",
            f"{name} agent must not redefine checkpoint template",
        )
        require(
            errors,
            spec["agent"],
            agent,
            "신호만 반환하고 파일을 남기지 않는 것은 실패",
            f"{name} save-before-signal guard reference",
        )
        require(
            errors,
            spec["agent"],
            agent,
            "정상 완료 시 [체크포인트 파일]",
            f"{name} normal completion checkpoint agent instruction",
        )
        require(
            errors,
            spec["agent"],
            agent,
            "[결과 파일]과 [체크포인트 파일]이 실제로 저장되기 전에는 정상 완료 신호",
            f"{name} normal completion waits for checkpoint file",
        )
        require(
            errors,
            spec["agent"],
            agent,
            "`CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다",
            f"{name} normal completion must not use checkpoint signal",
        )
        require(
            errors,
            spec["agent"],
            agent,
            "완료 snapshot",
            f"{name} normal completion snapshot agent instruction",
        )
        if agent is not None and spec["title"] in agent:
            errors.append(f"{spec['agent']}: checkpoint template title must live only in contract: {spec['title']}")
        if agent is not None and "체크포인트 파일은 아래 섹션을 포함한다" in agent:
            errors.append(f"{spec['agent']}: checkpoint file template text must live only in contract")
        if agent is not None and "```markdown" in agent:
            errors.append(f"{spec['agent']}: markdown checkpoint template block must live only in contract")

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

    for name in ["technical-design-writer", "implementation-engineer"]:
        spec = AGENTS[name]
        contract = read(spec["contract"])
        require(
            errors,
            spec["contract"],
            contract,
            "[명시적 제외사항]",
            f"{name} contract explicit exclusions field",
        )

    design_agent = read(AGENTS["technical-design-writer"]["agent"])
    require(
        errors,
        AGENTS["technical-design-writer"]["agent"],
        design_agent,
        ".agents/skills/write-tech-design-doc/SKILL.md",
        "technical-design-writer local write-tech-design-doc skill path",
    )
    design_skill_match = re.search(r'path\s*=\s*"([^"]*\.agents/skills/write-tech-design-doc/SKILL\.md)"', design_agent or "")
    if design_skill_match is None:
        errors.append(f"{AGENTS['technical-design-writer']['agent']}: missing parseable write-tech-design-doc skill path")
    else:
        design_skill_path = Path(design_skill_match.group(1))
        if design_skill_path.is_absolute():
            errors.append(f"{AGENTS['technical-design-writer']['agent']}: write-tech-design-doc skill path must be relative")
        if not design_skill_path.is_absolute():
            design_skill_path = ROOT / design_skill_path
        if not design_skill_path.exists():
            errors.append(f"{design_skill_path}: missing write-tech-design-doc skill")

    if errors:
        print("FAIL context checkpoint contract validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS context checkpoint contract validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
