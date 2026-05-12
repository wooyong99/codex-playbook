---
name: implement-backend
description: 백엔드 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경, storage/external/app/application 계층 변경을 기술설계(D) → backend 구현(A) → backend 아키텍처 검토(B) → 수정 루프로 실행하는 스킬. backend-only 요청이거나 `implement` 라우터가 backend 마일스톤으로 분류한 작업에 사용한다.
---

# implement-backend — 백엔드 구현 실행

## 역할

- backend 마일스톤을 기술설계(D), backend 구현(A), backend 아키텍처 검토(B), 위반 수정 루프로 실행한다.
- Agent D는 `backend-technical-design-writer`를 사용하며, backend TDD가 필요하면 `write-backend-tech-design-doc` 스킬을 통해 문서를 작성한다.
- Agent A는 `backend-implementation-engineer`를 사용한다.
- Agent B는 `backend-architecture-reviewer`를 사용한다.
- 문서 구조 변경과 보안 민감 변경은 필요한 경우 supplemental reviewer로 추가한다.

## 참조 문서

- 공통 역할 경계: [../implement/references/orchestration-boundaries.md](../implement/references/orchestration-boundaries.md)
- 공통 마일스톤 분할 기준: [../implement/references/milestone-planning.md](../implement/references/milestone-planning.md)
- 공통 handoff/checkpoint 규약: [../implement/references/handoff-checkpoint-protocol.md](../implement/references/handoff-checkpoint-protocol.md)
- 공통 실행 루프: [../implement/references/milestone-execution-workflow.md](../implement/references/milestone-execution-workflow.md)
- D 계약: [references/backend-technical-design-writer-contract.md](references/backend-technical-design-writer-contract.md)
- backend TDD 작성 스킬: [../write-backend-tech-design-doc/SKILL.md](../write-backend-tech-design-doc/SKILL.md)
- A 계약: [references/backend-implementation-engineer-contract.md](references/backend-implementation-engineer-contract.md)
- B 계약: [references/backend-architecture-reviewer-contract.md](references/backend-architecture-reviewer-contract.md)

## 실행 원칙

- backend 코드와 `docs/backend/**`에 직접 영향을 주는 범위만 처리한다.
- frontend 작업은 직접 구현하지 않고 `implement-frontend` 마일스톤으로 분리한다.
- backend와 frontend가 함께 필요한 요청에서는 API 계약, 도메인 상태, 데이터 저장, 외부 연동을 먼저 안정화한다.
- backend 변경 파일은 `backend-architecture-reviewer`가 검토한다.
- secret, token, 인증/인가, 로그, 외부 연동 설정 변경은 `security-policy-reviewer`를 추가한다.

## 프로세스

1. 요구사항, 명시적 제외사항, 성공 기준을 backend 관점으로 고정한다.
2. 마일스톤을 backend 도메인 경계, 트랜잭션 경계, 계층 경계, 검증 범위 기준으로 나눈다.
3. run id와 handoff/checkpoint 경로를 할당한다.
4. 필요한 경우 D를 호출해 backend TDD를 작성하거나 skip 근거를 받는다.
5. A로 `backend-implementation-engineer`를 호출해 구현 또는 수정을 수행한다.
6. B로 `backend-architecture-reviewer`를 호출해 B 계약의 `[Source of Truth]` 기준 준수 여부를 검토한다.
7. 위반이 있으면 같은 backend A 인스턴스에 수정 작업을 맡기고 B를 새 인스턴스로 다시 호출한다.
8. 모든 backend B와 필수 supplemental reviewer가 통과하면 마일스톤을 완료한다.

## 완료 산출물

- backend 마일스톤별 D/A/B 결과 파일 경로
- backend 변경 파일 목록
- backend compile/test 검증 결과
- backend architecture review 통과 여부와 남은 위반
- frontend 마일스톤으로 넘겨야 할 계약 또는 미해결 사항
