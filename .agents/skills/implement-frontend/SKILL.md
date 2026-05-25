---
name: implement-frontend
description: Use when 프론트엔드 기능 구현, 리팩토링, route/page/component/state/API client/query/cache/rendering/UI-UX 변경, 또는 frontend 아키텍처 기준에 영향을 주는 변경을 수행해야 할 때.
---

# implement-frontend — 프론트엔드 구현 실행

## 목적

`implement-frontend`는 frontend 변경을 하나 이상의 마일스톤으로 나누고, 각 마일스톤을 Frontend Design Writer → Frontend Implementation Engineer → Frontend Architecture Reviewer → 수정 루프로 실행하는 frontend 전용 오케스트레이션 스킬이다.

이 문서는 스킬의 진입점이다. 핵심 구조, 문서 맵, 역할 책임 경계, 필수 작업 절차는 이 문서가 소유하고, 마일스톤 분할 기준·마일스톤 실행 세부 절차·파일 저장 규칙·Markdown artifact 섹션·체크포인트 템플릿은 references 문서가 소유한다.

## 적용 대상

포함:

- frontend 코드, route/page, component, state, API client, cache, rendering, UI/UX 변경
- `docs/frontend/**`에 직접 영향을 주는 frontend 설계·컨벤션·성능·UI/UX 변경
- backend가 제공해야 할 API 계약 또는 미해결 frontend 소비 계약 정리

제외:

- backend persistence, domain policy, DB/schema 구현
- frontend 아키텍처 기준과 무관한 일반 코드 리뷰
- 서브에이전트 간 직접 통신

## 책임

- 구현 전 요구사항 명확화 게이트를 수행한다.
- frontend 범위, 제외사항, 성공 기준, 확정 요구사항 컨텍스트를 고정한다.
- frontend 마일스톤을 나누고, 각 역할의 input/output/checkpoint artifact를 연결한다.
- Frontend Design Writer, Frontend Implementation Engineer, Frontend Architecture Reviewer의 역할 경계를 유지한다.
- architecture review 위반, 검증 실패, 체크포인트, 반복 한계 상황을 라우팅한다.
- backend API 계약 또는 미해결 frontend 소비 계약을 분리해 사용자에게 보고한다.

## 참조 문서

이 문서가 `implement-frontend`의 참조 문서 맵을 소유한다. 필요한 세부 문서만 선별해 읽는다.

핵심 개념 문서:

- 요구사항 명확화 게이트: [references/requirement-clarification-gate.md](references/requirement-clarification-gate.md)
- 확정 요구사항 컨텍스트 템플릿: [references/requirement-context-template.md](references/requirement-context-template.md)
- 상세 책임 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- 마일스톤 계획: [references/milestone-planning.md](references/milestone-planning.md)
- 실행 흐름: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)

세부 규격 문서:

- run artifact 저장·검증·복구 규약: [references/run-artifact-protocol.md](references/run-artifact-protocol.md)
- Frontend Design Writer 계약: [references/frontend-technical-design-writer-contract.md](references/frontend-technical-design-writer-contract.md)
- Frontend Implementation Engineer 계약: [references/frontend-implementation-engineer-contract.md](references/frontend-implementation-engineer-contract.md)
- Frontend Architecture Reviewer 계약: [references/frontend-architecture-reviewer-contract.md](references/frontend-architecture-reviewer-contract.md)

## 역할

| 주체 | 핵심 책임 | 책임이 아닌 것 |
|------|-----------|----------------|
| 메인 에이전트 | 요구사항 명확화, 질문 생성, 확정/미확정 UX·API·상태 정책 분리, backend dependency 확인, 브라우저 검증 기준 확정, 마일스톤 분할, Source of Truth 선별, input 작성, output 검증, 다음 단계 라우팅, 사용자 보고 | 서브에이전트의 전문 판단 대체, 미확정 제품 UX/API/cache/navigation 정책 추론 |
| Frontend Design Writer `frontend-technical-design-writer` | 확정 요구사항 컨텍스트 기반 frontend 설계 판단, TDD 작성 또는 스킵/차단 근거 작성 | 구현, 리뷰, 다음 input 작성, 사용자 직접 질문, 미확정 UX/API/cache/navigation 정책 추론 |
| Frontend Implementation Engineer `frontend-implementation-engineer` | frontend 코드 작성·수정, build/test/browser 검증 실행, 구현 output 작성 | architecture review 판정, 미확정 UX/API/cache/navigation 정책 구현 |
| Frontend Architecture Reviewer `frontend-architecture-reviewer` | 입력된 Source of Truth와 TDD 결정 기준으로 frontend 변경 파일 검토 | 기능 QA, 시각 QA, backend 검토, 입력에 없는 제품/UX 기준으로 violation 생성 |

