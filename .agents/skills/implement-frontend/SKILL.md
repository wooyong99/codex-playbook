---
name: implement-frontend
description: 프론트엔드 기능 구현, 리팩토링, UI 상태/API client/query/cache/rendering/UI-UX 변경을 기술설계(D) → frontend 구현(A) → frontend 아키텍처 검토(B) → 수정 루프로 실행하는 스킬. frontend-only 요청이거나 `implement` 라우터가 frontend 마일스톤으로 분류한 작업에 사용한다.
---

# implement-frontend — 프론트엔드 구현 실행

## 역할

- frontend 마일스톤을 기술설계(D), frontend 구현(A), frontend 아키텍처 검토(B), 위반 수정 루프로 실행한다.
- Agent D는 `frontend-technical-design-writer`를 사용하며, frontend TDD가 필요하면 `write-frontend-tech-design-doc` 스킬을 통해 문서를 작성한다.
- Agent A는 `frontend-implementation-engineer`를 사용한다.
- Agent B는 `frontend-architecture-reviewer`를 사용한다.
- 문서 구조 변경과 보안 민감 변경은 필요한 경우 supplemental reviewer로 추가한다.

## 참조 문서

- frontend 역할 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- frontend 마일스톤 분할 기준: [references/milestone-planning.md](references/milestone-planning.md)
- frontend input/output/checkpoint 규약: [references/input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)
- frontend 실행 루프: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)
- D 계약: [references/frontend-technical-design-writer-contract.md](references/frontend-technical-design-writer-contract.md)
- frontend TDD 작성 스킬: [../write-frontend-tech-design-doc/SKILL.md](../write-frontend-tech-design-doc/SKILL.md)
- A 계약: [references/frontend-implementation-engineer-contract.md](references/frontend-implementation-engineer-contract.md)
- B 계약: [references/frontend-architecture-reviewer-contract.md](references/frontend-architecture-reviewer-contract.md)

## 실행 원칙

- frontend 코드와 `docs/frontend/**`에 직접 영향을 주는 범위만 처리한다.
- backend 작업은 직접 구현하지 않고 `implement-backend` 마일스톤으로 분리한다.
- backend API 계약이 불확실하면 구현 전에 계약 불확실성으로 보고하거나 backend 마일스톤을 선행시킨다.
- frontend 변경 파일은 `frontend-architecture-reviewer`가 검토한다.
- secret, token, 인증/인가, 민감 정보 노출, 외부 연동 설정 변경은 `security-policy-reviewer`를 추가한다.

## 프로세스

1. 요구사항, 명시적 제외사항, 성공 기준을 frontend 관점으로 고정한다.
2. 마일스톤을 사용자 흐름, route/page, feature/entity 경계, 상태/API/cache 경계, UI 검증 범위 기준으로 나눈다.
3. run id와 input/output/checkpoint 경로를 할당한다.
4. 필요한 경우 D를 호출해 frontend TDD를 작성하거나 skip 근거를 받는다.
5. A로 `frontend-implementation-engineer`를 호출해 구현 또는 수정을 수행한다.
6. B로 `frontend-architecture-reviewer`를 호출해 B 계약 형식으로 전달한 이번 frontend 검토의 `[Source of Truth]` 기준 준수 여부를 검토한다.
7. 위반이 있으면 같은 frontend A 인스턴스에 수정 작업을 맡기고 B를 새 인스턴스로 다시 호출한다.
8. 모든 frontend B와 필수 supplemental reviewer가 통과하면 마일스톤을 완료한다.

## 완료 산출물

- frontend 마일스톤별 D/A/B input/output 파일 경로
- frontend 변경 파일 목록
- frontend build/test 또는 브라우저 검증 결과
- frontend architecture review 통과 여부와 남은 위반
- backend 마일스톤으로 넘겨야 할 API 계약 또는 미해결 사항
