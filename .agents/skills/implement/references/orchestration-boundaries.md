# Router Orchestration Boundaries

이 문서는 `implement` 라우터와 영역별 실행 스킬 사이의 책임 경계를 정리한다. 영역 내부 D/A/B 책임 경계는 `implement-backend/references/orchestration-boundaries.md`와 `implement-frontend/references/orchestration-boundaries.md`가 각각 소유한다.

## 참여 주체

| 주체 | 책임 | 참조 문서 |
|------|------|-----------|
| `implement` 라우터 | 요구사항 분류, fullstack 분해, run id 생성, 영역별 실행 순서 결정, 통합 보고 | 이 문서와 `SKILL.md` |
| `implement-backend` | backend 마일스톤의 D/A/B 실행, backend handoff 검증, backend reviewer 반복 루프 | [implement-backend references](../../implement-backend/references) |
| `implement-frontend` | frontend 마일스톤의 D/A/B 실행, frontend handoff 검증, frontend reviewer 반복 루프 | [implement-frontend references](../../implement-frontend/references) |
| Supplemental reviewers | 문서, 보안 민감 변경 검토 | [review routing](../../../../docs/review/README.md) |

## 라우터 제약

- 라우터는 일반 경로에서 구현 파일을 직접 수정하지 않는다.
- 라우터는 D/A/B 서브에이전트를 직접 운영하지 않고 영역별 실행 스킬에 위임한다.
- 라우터는 영역별 결과 파일과 체크포인트 파일의 존재 여부를 확인할 수 있지만, 영역 내부 payload 스키마를 재정의하지 않는다.
- 라우터는 backend/frontend 검토를 직접 수행하지 않는다.
- 라우터는 영역 간 계약 불확실성을 추측해 채우지 않고 사용자 보고 또는 후속 마일스톤으로 분리한다.

## 실행 스킬 경계

- `implement-backend`는 backend 코드, `docs/backend/**`, DB/schema, backend policy, server integration 변경을 소유한다.
- `implement-frontend`는 frontend 코드, `docs/frontend/**`, route/page, component, state/API/cache, rendering/UI-UX 변경을 소유한다.
- backend와 frontend가 모두 필요한 요청은 라우터가 영역별 마일스톤으로 나눈다.
- 단일 사용자 흐름이어도 검증 명령이나 변경 책임이 다르면 영역을 분리한다.

## Source of Truth 경계

- 라우터는 영역을 분류하기 위해 `AGENTS.md`, `docs/PRD.md`, `docs/backend/README.md`, `docs/frontend/README.md` 같은 진입점 문서를 읽을 수 있다.
- backend 세부 기준 문서 선택은 `implement-backend`와 backend 계약 문서가 소유한다.
- frontend 세부 기준 문서 선택은 `implement-frontend`와 frontend 계약 문서가 소유한다.
- 라우터는 영역별 Source of Truth 후보를 통합 문서에 고정하지 않는다.

## 인스턴스 생명주기

- 라우터는 사용자 요청 하나에 하나의 `run_id`를 생성한다.
- backend/frontend 실행 스킬은 같은 `run_id` 아래에서 자기 마일스톤 파일을 생성한다.
- backend 결과가 frontend 입력이면 backend 실행이 끝난 뒤 frontend 실행을 시작한다.
- 서로 독립인 backend/frontend 마일스톤이라도 결과 보고는 영역별로 분리한다.

## 판단 원칙

- 라우터의 성공 판단은 영역별 실행 스킬의 완료 결과를 종합하는 것이다.
- 한 영역의 `pass`는 다른 영역의 계약 또는 검증을 보증하지 않는다.
- 정상 산출물 전달의 표준 경로는 handoff artifact 파일과 결과 신호다.
- 체크포인트 복구의 표준 경로는 영역별 체크포인트 파일과 `CONTEXT_CHECKPOINT:` 신호다.
- 영역별 실행 스킬의 계약 문서와 라우터 문서가 충돌하면 영역 내부 실행은 해당 영역 문서를 우선하고, 통합 순서와 보고는 라우터 문서를 우선한다.