상세 경계와 예외는 [references/orchestration-boundaries.md](references/orchestration-boundaries.md)를 따른다.

## 작업 흐름

`implement-frontend`가 호출되면 메인 에이전트는 아래 순서를 반드시 따른다. 세부 판단 기준은 각 reference 문서가 소유한다.

```text
프론트엔드 요청
  -> 요구사항 명확화 게이트
  -> 확정 요구사항 컨텍스트 기록
  -> frontend 마일스톤 계획
  -> run artifact 경로 준비
  -> Frontend Design Writer
  -> Frontend Implementation Engineer
  -> Frontend Architecture Reviewer
  -> 통과 또는 위반 수정 루프
  -> 완료 보고
```

1. 요구사항 명확화 게이트를 수행한다.
   - 구현 결정에 필요한 정책이 누락되면 구현, TDD, role input artifact 생성을 시작하지 않는다.
   - 세부 기준은 [requirement-clarification-gate.md](references/requirement-clarification-gate.md)를 따른다.
2. 확정 요구사항 컨텍스트를 기록한다.
   - 사용자 흐름, UX 정책, API 계약, 상태 소유권, cache/invalidation, 검증 기준을 설계·구현 판단 기준으로 고정한다.
   - 코드베이스 관례로 처리할 항목, 금지된 추론, 남은 미결정 사항을 분리한다.
   - 템플릿은 [requirement-context-template.md](references/requirement-context-template.md)를 따른다.
3. frontend 마일스톤을 계획한다.
   - 하나의 검증 가능한 frontend 동작 단위로 나눈다.
   - 분할 기준은 [milestone-planning.md](references/milestone-planning.md)를 따른다.
4. run artifact 경로를 준비한다.
   - `docs/frontend`가 비어 있거나 generic 문서이거나 실제 코드와 불일치하면 design 위임 전에 frontend Source of Truth 갭으로 보고한다.
   - 각 role 호출 전에 `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 할당한다.
   - 저장·검증·복구 규약은 [run-artifact-protocol.md](references/run-artifact-protocol.md)를 따른다.
5. 각 마일스톤을 design → implementation → architecture review 순서로 실행한다.
   - 역할별 input/output/checkpoint 템플릿은 각 `*-contract.md`를 따른다.
   - 실행 세부 절차는 [milestone-execution-workflow.md](references/milestone-execution-workflow.md)를 따른다.
6. architecture review 위반이 있으면 수정 루프로 보낸다.
   - `blocker` 또는 `major` 위반은 통과로 간주하지 않는다.
   - 반복 한계를 넘으면 [milestone-execution-workflow.md](references/milestone-execution-workflow.md)의 escalation 절차를 따른다.
7. 완료 시 변경 파일, 검증 결과, architecture review 판정, backend 전달 계약을 보고한다.

## 검증

frontend 실행 규약, 계약 문서, 서브에이전트 정의를 수정한 뒤에는 아래 검증을 수행한다.

- `python3 .agents/scripts/validate-context-checkpoints.py`
- `python3 /Users/a1004/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/implement-frontend`
- `python3 .agents/skills/write-skill-artifact/scripts/check_skill_artifact.py .agents/skills/implement-frontend/SKILL.md`

## 완료 기준

- frontend 마일스톤별 design/implementation/review input/output 파일 경로
- frontend 변경 파일 목록
- frontend build/test 또는 브라우저 검증 결과
- frontend architecture review 통과 여부와 남은 위반
- backend 마일스톤으로 넘겨야 할 API 계약 또는 미해결 사항
