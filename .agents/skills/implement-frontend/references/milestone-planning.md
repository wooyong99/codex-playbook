# Frontend Milestone Planning

이 문서는 `implement-frontend` 스킬의 frontend 요구사항 분석과 마일스톤 분할 기준을 소유한다. 실행 중 D/A/B 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유한다.

## 요구사항 분석

- 사용자 입력을 frontend 관점의 한 문장 목표로 고정한다.
- route/page, feature/entity, component, state, API client, cache, rendering, UI/UX 중 무엇이 바뀌는지 분리한다.
- 명시적 제외사항을 요구사항과 분리해 기록한다.
- API 계약, 상태 소유권, cache key, loading/error/empty 상태, 브라우저 검증 기준이 불명확하면 구현 전에 확인한다.
- backend 저장 방식이나 도메인 정책 변경은 frontend 마일스톤 범위로 끌어오지 않는다.

## 마일스톤 분할 기준

frontend 마일스톤은 하나의 사용자 흐름 또는 하나의 화면 책임과 하나의 검증 가능한 UI 동작을 기준으로 나눈다. 목표는 한 D/A/B 루프가 과도하게 커지기 전에 끝나는 단위로 작업을 제한하는 것이다.

마일스톤 기본 단위:

- 사용자 관점의 frontend 결과 1개
- route/page 1개 또는 밀접한 화면 묶음 1개
- feature/entity 책임 1개
- 주요 상태 소유권 또는 API/cache 경계 1개
- component 묶음 1개
- loading/error/empty/success 상태 검증 묶음 1개
- 예상 변경 파일 3~8개 권장
- build/test 또는 브라우저 검증 묶음 1개로 성공과 실패 판단 가능

무조건 분할을 검토하는 조건:

- 독립 사용자 흐름이 2개 이상이다.
- route/page 3개 이상 또는 feature/entity 3개 이상을 동시에 건드린다.
- 예상 변경 파일이 12개를 넘는다.
- API client 계약, query key/cache 정책, 전역 상태 구조가 핵심 UI 변경과 섞여 있다.
- responsive layout, 접근성, 성능 최적화가 기능 구현과 크게 섞여 있다.
- 한 번의 frontend B 검토 대상이 10개 파일을 넘는다.

분할이 어렵다면 하나의 큰 마일스톤으로 강행하지 않고 `M{n}-frontend-a`, `M{n}-frontend-b` 같은 하위 마일스톤으로 나눈다. 사용자가 한 번에 체감하는 원자적 흐름일 때만 큰 마일스톤을 허용한다.

## 규모별 기준

- 단일 화면의 작은 상태 추가는 보통 1개 frontend 마일스톤으로 둔다.
- API client와 화면 상태가 함께 바뀌는 기능은 보통 설계, 구현, 검증이 한 루프에서 끝나는지 먼저 판단한다.
- 여러 화면에 걸친 기능은 보통 2~4개 frontend 마일스톤으로 나눈다.
- 전역 상태 구조, routing 구조, cache 전략 리팩토링은 5개 이상 마일스톤을 허용하되 사용자에게 진행 여부를 먼저 확인한다.

## 마일스톤 메타데이터

각 frontend 마일스톤에는 아래 항목을 붙인다.

- `목표`: 사용자 관점 frontend 결과 1개
- `범위`: 포함할 route/page, feature/entity, component, state/API/cache 영역
- `명시적 제외사항`: 사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"
- `예상 변경 파일 수`: 3~8개 권장
- `검증 기준`: 실행할 build/test 또는 브라우저 검증 명령
- `backend 계약`: 필요한 API 계약 또는 불확실성. 없으면 "없음"

## 실행 준비

- 마일스톤 계획을 사용자에게 짧게 보고한다.
- 마일스톤이 5개 이상이면 진행 여부를 확인한다.
- 진행이 확정되면 `run_id`를 생성하고 `.agents/runs/{run_id}/inputs`, `.agents/runs/{run_id}/outputs`, `.agents/runs/{run_id}/checkpoints` 하위 경로를 준비한다.
- run id와 경로 구성 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.
