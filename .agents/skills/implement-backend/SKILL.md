---
name: implement-backend
description: Use when 백엔드 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경, storage/external/app/application 계층 변경, 또는 backend 아키텍처 기준에 영향을 주는 변경을 수행해야 할 때.
---

# implement-backend — 백엔드 구현 실행

## 목적

`implement-backend`는 backend 변경을 하나 이상의 마일스톤으로 나누고, 각 마일스톤을 Backend Design Writer → Backend Implementation Engineer → Backend Architecture Reviewer → 수정 루프로 실행하는 backend 전용 오케스트레이션 스킬이다.

이 문서는 스킬의 진입점이다. 핵심 구조, 문서 맵, 역할 책임 경계, 작업 흐름은 이 문서가 소유하고, 세부 파일 규칙·Markdown artifact 섹션·체크포인트 템플릿은 references 문서가 소유한다.

## 적용 대상

포함:

- backend 코드, 서버 설정, DB/schema, UseCase, domain, storage, external integration 변경
- `docs/backend/**`에 직접 영향을 주는 backend 설계·정책·전략 변경
- frontend가 소비할 API 계약 또는 미해결 backend 계약 정리

제외:

- frontend 화면, route, component, client cache, UI 상태 구현
- backend 아키텍처 기준과 무관한 일반 코드 리뷰
- 서브에이전트 간 직접 통신

## 책임

- 구현 전 요구사항 명확화 게이트를 수행한다.
- backend 범위, 제외사항, 성공 기준, 확정 요구사항 컨텍스트를 고정한다.
- backend 마일스톤을 나누고, 각 역할의 input/output/checkpoint artifact를 연결한다.
- Backend Design Writer, Backend Implementation Engineer, Backend Architecture Reviewer의 역할 경계를 유지한다.
- architecture review 위반, 검증 실패, 체크포인트, 반복 한계 상황을 라우팅한다.

## 참조 문서

이 문서가 `implement-backend`의 참조 문서 맵을 소유한다. 필요한 세부 문서만 선별해 읽는다.

핵심 개념 문서:

- 요구사항 명확화 게이트: [references/requirement-clarification-gate.md](references/requirement-clarification-gate.md)
- 상세 책임 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
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

`implement-backend`의 중심 책임은 메인 에이전트의 오케스트레이션이다. 메인 에이전트가 요구사항을 명확히 한 뒤 파일 기반 input/output/checkpoint artifact로 backend 역할 서브에이전트를 연결한다.

```text
백엔드 요청
  -> 메인 에이전트가 요구사항 명확화 게이트 수행
  -> 구현 결정에 필요한 정보가 없으면 사용자에게 질문
  -> 확정 요구사항 컨텍스트 기록
  -> backend 마일스톤 계획
  -> Backend Design Writer 입력 -> 설계 출력
  -> 메인 에이전트가 설계 출력을 구현 입력으로 변환
  -> Backend Implementation Engineer 구현 출력
  -> 메인 에이전트가 구현 출력을 아키텍처 검토 입력으로 변환
  -> Backend Architecture Reviewer 검토 출력
  -> 통과 또는 구현 수정 루프
```

## 역할

| 주체 | 핵심 책임 | 책임이 아닌 것 |
|------|-----------|----------------|
| 메인 에이전트 | 요구사항 명확화, 질문 생성, 확정/미확정 정책 분리, 운영 가능성 확인, 마일스톤 분할, Source of Truth 선별, input 작성, output 검증, 다음 단계 라우팅, 사용자 보고 | 서브에이전트의 전문 판단 대체, 미확정 비즈니스/운영 정책 추론 |
| Backend Design Writer `backend-technical-design-writer` | 확정 요구사항 컨텍스트 기반 backend 설계 판단, TDD 작성 또는 스킵/차단 근거 작성 | 구현, 리뷰, 다음 input 작성, 사용자 직접 질문, 미확정 정책 추론 |
| Backend Implementation Engineer `backend-implementation-engineer` | backend 코드 작성·수정, 검증 실행, 구현 output 작성 | architecture review 판정, 미확정 정책 구현 |
| Backend Architecture Reviewer `backend-architecture-reviewer` | 입력된 Source of Truth와 TDD 결정 기준으로 backend 변경 파일 검토 | 기능 QA, 성능 튜닝 제안, frontend 검토, 입력에 없는 기준으로 violation 생성 |

상세 경계와 예외는 [references/orchestration-boundaries.md](references/orchestration-boundaries.md)를 따른다.

## 작업 흐름

1. [requirement-clarification-gate.md](references/requirement-clarification-gate.md)에 따라 구현 전 요구사항 명확화 게이트를 수행한다.
2. backend 범위, 제외사항, 성공 기준, 확정 요구사항 컨텍스트를 고정한다.
3. [milestone-planning.md](references/milestone-planning.md)에 따라 마일스톤을 나눈다.
4. [input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)에 따라 run 경로를 준비한다.
5. [milestone-execution-workflow.md](references/milestone-execution-workflow.md)에 따라 design/implementation/review 루프를 실행한다.
6. `backend-architecture-reviewer`가 통과하면 backend 마일스톤을 완료한다.

## 검증

backend 실행 규약, 계약 문서, 서브에이전트 정의를 수정한 뒤에는 아래 검증을 수행한다.

- `python3 .agents/scripts/validate-context-checkpoints.py`
- `python3 /Users/a1004/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/implement-backend`
- `python3 .agents/skills/write-skill-artifact/scripts/check_skill_artifact.py .agents/skills/implement-backend/SKILL.md`

## 완료 기준

- backend 마일스톤별 design/implementation/review input/output 파일 경로
- backend 변경 파일 목록
- backend compile/test 검증 결과
- backend architecture review 통과 여부와 남은 위반
- frontend 마일스톤으로 넘겨야 할 계약 또는 미해결 사항
