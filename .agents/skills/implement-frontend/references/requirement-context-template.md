# Frontend Requirement Context Template

이 문서는 `implement-frontend`가 요구사항 명확화 게이트를 통과한 뒤 저장하는 확정 요구사항 컨텍스트 artifact의 템플릿을 정의한다.

## 문서 역할

확정 요구사항 컨텍스트는 메인 에이전트가 작성하는 공통 입력 artifact다.

목적은 사용자 흐름, UX 정책, API 계약, 상태 변화, cache/invalidation, 검증 요구사항을 명확히 정의하여 Frontend Design Writer와 Implementation Engineer가 추가 해석 없이 화면과 상호작용을 설계·구현할 수 있게 하는 것이다.

- 요구사항 명확화 기준은 [requirement-clarification-gate.md](requirement-clarification-gate.md)가 소유한다.
- run 저장 위치와 파일명 규칙은 [run-artifact-protocol.md](run-artifact-protocol.md)가 소유한다.
- design/implementation/review input에서 이 파일의 경로를 참조한다.
- 각 서브에이전트는 이 파일에 없는 제품 UX, navigation flow, API shape, cache freshness, invalidation, optimistic update, destructive action, form validation 정책을 임의로 확정하지 않는다.

## 저장 위치

run 전체에 같은 요구사항 경계를 적용할 수 있으면 아래 경로를 권장한다.

```text
.agents/runs/{run_id}/inputs/requirement-context.v1.md
```

마일스톤별로 요구사항 경계가 다르면 아래 경로를 사용한다.

```text
.agents/runs/{run_id}/inputs/M{n}/requirement-context.v1.md
```

## Template

````markdown
# Frontend Requirement Context

## Metadata

```yaml
schema_version: implement-frontend-requirement-context/v1
run_id: <run_id>
milestone: <all | M<n>>
created_at: <ISO-8601 timestamp>
source_request: <사용자 요청 요약>
```

## 요청 요약

- 사용자가 요청한 frontend 변경을 한 문단으로 요약한다.
- 원문 요청의 핵심 의도와 이번 run에서 다룰 화면·상호작용 문제를 분리한다.

## 사용자 목표

- 사용자가 화면에서 달성해야 하는 결과를 기록한다.
- 성공으로 간주할 수 있는 observable frontend 결과를 적는다.

## 범위와 제외사항

- 이번 run 또는 마일스톤에 포함할 route, page, component, state, API client, cache, rendering, UI/UX 범위를 기록한다.
- 명시적으로 제외할 화면, interaction, API 계약, responsive/a11y, 후속 작업을 기록한다.

## 사용자 흐름

- 사용 주체, 진입 화면, 주요 행동 순서, 완료 후 기대 상태를 기록한다.
- 예외 흐름, 취소, 재시도, 뒤로가기, 중복 실행 방지 필요 여부를 기록한다.

## 라우팅과 진입 경로

- route, page/layout, deep link, redirect, guard, URL state, back navigation 요구를 기록한다.
- 미확정 route나 navigation 정책은 임의로 정하지 않고 `남은 미결정 사항`으로 보낸다.

## 화면 상태와 Interaction 정책

- loading, error, empty, success, disabled, pending, dirty, optimistic 상태를 기록한다.
- 클릭, 입력, submit, 취소, 재시도, focus 이동 흐름을 기록한다.

## API 계약과 Backend Dependency

- 확정된 request/response/error shape, pagination, sorting/filtering, backend 선행 작업을 기록한다.
- 미확정 API 계약과 이번 frontend 마일스톤에서 제외할 불확실성을 구분한다.

## 상태 소유권

- server state, client state, form state, URL state, derived state, global state를 분류한다.
- 상태 생성, 갱신, 초기화, 동기화 책임을 기록한다.

## Cache와 동기화 정책

- query key, stale time, invalidation, refetch, prefetch, optimistic update, pagination/infinite query 요구를 기록한다.
- 최신성 요구와 사용자에게 보여야 하는 stale/fresh 상태를 기록한다.

## Form과 Submit 정책

- validation 위치, schema, 중복 제출 방지, 저장 중 navigation guard, 실패 시 값 보존, 재시도 정책을 기록한다.
- partial submit 허용 여부와 submit 성공 후 이동/닫기 정책을 기록한다.

## Error/Loading/Empty/Success UX

- 사용자에게 보여야 하는 문구, toast, inline error, retry, fallback UI, error boundary 요구를 기록한다.
- 실패 복구 가능성과 사용자 행동으로 해결 가능한 범위를 기록한다.

## Responsive와 Accessibility 요구사항

- viewport별 layout, keyboard interaction, focus management, aria/semantic 요구를 기록한다.
- design-critical 예외나 접근성 완화가 있다면 사용자 또는 Source of Truth 근거를 기록한다.

## Design Source와 UI 제약

- Figma, 기존 design system, 기존 화면 관례, 문서화된 UI/UX 기준을 기록한다.
- 새 시각 규칙을 임의로 만들지 않고 확인된 design source만 사용한다.

## Rendering 성능 요구사항

- list size, virtualization, memoization, hydration, suspense, code splitting 등 구현 방식에 영향을 주는 요구를 기록한다.
- 명시 요구가 없으면 `없음`으로 쓰고 임의 목표를 만들지 않는다.

## 검증 기준

- 요구사항 충족 여부를 확인할 build/test/browser/visual/a11y 검증 기준을 기록한다.
- viewport, interaction, expected UI state, 접근성 확인 범위를 구분한다.

## 사용자 확인 필요 없음

- 코드베이스 관례로 처리해도 되는 구현 선택을 기록한다.
- 폴더 구조, naming, component/hook/query/store 배치, 공통 component 사용 방식처럼 저장소 관례로 충분히 결정 가능한 항목만 포함한다.

## 금지된 추론

- 아직 확정되지 않아 구현, 설계, 리뷰에 반영하면 안 되는 정책을 기록한다.
- 특히 제품 UX, navigation flow, API shape, cache freshness, invalidation, optimistic update, destructive action, submit/retry/cancel, form validation, 사용자 노출 문구는 사용자 또는 Source of Truth 없이 확정하지 않는다.

## 남은 미결정 사항

- 이번 마일스톤에서 제외하거나 사용자 확인이 필요한 항목을 기록한다.
- 구현을 차단하는 항목과 후속 마일스톤으로 넘길 수 있는 항목을 구분한다.
````

## 작성 규칙

- 빈 섹션은 `없음`으로 명시한다.
- 추론한 저장소 관례는 요구사항 섹션이 아니라 `사용자 확인 필요 없음`에 둔다.
- UX 정책, API 계약, 상태 소유권, cache/invalidation, 검증 기준은 가능한 한 구체적인 조건과 기대 결과로 작성한다.
- 기술 선택은 기록하지 않는다. 기술 판단에 필요한 제품·UX·API·상태·검증 제약만 기록한다.
- 설계 판단에 영향을 주는 미확정 정책은 `금지된 추론` 또는 `남은 미결정 사항`에 둔다.
- role input artifact에는 이 문서의 본문을 복사하지 않고 경로만 기록한다.
