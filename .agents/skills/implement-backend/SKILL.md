---
name: implement-backend
description: 백엔드 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경, storage/external/app/application 계층 변경을 Backend Design Writer → Backend Implementation Engineer → Backend Architecture Reviewer → 수정 루프로 실행하는 backend 전용 스킬.
---

# implement-backend — 백엔드 구현 실행

## 목적

`implement-backend`는 backend 변경을 하나 이상의 마일스톤으로 나누고, 각 마일스톤을 Backend Design Writer → Backend Implementation Engineer → Backend Architecture Reviewer → 수정 루프로 실행하는 backend 전용 오케스트레이션 스킬이다.

이 문서는 스킬의 진입점이다. 전체 구조와 책임 경계만 설명하고, 세부 파일 규칙·Markdown artifact 섹션·체크포인트 템플릿은 references 문서가 소유한다.

## 적용 범위

포함:

- backend 코드, 서버 설정, DB/schema, UseCase, domain, storage, external integration 변경
- `docs/backend/**`에 직접 영향을 주는 backend 설계·정책·전략 변경
- frontend가 소비할 API 계약 또는 미해결 backend 계약 정리

제외:

- frontend 화면, route, component, client cache, UI 상태 구현
- backend 아키텍처 기준과 무관한 일반 코드 리뷰
- 서브에이전트 간 직접 통신

## 참조 문서

먼저 [references/README.md](references/README.md)를 읽고 문서 계층을 확인한다.

핵심 개념 문서:

- 책임 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- 마일스톤 계획: [references/milestone-planning.md](references/milestone-planning.md)
- 실행 흐름: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)

세부 규격 문서:

- input/output/checkpoint 규약: [references/input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)
- Backend Design Writer 계약: [references/backend-technical-design-writer-contract.md](references/backend-technical-design-writer-contract.md)
- Backend Implementation Engineer 계약: [references/backend-implementation-engineer-contract.md](references/backend-implementation-engineer-contract.md)
- Backend Architecture Reviewer 계약: [references/backend-architecture-reviewer-contract.md](references/backend-architecture-reviewer-contract.md)

관련 스킬:

- backend TDD 작성: [../write-backend-tech-design-doc/SKILL.md](../write-backend-tech-design-doc/SKILL.md)

## 운영 모델

`implement-backend`의 중심 책임은 메인 에이전트의 오케스트레이션이다.

- 메인 에이전트는 요구사항을 backend 마일스톤으로 나눈다.
- 메인 에이전트는 각 서브에이전트 호출 전에 input artifact를 저장한다.
- 서브에이전트는 자기 역할의 output artifact와 checkpoint snapshot을 저장한다.
- 메인 에이전트는 output을 검증하고, 다음 서브에이전트의 input artifact로 재구성한다.
- Backend Architecture Reviewer가 blocker/major 위반을 반환하면 같은 Backend Implementation Engineer 인스턴스에 수정 작업을 맡긴다.

```text
Backend request
  -> Main agent plans backend milestones
  -> Backend Design Writer input -> design output
  -> Main agent converts design output into implementation input
  -> implementation output
  -> Main agent converts implementation output into architecture review input
  -> architecture review output
  -> pass or implementation fix loop
```

## 역할

- Backend Design Writer: `backend-technical-design-writer`
- Backend Implementation Engineer: `backend-implementation-engineer`
- Backend Architecture Reviewer: `backend-architecture-reviewer`

역할별 상세 책임은 [references/orchestration-boundaries.md](references/orchestration-boundaries.md)가 소유한다.

## 실행 흐름

1. backend 범위, 제외사항, 성공 기준을 확정한다.
2. [milestone-planning.md](references/milestone-planning.md)에 따라 마일스톤을 나눈다.
3. [input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)에 따라 run 경로를 준비한다.
4. [milestone-execution-workflow.md](references/milestone-execution-workflow.md)에 따라 design/implementation/review 루프를 실행한다.
5. `backend-architecture-reviewer`가 통과하면 backend 마일스톤을 완료한다.

## 검증

backend 실행 규약, 계약 문서, 서브에이전트 정의를 수정한 뒤에는 아래 검증을 수행한다.

- `python3 .agents/scripts/validate-context-checkpoints.py`
- `python3 /Users/a1004/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/implement-backend`
- `python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py .agents/skills/implement-backend/SKILL.md .agents/skills/implement-backend/references/*.md`

## 완료 기준

- backend 마일스톤별 design/implementation/review input/output 파일 경로
- backend 변경 파일 목록
- backend compile/test 검증 결과
- backend architecture review 통과 여부와 남은 위반
- frontend 마일스톤으로 넘겨야 할 계약 또는 미해결 사항
