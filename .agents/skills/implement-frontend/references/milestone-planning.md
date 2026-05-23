# Frontend Milestone Planning

이 문서는 `implement-frontend`가 frontend 요구사항을 어떤 마일스톤 단위로 나누는지 정의한다.

요구사항 명확화 게이트는 [requirement-clarification-gate.md](requirement-clarification-gate.md)가 소유한다. 실행 중 design/implementation/review 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 파일 저장 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)가 소유한다.

## 계획 모델

frontend 마일스톤은 하나의 사용자 흐름 또는 하나의 화면 책임을 끝까지 닫는 단위다.

좋은 frontend 마일스톤은 아래 조건을 만족한다.

- 사용자 관점의 frontend 결과가 하나다.
- route/page 또는 밀접한 화면 묶음이 하나다.
- 주요 상태 소유권 또는 API/cache 경계가 하나다.
- loading/error/empty/success 상태를 함께 검증할 수 있다.
- build/test 또는 브라우저 검증 한 묶음으로 성공 여부를 판단할 수 있다.
- design/implementation/review 루프가 과도하게 커지기 전에 끝난다.

## 계획 산출물

각 frontend 마일스톤에는 아래 메타데이터를 붙인다.

- `목표`: 사용자 관점 frontend 결과 1개
- `범위`: 포함할 route/page, feature/entity, component, state/API/cache 영역
- `명시적 제외사항`: 사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"
- `확정 요구사항 컨텍스트`: 요구사항 명확화 게이트 결과 경로 또는 요약
- `검증 기준`: 실행할 build/test 또는 브라우저 검증 명령
- `backend 계약`: 필요한 API 계약 또는 불확실성. 없으면 "없음"
- `예상 변경 파일 수`: 가능하면 3~8개

## 요구사항 분석

마일스톤을 나누기 전에 [requirement-clarification-gate.md](requirement-clarification-gate.md)에 따라 사용자 입력을 frontend 관점의 구현 가능한 목표로 고정한다. 구현 방식에 영향을 주는 UX/API/state/cache/rendering/verification 정보가 누락되면 마일스톤을 만들지 않고 사용자에게 질문한다.

분리해서 확인할 항목:

- 사용자 흐름, 대상 route/page, feature/entity, component, state, API client, cache, rendering, UI/UX 중 무엇이 바뀌는가
- 명시적 제외사항은 무엇인가
- API 계약과 backend 응답 shape가 확정돼 있는가
- 상태 소유권, cache key, invalidation, optimistic update, loading/error/empty/success 상태가 필요한가
- form submit, 중복 실행 방지, 실패 복구, URL state, navigation guard가 필요한가
- 브라우저 검증, 반응형, 접근성, 시각 검증 기준이 무엇인가
- backend 저장 방식이나 도메인 정책 변경이 frontend 범위로 잘못 들어와 있지 않은가

모호한 요청에서 먼저 확인할 기준:

- 목록 화면: 대상 사용자, route, API 계약, 정렬/필터, pagination, loading/error/empty, 데이터 규모
- 폼 구현: validation, submit lifecycle, 중복 제출 방지, 실패 복구, dirty state, navigation guard
- 검색 UI: URL state, debounce, API contract, cache key, no-result UX, 성능 기준
- UI 개선: design source, 변경 범위, responsive/a11y, 기존 design system 준수, visual verification
- 상태관리 구조 개선: state ownership, global state 사용 여부, cache invalidation, 기존 route/component 호환 범위

## 마일스톤 분할 기준

기본 권장 단위:

- 사용자 관점의 frontend 결과 1개
- route/page 1개 또는 밀접한 화면 묶음 1개
- feature/entity 책임 1개
- 주요 상태 소유권 또는 API/cache 경계 1개
- component 묶음 1개
- loading/error/empty/success 상태 검증 묶음 1개
- 예상 변경 파일 3~8개 권장
- build/test 또는 브라우저 검증 묶음 1개

분할을 반드시 검토하는 조건:

- 독립 사용자 흐름이 2개 이상이다.
- route/page 3개 이상 또는 feature/entity 3개 이상을 동시에 건드린다.
- 예상 변경 파일이 12개를 넘는다.
- API client 계약, query key/cache 정책, 전역 상태 구조가 핵심 UI 변경과 섞여 있다.
- cache/invalidation, optimistic update, URL state, form lifecycle이 component 구현과 강하게 결합돼 있다.
- responsive layout, 접근성, 성능 최적화가 기능 구현과 크게 섞여 있다.
- large list virtualization, infinite query, scroll restoration, browser verification이 별도 검증 단위를 요구한다.
- 한 번의 frontend architecture review 대상이 10개 파일을 넘는다.

분할이 어렵다면 하나의 큰 마일스톤으로 강행하지 않고 `M{n}-frontend-a`, `M{n}-frontend-b` 같은 하위 마일스톤으로 나눈다. 사용자가 한 번에 체감하는 원자적 흐름일 때만 큰 마일스톤을 허용한다.

## 규모별 기준

- 단일 화면의 작은 상태 추가는 보통 1개 frontend 마일스톤으로 둔다.
- API client와 화면 상태가 함께 바뀌는 기능은 설계, 구현, 검증이 한 루프에서 끝나는지 먼저 판단한다.
- 여러 화면에 걸친 기능은 보통 2~4개 frontend 마일스톤으로 나눈다.
- 전역 상태 구조, routing 구조, cache 전략 리팩토링은 5개 이상 마일스톤을 허용하되 사용자에게 진행 여부를 먼저 확인한다.

## 실행 준비

- 마일스톤 계획을 사용자에게 짧게 보고한다.
- 마일스톤이 5개 이상이면 진행 여부를 확인한다.
- 진행이 확정되면 `run_id`를 생성하고 frontend 마일스톤의 run artifact 경로를 준비한다.
- run artifact의 디렉토리 구조와 파일명 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.
