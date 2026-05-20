# Router Orchestration Boundaries

이 문서는 `implement` 라우터와 영역별 실행 스킬 사이의 책임 경계를 정리한다. 영역 내부 D/A/B 책임 경계는 `implement-backend/references/orchestration-boundaries.md`와 `implement-frontend/references/orchestration-boundaries.md`가 각각 소유한다.

## 참여 주체

| 주체 | 책임 | 참조 문서 |
|------|------|-----------|
| `implement` 라우터 | 요구사항 분류, 기획/API 선행 단계 결정, fullstack 분해, run id 생성, 영역별 실행 순서 결정, 통합 보고 | 이 문서와 `SKILL.md` |
| `plan-implementation-requirements` | 기획 phase의 workflow, input/output 계약, checkpoint schema 소유 | [plan-implementation-requirements](../../plan-implementation-requirements/SKILL.md) |
| `product-planning-designer` | 구현 전 요구사항을 업무 흐름, 프로세스, 정책, 상태, 화면 설계로 구체화 | [.codex agent](../../../../.codex/agents/product-planning-designer.toml) |
| `write-api-spec` | API spec phase의 workflow, input/output 계약, checkpoint schema 소유 | [write-api-spec](../../write-api-spec/SKILL.md) |
| `api-contract-designer` | 기획 산출물을 backend/frontend 병렬 구현용 API 스펙으로 변환 | [.codex agent](../../../../.codex/agents/api-contract-designer.toml) |
| `implement-backend` | backend 마일스톤의 D/A/B 실행, backend input/output 검증, backend reviewer 반복 루프 | [implement-backend references](../../implement-backend/references) |
| `implement-frontend` | frontend 마일스톤의 D/A/B 실행, frontend input/output 검증, frontend reviewer 반복 루프 | [implement-frontend references](../../implement-frontend/references) |
| Supplemental reviewers | 문서, 보안 민감 변경 검토 | [review routing](../../../../docs/review/README.md) |

## 라우터 제약

- 라우터는 일반 경로에서 구현 파일을 직접 수정하지 않는다.
- 라우터는 product planning 또는 API spec artifact를 만들 수 있지만, 그 세부 출력 schema는 각 선행 스킬의 계약 문서가 소유한다.
- 라우터는 기획/API phase에서 선행 스킬의 계약을 읽고 해당 서브에이전트를 호출한다.
- 라우터는 선행 산출물 경로를 영역별 milestone input artifact의 `source_artifacts`로 정규화한다.
- 라우터는 D/A/B 서브에이전트를 직접 운영하지 않고 영역별 실행 스킬에 위임한다.
- 라우터는 영역별 input/output 파일과 체크포인트 파일의 존재 여부를 확인할 수 있지만, 영역 내부 payload 스키마를 재정의하지 않는다.
- 라우터는 backend/frontend 검토를 직접 수행하지 않는다.
- 라우터는 영역 간 계약 불확실성을 추측해 채우지 않고 사용자 보고 또는 후속 마일스톤으로 분리한다.

## 실행 스킬 경계

- `implement-backend`는 backend 코드, `docs/backend/**`, DB/schema, backend policy, server integration 변경을 소유한다.
- `implement-frontend`는 frontend 코드, `docs/frontend/**`, route/page, component, state/API/cache, rendering/UI-UX 변경을 소유한다.
- backend와 frontend가 모두 필요한 요청은 라우터가 영역별 마일스톤으로 나눈다.
- 기획 산출물과 API 스펙은 라우터가 해석해 영역별 milestone input artifact로 넘기는 입력 근거이며, backend/frontend D/A/B 계약의 대체물이 아니다.
- 선행 스킬은 서브에이전트 역할 철학을 소유하지 않고, 서브에이전트 TOML은 특정 스킬 경로를 고정하지 않는다.
- 단일 사용자 흐름이어도 검증 명령이나 변경 책임이 다르면 영역을 분리한다.

## Source of Truth 경계

- 라우터는 영역을 분류하기 위해 `AGENTS.md`, `docs/PRD.md`, `docs/backend/README.md`, `docs/frontend/README.md` 같은 진입점 문서를 읽을 수 있다.
- 라우터는 기획 산출물과 API 스펙을 `source_artifacts`로 정규화해 영역별 Source of Truth 후보로 전달할 수 있다.
- backend 세부 기준 문서 선택은 `implement-backend`와 backend 계약 문서가 소유한다.
- frontend 세부 기준 문서 선택은 `implement-frontend`와 frontend 계약 문서가 소유한다.
- 라우터는 영역별 Source of Truth 후보를 통합 문서에 고정하지 않는다.

## 인스턴스 생명주기

- 라우터는 사용자 요청 하나에 하나의 `run_id`를 생성한다.
- planning/API 선행 산출물이 필요하면 같은 `run_id` 아래에서 먼저 생성한다.
- backend/frontend 실행 스킬은 같은 `run_id` 아래에서 자기 마일스톤 파일을 생성한다.
- 공통 API 스펙이 안정적이면 backend/frontend 실행을 병렬 후보로 둘 수 있다.
- API 스펙 없이 backend 결과가 frontend 입력이면 backend 실행이 끝난 뒤 frontend 실행을 시작한다.
- 서로 독립인 backend/frontend 마일스톤이라도 결과 보고는 영역별로 분리한다.

## 판단 원칙

- 라우터의 성공 판단은 영역별 실행 스킬의 완료 결과를 종합하는 것이다.
- 기획 산출물의 완료는 구현 완료를 의미하지 않고, API 스펙의 완료는 backend/frontend 구현 완료를 의미하지 않는다.
- 한 영역의 `pass`는 다른 영역의 계약 또는 검증을 보증하지 않는다.
- 정상 산출물 전달의 표준 경로는 output artifact 파일과 결과 신호다.
- 체크포인트 복구의 표준 경로는 영역별 체크포인트 파일과 `CONTEXT_CHECKPOINT:` 신호다.
- 영역별 실행 스킬의 계약 문서와 라우터 문서가 충돌하면 영역 내부 실행은 해당 영역 문서를 우선하고, 통합 순서와 보고는 라우터 문서를 우선한다.
