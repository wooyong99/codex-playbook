# Router Milestone Planning

이 문서는 `implement` 라우터의 요구사항 분류와 backend/frontend/fullstack 마일스톤 분할 기준을 소유한다. 영역 내부의 backend 또는 frontend 마일스톤 세부 분할 기준은 각 실행 스킬의 `references/milestone-planning.md`가 소유한다.

## 요구사항 분석

- 사용자 입력을 한 문장으로 재진술하여 목표를 고정한다.
- 요구사항, 명시적 제외사항, 성공 기준을 분리한다.
- 업무 흐름, 프로세스, 정책, 상태, 화면 흐름, 도메인 용어가 구현 가능한 수준인지 확인한다.
- 위 항목이 비어 있고 추측하면 구현 범위가 달라지는 경우 사용자에게 질문하거나 `plan-implementation-requirements` 계약으로 `product-planning-designer`를 먼저 호출한다.
- 기획 산출물이 있으면 라우팅과 마일스톤 분할의 기준 입력으로 사용한다.
- 변경 예상 파일과 문서 기준으로 backend, frontend, fullstack 여부를 판정한다.
- API 계약, 데이터 계약, UI 계약 중 어느 계약이 선행되어야 하는지 확인한다.
- API 계약이 backend/frontend 병렬 구현의 기준이 되는 경우 `write-api-spec` 계약으로 `api-contract-designer`를 먼저 호출한다.
- 영역이 불명확하고 잘못 라우팅하면 작업 범위가 달라지는 경우에는 구현 전에 사용자에게 확인한다.

## 기획 산출물 필요 기준

아래 조건 중 하나라도 해당하면 영역별 실행 전에 기획 산출물을 만든다.

- 사용자 요구가 한두 문장 수준이고 업무 흐름, 정책, 상태, 화면 흐름이 비어 있다.
- 승인, 반려, 취소, 재시도, 권한, 감사, 알림 같은 업무 정책이 구현 결과를 좌우한다.
- backend 도메인 상태와 frontend 화면 상태가 같은 사용자 흐름에서 함께 바뀐다.
- 여러 사용자 유형 또는 시스템 행위자가 같은 업무 흐름에 참여한다.
- 기존 PRD만으로는 이번 구현 범위의 인수 기준을 판단하기 어렵다.

기획 산출물이 필요하지만 사용자에게 질문해야 하는 경우:

- 누가 어떤 권한으로 기능을 쓰는지 확정되지 않았다.
- 상태 전이 guard 또는 실패 복구 정책이 구현 범위를 바꿀 수 있다.
- 화면 진입점과 주요 액션이 API 계약을 바꿀 수 있다.
- 데이터 보존, 감사, 외부 연동 정책이 필수인지 불명확하다.

## API 스펙 필요 기준

아래 조건 중 하나라도 해당하면 영역별 실행 전에 API 스펙을 만든다.

- frontend가 새 backend API 또는 변경된 response shape를 소비한다.
- backend 상태 전이와 frontend UI 상태가 같은 operation에 연결된다.
- error, auth, pagination, cache, idempotency가 화면 동작에 영향을 준다.
- backend/frontend를 병렬로 구현하려면 mock과 contract test 기준이 필요하다.

API 스펙의 `stable_for_parallel`이 `true`일 때만 backend/frontend 병렬 실행을 허용한다.

## 라우팅 기준

- backend: 서버 API, UseCase, domain, application, storage, external integration, DB/schema, backend policy, `docs/backend/**`
- frontend: UI, route/page, component, client state, API client, query/cache, rendering performance, UI/UX, `docs/frontend/**`
- fullstack: API 계약과 UI가 함께 바뀌거나 backend 결과를 frontend가 소비해야 하는 사용자 흐름
- planning-required: 구현 전에 업무 흐름, 정책, 상태, 화면 설계를 확정해야 하는 사용자 흐름
- api-spec-required: backend/frontend 공통 API 계약을 먼저 확정해야 하는 사용자 흐름
- 문서 구조 변경은 구현 흐름에 섞지 않고 문서 검토 대상으로 분리한다.
- 보안 민감 변경은 영역과 무관하게 supplemental reviewer 대상 후보로 표시한다.

## 마일스톤 분할 기준

라우터 마일스톤은 backend/frontend 실행 스킬에 넘길 수 있는 독립 영역 단위로 나눈다. 영역 내부의 예상 변경 파일 수, D/A/B 호출 순서, 검증 명령 세부 판단은 해당 실행 스킬이 소유한다.

라우터 기본 단위:

- 사용자 관점 결과 1개
- backend 또는 frontend 중 주 책임 영역 1개
- 영역 간 계약 1개
- 명시적 제외사항 1개 묶음
- 실행 스킬 하나가 완료 여부를 판단할 수 있는 검증 기준 1개

무조건 분할을 검토하는 조건:

- backend API 계약과 frontend UI 변경이 모두 필요하다.
- 데이터 저장 방식과 화면 상태 관리가 동시에 바뀐다.
- 공통 API 스펙이 안정화되지 않았거나 operation별 병렬 가능 여부가 다르다.
- 인증/인가, 외부 연동, 민감 정보 노출, 문서 구조 변경이 기능 구현과 섞여 있다.
- 한 영역의 산출물이 다른 영역의 입력이 된다.
- 사용자 흐름은 하나지만 backend와 frontend 검증 명령이 서로 독립적이다.

## 실행 순서 기준

- frontend가 소비할 API 계약이 바뀌면 backend 마일스톤을 먼저 실행한다.
- backend 변경 없이 UI 표현, local state, client cache만 바뀌면 frontend 마일스톤만 실행한다.
- backend 저장 모델이 불확실하면 frontend 마일스톤을 시작하지 않고 계약 불확실성을 먼저 보고한다.
- frontend 검증 중 backend 계약 누락이 드러나면 새 backend 마일스톤을 만들거나 사용자에게 범위 확장을 확인한다.

## 마일스톤 메타데이터

각 라우터 마일스톤에는 아래 항목을 붙인다.

- `목표`: 사용자 관점 결과 1개
- `영역`: `backend`, `frontend`, `fullstack split`
- `선행 관계`: 먼저 실행해야 하는 영역. 없으면 "없음"
- `명시적 제외사항`: 사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"
- `기획 산출물`: 연결된 planning output artifact. 없으면 "없음"
- `API 스펙`: 연결된 API spec artifact와 병렬 실행 가능 여부. 없으면 "없음"
- `계약 전달`: 다음 영역에 넘길 API/UI/data 계약. 없으면 "없음"
- `검증 기준`: 영역별 실행 스킬이 보고해야 할 검증 결과

## 실행 준비

- 라우팅 결과와 마일스톤 계획을 사용자에게 짧게 보고한다.
- 영역별 마일스톤이 5개 이상이면 진행 여부를 확인한다.
- 진행이 확정되면 `run_id`를 생성하고 영역별 실행 스킬에 전달한다.
- run id와 영역별 경로 구성 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.
