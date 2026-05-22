#!/usr/bin/env python3
"""Validate backend/frontend context-checkpoint contracts.

This script intentionally uses only Python 3.9 standard-library features.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]

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


def require_between(errors, path, text, start, needle, end, reason):
    if text is None:
        errors.append(f"{path}: missing file")
        return
    start_idx = text.find(start)
    needle_idx = text.find(needle)
    end_idx = text.find(end)
    if start_idx == -1 or needle_idx == -1 or end_idx == -1:
        errors.append(f"{path}: missing ordering marker for {reason}")
    elif not (start_idx < needle_idx < end_idx):
        errors.append(f"{path}: {reason} must appear between {start} and {end}")


def main():
    errors = []

    backend_skill_path = ROOT / ".agents/skills/implement-backend/SKILL.md"
    frontend_skill_path = ROOT / ".agents/skills/implement-frontend/SKILL.md"
    backend_boundaries_path = ROOT / ".agents/skills/implement-backend/references/orchestration-boundaries.md"
    backend_planning_path = ROOT / ".agents/skills/implement-backend/references/milestone-planning.md"
    backend_protocol_path = ROOT / ".agents/skills/implement-backend/references/input-output-checkpoint-protocol.md"
    backend_workflow_path = ROOT / ".agents/skills/implement-backend/references/milestone-execution-workflow.md"
    frontend_boundaries_path = ROOT / ".agents/skills/implement-frontend/references/orchestration-boundaries.md"
    frontend_planning_path = ROOT / ".agents/skills/implement-frontend/references/milestone-planning.md"
    frontend_protocol_path = ROOT / ".agents/skills/implement-frontend/references/input-output-checkpoint-protocol.md"
    frontend_workflow_path = ROOT / ".agents/skills/implement-frontend/references/milestone-execution-workflow.md"

    backend_skill = read(backend_skill_path)
    for needle, reason in [
        ("name: implement-backend", "backend skill name"),
        ("backend-technical-design-writer", "backend design agent"),
        ("backend-implementation-engineer", "backend implementation agent"),
        ("backend-architecture-reviewer", "backend review agent"),
        ("references/orchestration-boundaries.md", "backend boundary reference"),
        ("references/milestone-planning.md", "backend planning reference"),
        ("references/input-output-checkpoint-protocol.md", "backend input output reference"),
        ("references/milestone-execution-workflow.md", "backend workflow reference"),
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
        ("references/orchestration-boundaries.md", "frontend boundary reference"),
        ("references/milestone-planning.md", "frontend planning reference"),
        ("references/input-output-checkpoint-protocol.md", "frontend input output reference"),
        ("references/milestone-execution-workflow.md", "frontend workflow reference"),
        ("references/frontend-technical-design-writer-contract.md", "frontend design contract"),
        ("references/frontend-implementation-engineer-contract.md", "frontend implementation contract"),
        ("references/frontend-architecture-reviewer-contract.md", "frontend reviewer contract"),
    ]:
        require(errors, frontend_skill_path, frontend_skill, needle, reason)

    for path, expected in [
        (
            backend_planning_path,
            [
                ("# Backend Milestone Planning", "backend planning title"),
                ("## 마일스톤 분할 기준", "backend milestone split criteria"),
                ("트랜잭션 경계", "backend transaction split signal"),
                ("예상 변경 파일 3~8개 권장", "backend recommended changed file range"),
                ("frontend 전달 계약", "backend frontend contract metadata"),
            ],
        ),
        (
            backend_protocol_path,
            [
                ("# Backend Input Output And Checkpoint Protocol", "backend protocol title"),
                ("## Backend Input Artifact 처리", "backend input handling"),
                ("## Backend Output Artifact 처리", "backend output handling"),
                ("## 체크포인트 처리", "backend checkpoint handling"),
                ("Markdown input artifact", "backend markdown input artifact"),
                ("Markdown output artifact", "backend markdown output artifact"),
                ("├── inputs/", "backend input directory"),
                ("├── outputs/", "backend output directory"),
                ("역할별 체크포인트 판단 기준은 backend 계약 문서가 단일 출처", "backend contract-owned checkpoint criteria"),
                ("체크포인트 규격", "backend protocol passes checkpoint criteria input"),
            ],
        ),
        (
            backend_boundaries_path,
            [
                ("# Backend Orchestration Boundaries", "backend boundary title"),
                ("backend 역할 서브에이전트", "backend role boundary"),
                ("서브에이전트는 서로 호출하지 않는다", "backend subagent communication boundary"),
                ("정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다", "backend normal-completion checkpoint guarantee"),
            ],
        ),
        (
            backend_workflow_path,
            [
                ("# Backend Milestone Execution Workflow", "backend workflow title"),
                ("## Step 2. Backend Design Writer 위임", "backend design workflow step"),
                ("backend-technical-design-writer-contract.md", "backend D contract"),
                ("backend-implementation-engineer-contract.md", "backend A contract"),
                ("backend-architecture-reviewer-contract.md", "backend B contract"),
                ("[입력 파일]", "backend workflow input file"),
                ("[출력 파일]", "backend workflow output file"),
                ("체크포인트 규격", "backend workflow checkpoint criteria input"),
                ("## Escalation", "backend escalation workflow"),
            ],
        ),
        (
            frontend_planning_path,
            [
                ("# Frontend Milestone Planning", "frontend planning title"),
                ("## 마일스톤 분할 기준", "frontend milestone split criteria"),
                ("route/page", "frontend route split signal"),
                ("예상 변경 파일 3~8개 권장", "frontend recommended changed file range"),
                ("backend 계약", "frontend backend contract metadata"),
            ],
        ),
        (
            frontend_protocol_path,
            [
                ("# Frontend Input Output And Checkpoint Protocol", "frontend protocol title"),
                ("## Frontend Input Artifact 처리", "frontend input handling"),
                ("## Frontend Output Artifact 처리", "frontend output handling"),
                ("## 체크포인트 처리", "frontend checkpoint handling"),
                ("Markdown input artifact", "frontend markdown input artifact"),
                ("Markdown output artifact", "frontend markdown output artifact"),
                ("├── inputs/", "frontend input directory"),
                ("├── outputs/", "frontend output directory"),
                ("역할별 체크포인트 판단 기준은 frontend 계약 문서가 단일 출처", "frontend contract-owned checkpoint criteria"),
                ("체크포인트 규격", "frontend protocol passes checkpoint criteria input"),
            ],
        ),
        (
            frontend_boundaries_path,
            [
                ("# Frontend Orchestration Boundaries", "frontend boundary title"),
                ("frontend 역할 서브에이전트", "frontend role boundary"),
                ("서브에이전트는 서로 호출하지 않는다", "frontend subagent communication boundary"),
                ("정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다", "frontend normal-completion checkpoint guarantee"),
            ],
        ),
        (
            frontend_workflow_path,
            [
                ("# Frontend Milestone Execution Workflow", "frontend workflow title"),
                ("## Step 2. Frontend Design Writer 위임", "frontend design workflow step"),
                ("frontend-technical-design-writer-contract.md", "frontend D contract"),
                ("frontend-implementation-engineer-contract.md", "frontend A contract"),
                ("frontend-architecture-reviewer-contract.md", "frontend B contract"),
                ("[입력 파일]", "frontend workflow input file"),
                ("[출력 파일]", "frontend workflow output file"),
                ("체크포인트 규격", "frontend workflow checkpoint criteria input"),
                ("## Escalation", "frontend escalation workflow"),
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
        "Output > 역할별 체크포인트 기준",
        "handoffs",
        "Handoff Artifact",
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
        backend_skill_path,
        frontend_skill_path,
        backend_boundaries_path,
        backend_planning_path,
        backend_protocol_path,
        backend_workflow_path,
        frontend_boundaries_path,
        frontend_planning_path,
        frontend_protocol_path,
        frontend_workflow_path,
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
        is_markdown_case_contract = name.startswith(("backend-", "frontend-"))

        require(errors, spec["contract"], contract, spec["title"], f"{name} checkpoint title")
        require(errors, spec["contract"], contract, "CONTEXT_CHECKPOINT:", f"{name} checkpoint signal")
        require(errors, spec["contract"], contract, "[입력 파일]", f"{name} input artifact field")
        require(errors, spec["contract"], contract, "[출력 파일]", f"{name} output artifact field")
        require(errors, spec["contract"], contract, "/inputs/", f"{name} input directory path")
        require(errors, spec["contract"], contract, "/outputs/", f"{name} output directory path")
        if is_markdown_case_contract:
            require(errors, spec["contract"], contract, "Case", f"{name} case contract")
            require(errors, spec["contract"], contract, "Markdown", f"{name} markdown artifact contract")
            require(errors, spec["contract"], contract, "출력 규격", f"{name} output contract in input")
            require(errors, spec["contract"], contract, "체크포인트 규격", f"{name} checkpoint contract in input")
            require(errors, spec["contract"], contract, "Metadata.output_file", f"{name} output artifact path field")
            require(errors, spec["contract"], contract, "Metadata.checkpoint_file", f"{name} checkpoint artifact path field")
        else:
            require(errors, spec["contract"], contract, "역할별 체크포인트 기준", f"{name} role checkpoint criteria")
            require(errors, spec["contract"], contract, "artifacts.output_file", f"{name} output artifact path field")
            require(errors, spec["contract"], contract, "artifacts.checkpoint_file", f"{name} checkpoint artifact path field")
            require(errors, spec["contract"], contract, "[체크포인트 판단 기준]", f"{name} checkpoint criteria input field")
            require(errors, spec["contract"], contract, "Input > 역할별 체크포인트 기준", f"{name} checkpoint criteria source pointer")
            require_between(
                errors,
                spec["contract"],
                contract,
                "## Input",
                "### 역할별 체크포인트 기준",
                "## Output",
                f"{name} checkpoint criteria location",
            )
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
                ("Source of Truth", "backend design source-of-truth input section"),
                ("docs/PRD.md", "backend D PRD source candidate"),
                ("docs/backend/README.md", "backend D README source candidate"),
                ("docs/backend/architecture/**", "backend D architecture source candidates"),
                ("docs/backend/policies/**", "backend D policy source candidates"),
                ("docs/backend/design/**", "backend D design source candidates"),
                ("implement-backend-design-input/v1", "backend D input schema version"),
                ("implement-backend-design/v1", "backend D schema version"),
                ("특정 unit 이름은 이 계약에서 고정하지 않는다", "backend D architecture unit neutrality"),
            ],
        ),
        (
            "frontend-technical-design-writer",
            [
                ("Source of Truth", "frontend design source-of-truth input section"),
                ("docs/PRD.md", "frontend D PRD source candidate"),
                ("docs/frontend/README.md", "frontend D README source candidate"),
                ("docs/frontend/architecture/**", "frontend D architecture source candidates"),
                ("docs/frontend/conventions/**", "frontend D convention source candidates"),
                ("docs/frontend/performance/**", "frontend D performance source candidates"),
                ("docs/frontend/ui-ux/**", "frontend D UI/UX source candidates"),
                ("docs/frontend/design/**", "frontend D design source candidates"),
                ("implement-frontend-design-input/v1", "frontend D input schema version"),
                ("implement-frontend-design/v1", "frontend D schema version"),
            ],
        ),
        (
            "backend-implementation-engineer",
            [
                ("Source of Truth", "backend implementation source-of-truth input section"),
                ("docs/backend/README.md", "backend A README source candidate"),
                ("docs/backend/architecture/**", "backend A architecture source candidates"),
                ("docs/backend/policies/**", "backend A policy source candidates"),
                ("design result의 TDD 경로", "backend implementation TDD source candidate"),
                ("implement-backend-implementation-input/v1", "backend implementation input schema version"),
                ("implement-backend-fix-input/v1", "backend fix input schema version"),
                ("implement-backend-implementation/v1", "backend implementation schema version"),
            ],
        ),
        (
            "frontend-implementation-engineer",
            [
                ("Source of Truth", "frontend implementation source-of-truth input section"),
                ("docs/frontend/README.md", "frontend A README source candidate"),
                ("docs/frontend/architecture/**", "frontend A architecture source candidates"),
                ("docs/frontend/conventions/**", "frontend A convention source candidates"),
                ("docs/frontend/performance/**", "frontend A performance source candidates"),
                ("docs/frontend/ui-ux/**", "frontend A UI/UX source candidates"),
                ("design result의 TDD 경로", "frontend implementation TDD source candidate"),
                ("implement-frontend-implementation-input/v1", "frontend implementation input schema version"),
                ("implement-frontend-fix-input/v1", "frontend fix input schema version"),
                ("implement-frontend-implementation/v1", "frontend implementation schema version"),
            ],
        ),
        (
            "frontend-architecture-reviewer",
            [
                ("Source of Truth", "frontend reviewer source-of-truth input section"),
                ("검토 기준은 `[입력 파일]`의 `Source of Truth` 섹션으로 한정한다", "frontend reviewer source-of-truth ownership"),
                ("docs/frontend/README.md", "frontend reviewer README source candidate"),
                ("docs/frontend/architecture/**", "frontend reviewer architecture source candidates"),
                ("docs/frontend/conventions/**", "frontend reviewer convention source candidates"),
                ("docs/frontend/performance/**", "frontend reviewer performance source candidates"),
                ("docs/frontend/ui-ux/**", "frontend reviewer UI/UX source candidates"),
                ("design result의 TDD 경로", "frontend reviewer TDD source candidate"),
                ("implement-frontend-review-input/v1", "frontend reviewer input schema version"),
                ("implement-frontend-review/v1", "frontend reviewer schema version"),
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
        "Source of Truth",
        "backend reviewer source-of-truth input section",
    )
    require(
        errors,
        backend_review_spec["contract"],
        backend_review_contract,
        "검토 기준은 `[입력 파일]`의 `Source of Truth` 섹션으로 한정한다",
        "backend reviewer source-of-truth ownership",
    )
    for needle, reason in [
        ("docs/backend/README.md", "backend reviewer source-of-truth README candidate"),
        ("docs/backend/architecture/**", "backend reviewer architecture source candidates"),
        ("docs/backend/policies/**", "backend reviewer policy source candidates"),
        ("design result의 TDD 경로", "backend reviewer TDD source candidate"),
        ("implement-backend-review-input/v1", "backend reviewer input schema version"),
        ("implement-backend-review/v1", "backend reviewer schema version"),
        ("특정 unit 이름은 이 계약에서 고정하지 않는다", "backend reviewer architecture unit neutrality"),
        ("변경 파일 경로·implementation 결과 요약·design 결과의 설계 결정", "backend reviewer source selection basis"),
    ]:
        require(errors, backend_review_spec["contract"], backend_review_contract, needle, reason)
    implement_coupling_banned = [
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
        "Input Artifact:",
        "Output Artifact:",
        "CONTEXT_CHECKPOINT:",
        "[입력 파일]",
        "[출력 파일]",
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
