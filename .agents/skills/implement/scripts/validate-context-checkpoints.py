#!/usr/bin/env python3
"""Validate implement skill context-checkpoint contracts.

This script intentionally uses only Python 3.9 standard-library features.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]

AGENTS = {
    "backend-technical-design-writer": {
        "agent": ROOT / ".codex/agents/backend-technical-design-writer.toml",
        "contract": ROOT / ".agents/skills/implement-backend/references/backend-technical-design-writer-contract.md",
        "title": "# Backend Technical Design Writer Checkpoint",
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
    "frontend-technical-design-writer": {
        "agent": ROOT / ".codex/agents/frontend-technical-design-writer.toml",
        "contract": ROOT / ".agents/skills/implement-frontend/references/frontend-technical-design-writer-contract.md",
        "title": "# Frontend Technical Design Writer Checkpoint",
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
    "backend-implementation-engineer": {
        "agent": ROOT / ".codex/agents/backend-implementation-engineer.toml",
        "contract": ROOT / ".agents/skills/implement-backend/references/backend-implementation-engineer-contract.md",
        "title": "# Backend Implementation Engineer Checkpoint",
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
    "frontend-implementation-engineer": {
        "agent": ROOT / ".codex/agents/frontend-implementation-engineer.toml",
        "contract": ROOT / ".agents/skills/implement-frontend/references/frontend-implementation-engineer-contract.md",
        "title": "# Frontend Implementation Engineer Checkpoint",
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
        "contract": ROOT / ".agents/skills/implement-backend/references/backend-architecture-reviewer-contract.md",
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
    "frontend-architecture-reviewer": {
        "agent": ROOT / ".codex/agents/frontend-architecture-reviewer.toml",
        "contract": ROOT / ".agents/skills/implement-frontend/references/frontend-architecture-reviewer-contract.md",
        "title": "# Frontend Architecture Reviewer Checkpoint",
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
    backend_skill_path = ROOT / ".agents/skills/implement-backend/SKILL.md"
    frontend_skill_path = ROOT / ".agents/skills/implement-frontend/SKILL.md"
    boundaries_path = ROOT / ".agents/skills/implement/references/orchestration-boundaries.md"
    planning_path = ROOT / ".agents/skills/implement/references/milestone-planning.md"
    protocol_path = ROOT / ".agents/skills/implement/references/handoff-checkpoint-protocol.md"
    workflow_path = ROOT / ".agents/skills/implement/references/milestone-execution-workflow.md"

    implement = read(implement_path)
    for needle, reason in [
        ("## 역할", "top-level role section"),
        ("## 기본 범위", "top-level scope section"),
        ("## 참조 문서", "top-level reference section"),
        ("## 라우팅 기준", "router classification section"),
        ("## 프로세스", "top-level process section"),
        ("implement-backend", "backend execution skill reference"),
        ("implement-frontend", "frontend execution skill reference"),
        ("references/orchestration-boundaries.md", "orchestration boundary reference"),
        ("references/milestone-planning.md", "milestone planning reference"),
        ("references/handoff-checkpoint-protocol.md", "handoff checkpoint protocol reference"),
        ("references/milestone-execution-workflow.md", "milestone execution workflow reference"),
    ]:
        require(errors, implement_path, implement, needle, reason)

    backend_skill = read(backend_skill_path)
    for needle, reason in [
        ("name: implement-backend", "backend skill name"),
        ("backend-technical-design-writer", "backend design agent"),
        ("backend-implementation-engineer", "backend implementation agent"),
        ("backend-architecture-reviewer", "backend review agent"),
        ("../implement/references/handoff-checkpoint-protocol.md", "shared handoff reference"),
        ("references/backend-technical-design-writer-contract.md", "backend design contract"),
        ("references/backend-implementation-engineer-contract.md", "backend implementation contract"),
        ("references/backend-architecture-reviewer-contract.md", "backend reviewer contract"),
    ]:
        require(errors, backend_skill_path, backend_skill, needle, reason)

    frontend_skill = read(frontend_skill_path)
    for needle, reason in [
        ("name: implement-frontend", "frontend skill name"),
        ("frontend-technical-design-writer", "frontend design agent"),
        ("frontend-implementation-engineer", "frontend implementation agent"),
        ("frontend-architecture-reviewer", "frontend review agent"),
        ("../implement/references/handoff-checkpoint-protocol.md", "shared handoff reference"),
        ("references/frontend-technical-design-writer-contract.md", "frontend design contract"),
        ("references/frontend-implementation-engineer-contract.md", "frontend implementation contract"),
        ("references/frontend-architecture-reviewer-contract.md", "frontend reviewer contract"),
    ]:
        require(errors, frontend_skill_path, frontend_skill, needle, reason)

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
                ("구체 계약 경로는 `implement-backend` 또는 `implement-frontend` 실행 스킬", "area skill contract ownership"),
                ("`implement-backend`의 D 계약 Input 형식", "backend D workflow contract ownership"),
                ("`implement-frontend`의 D 계약 Input 형식", "frontend D workflow contract ownership"),
                ("자기 A 계약 문서", "area-owned A workflow contract"),
                ("## Step 3. Agent A 라우팅 및 위임", "A workflow step"),
                ("## Step 4. Agent B 라우팅 및 Reviewer 위임", "review workflow step"),
                ("`implement-backend`의 B 계약 Input 형식", "backend B workflow contract ownership"),
                ("`implement-frontend`의 B 계약 Input 형식", "frontend B workflow contract ownership"),
                ("[Source of Truth]", "B source-of-truth input responsibility"),
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

    all_paths = [
        implement_path,
        backend_skill_path,
        frontend_skill_path,
        boundaries_path,
        planning_path,
        protocol_path,
        workflow_path,
    ]
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

    for name in [
        "backend-technical-design-writer",
        "frontend-technical-design-writer",
        "backend-implementation-engineer",
        "frontend-implementation-engineer",
    ]:
        spec = AGENTS[name]
        contract = read(spec["contract"])
        require(
            errors,
            spec["contract"],
            contract,
            "[명시적 제외사항]",
            f"{name} contract explicit exclusions field",
        )

    source_expectations = [
        (
            "backend-technical-design-writer",
            [
                ("[Source of Truth]", "backend D source-of-truth input field"),
                ("docs/PRD.md", "backend D PRD source candidate"),
                ("docs/backend/README.md", "backend D README source candidate"),
                ("docs/backend/architecture/**", "backend D architecture source candidates"),
                ("docs/backend/policies/**", "backend D policy source candidates"),
                ("docs/backend/design/**", "backend D design source candidates"),
                ("특정 unit 이름은 이 계약에서 고정하지 않는다", "backend D architecture unit neutrality"),
            ],
        ),
        (
            "frontend-technical-design-writer",
            [
                ("[Source of Truth]", "frontend D source-of-truth input field"),
                ("docs/PRD.md", "frontend D PRD source candidate"),
                ("docs/frontend/README.md", "frontend D README source candidate"),
                ("docs/frontend/architecture/**", "frontend D architecture source candidates"),
                ("docs/frontend/conventions/**", "frontend D convention source candidates"),
                ("docs/frontend/performance/**", "frontend D performance source candidates"),
                ("docs/frontend/ui-ux/**", "frontend D UI/UX source candidates"),
                ("docs/frontend/design/**", "frontend D design source candidates"),
            ],
        ),
        (
            "backend-implementation-engineer",
            [
                ("[Source of Truth]", "backend implementation source-of-truth input field"),
                ("docs/backend/README.md", "backend A README source candidate"),
                ("docs/backend/architecture/**", "backend A architecture source candidates"),
                ("docs/backend/policies/**", "backend A policy source candidates"),
                ("payload.tdd_path", "backend implementation TDD source candidate"),
            ],
        ),
        (
            "frontend-implementation-engineer",
            [
                ("[Source of Truth]", "frontend implementation source-of-truth input field"),
                ("docs/frontend/README.md", "frontend A README source candidate"),
                ("docs/frontend/architecture/**", "frontend A architecture source candidates"),
                ("docs/frontend/conventions/**", "frontend A convention source candidates"),
                ("docs/frontend/performance/**", "frontend A performance source candidates"),
                ("docs/frontend/ui-ux/**", "frontend A UI/UX source candidates"),
                ("payload.tdd_path", "frontend implementation TDD source candidate"),
            ],
        ),
        (
            "frontend-architecture-reviewer",
            [
                ("[Source of Truth]", "frontend reviewer source-of-truth input field"),
                ("오케스트레이터가 입력한 `[Source of Truth]`", "frontend reviewer source-of-truth ownership"),
                ("docs/frontend/README.md", "frontend reviewer README source candidate"),
                ("docs/frontend/architecture/**", "frontend reviewer architecture source candidates"),
                ("docs/frontend/conventions/**", "frontend reviewer convention source candidates"),
                ("docs/frontend/performance/**", "frontend reviewer performance source candidates"),
                ("docs/frontend/ui-ux/**", "frontend reviewer UI/UX source candidates"),
                ("payload.tdd_path", "frontend reviewer TDD source candidate"),
            ],
        ),
    ]
    for name, expected in source_expectations:
        spec = AGENTS[name]
        contract = read(spec["contract"])
        for needle, reason in expected:
            require(errors, spec["contract"], contract, needle, reason)

    backend_review_spec = AGENTS["backend-architecture-reviewer"]
    backend_review_agent = read(backend_review_spec["agent"])
    backend_review_contract = read(backend_review_spec["contract"])
    require(
        errors,
        backend_review_spec["contract"],
        backend_review_contract,
        "[Source of Truth]",
        "backend reviewer source-of-truth input field",
    )
    require(
        errors,
        backend_review_spec["contract"],
        backend_review_contract,
        "오케스트레이터가 입력한 `[Source of Truth]`",
        "backend reviewer source-of-truth ownership",
    )
    for needle, reason in [
        ("docs/backend/README.md", "backend reviewer source-of-truth README candidate"),
        ("docs/backend/architecture/**", "backend reviewer architecture source candidates"),
        ("docs/backend/policies/**", "backend reviewer policy source candidates"),
        ("payload.tdd_path", "backend reviewer TDD source candidate"),
        ("특정 unit 이름은 이 계약에서 고정하지 않는다", "backend reviewer architecture unit neutrality"),
        ("변경 파일 경로·A 결과 요약·D 결과의 설계 결정", "backend reviewer source selection basis"),
    ]:
        require(errors, backend_review_spec["contract"], backend_review_contract, needle, reason)
    implement_coupling_banned = [
        ".agents/skills/implement/references",
        "backend-architecture-reviewer-contract.md",
        "frontend-architecture-reviewer-contract.md",
        "implementation-engineer-contract.md",
        "backend-implementation-engineer-contract.md",
        "frontend-implementation-engineer-contract.md",
        "backend-technical-design-writer-contract.md",
        "frontend-technical-design-writer-contract.md",
        "Context 절약 원칙",
        "Context Window Management",
        "계약 문서 단일 출처",
        "Handoff Artifact:",
        "CONTEXT_CHECKPOINT:",
        "[결과 파일]",
        "[체크포인트 파일]",
        "정상 완료 시",
        "Source of Truth:",
        "application/use case",
        "write-backend-tech-design-doc",
        "write-frontend-tech-design-doc",
        "docs/backend/",
        "docs/frontend/",
        "docs/review/",
        "docs/rules/",
    ]
    for path in sorted((ROOT / ".codex/agents").glob("*.toml")):
        agent_text = read(path)
        for needle in implement_coupling_banned:
            if agent_text is not None and needle in agent_text:
                errors.append(f"{path}: agent TOML should not embed implement-specific, skill-specific, or static source text: {needle}")

    if errors:
        print("FAIL context checkpoint contract validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS context checkpoint contract validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
