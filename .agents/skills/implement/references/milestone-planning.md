# Router Milestone Planning

이 문서는 `implement` 라우터의 요구사항 분류와 backend/frontend/fullstack 마일스톤 분할 기준을 소유한다. 영역 내부의 backend 또는 frontend 마일스톤 세부 분할 기준은 각 실행 스킬의 `references/milestone-planning.md`가 소유한다.

## 요구사항 분석

- 사용자 입력을 한 문장으로 재진술하여 목표를 고정한다.
- 요구사항, 명시적 제외사항, 성공 기준을 분리한다.
- 변경 예상 파일과 문서 기준으로 backend, frontend, fullstack 여부를 판정한다.
- API 계약, 데이터 계약, UI 계약 중 어느 계약이 선행되어야 하는지 확인한다.
- 영역이 불명확하고 잘못 라우팅하면 작업 범위가 달라지는 경우에는 구현 전에 사용자에게 확인한다.

## 라우팅 기준

- backend: 서버 API, UseCase, domain, application, storage, external integration, DB/schema, backend policy, `docs/backend/**`
- frontend: UI, route/page, component, client state, API client, query/cache, rendering performance, UI/UX, `docs/frontend/**`
- fullstack: API 계약과 UI가 함께 바뀌거나 backend 결과를 frontend가 소비해야 하는 사용자 흐름
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
- `계약 전달`: 다음 영역에 넘길 API/UI/data 계약. 없으면 "없음"
- `검증 기준`: 영역별 실행 스킬이 보고해야 할 검증 결과

## 실행 준비

- 라우팅 결과와 마일스톤 계획을 사용자에게 짧게 보고한다.
- 영역별 마일스톤이 5개 이상이면 진행 여부를 확인한다.
- 진행이 확정되면 `run_id`를 생성하고 영역별 실행 스킬에 전달한다.
- run id와 영역별 경로 구성 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.
