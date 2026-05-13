# Frontend TDD 작성 흐름

## 목적

프론트엔드 기술설계문서를 작성할 때 어떤 순서로 범위, 근거, 설계 판단, 저장 결과를 만들지 정의한다.

## 적용 범위

이 문서는 작성 과정의 흐름을 소유한다. 최종 문서의 섹션 구조와 표 형식은 [frontend-tdd-template.md](frontend-tdd-template.md)가 소유한다.

## 전체 흐름

```text
1. 설계 대상 식별
2. 프로젝트 컨텍스트 수집
3. 사용자 흐름과 라우팅 설계
4. 폴더와 컴포넌트 구조 설계
5. 상태관리 구조 설계
6. API 연동 방식 설계
7. 캐싱 전략 설계
8. 에러 처리와 복구 전략 설계
9. 성능과 UX 고려사항 정리
10. 문서 저장과 문서 맵 갱신
```

## 1. 설계 대상 식별

스킬 호출 인수에서 설계 대상을 추출한다.

- 설계 대상 화면, 기능, 리팩토링 범위를 한 문장으로 고정한다.
- 신규 화면인지 기존 화면 변경인지 판별한다.
- 포함 범위와 제외 범위를 분리한다.
- route, 주요 사용자 흐름, API 계약, 상태 범위가 모호하면 질문한다.

## 2. 프로젝트 컨텍스트 수집

필요한 문서와 코드만 선별해 읽는다.

- `docs/frontend/README.md`
- `docs/frontend/getting-started.md`
- `docs/frontend/architecture/**`
- `docs/frontend/conventions/**`
- `docs/frontend/performance/**`
- `docs/frontend/ui-ux/**`
- 관련 frontend 코드의 route, page, widget, feature, entity, shared 경로
- 관련 API client, query key, cache invalidation, state store, form, validation, error boundary 코드

backend API 계약이 설계에 필요하면 확인된 API 문서나 타입만 사용한다. backend 구현은 추측하지 않는다.

## 3. 사용자 흐름과 라우팅 설계

사용자가 어떤 경로로 진입하고 어떤 화면 흐름을 거치는지 먼저 고정한다.

- route, page, layout, guard, redirect를 확인한다.
- URL state와 화면 상태가 어떻게 연결되는지 정리한다.
- 기존 route 변경이 있으면 backward compatibility와 deep link 영향을 확인한다.

## 4. 폴더와 컴포넌트 구조 설계

프로젝트의 frontend architecture 문서에 맞춰 파일 배치와 component 책임을 설계한다.

- 신규 파일과 변경 파일의 역할을 구분한다.
- component tree는 page, widget, feature, shared boundary를 드러내도록 작성한다.
- reusable component와 feature-specific component를 구분한다.
- public API, index export, import boundary를 명시한다.

## 5. 상태관리 구조 설계

상태를 종류별로 분류하고 소유 위치를 결정한다.

- server state: API 응답과 cache가 소유하는 상태
- client state: UI mode, modal, selection처럼 client가 소유하는 상태
- form state: 입력, validation, submit lifecycle
- URL state: filter, tab, pagination처럼 주소와 동기화되는 상태
- derived state: 기존 상태에서 계산되는 값

상태 흐름에는 생성, 갱신, 초기화, 동기화, unmount 시 처리를 포함한다.

## 6. API 연동 방식 설계

API 연동은 endpoint 목록이 아니라 사용자 경험과 cache 정책까지 포함해 설계한다.

- 확인된 API request/response type과 사용 위치를 정리한다.
- client 함수, query/mutation hook, type 위치를 명시한다.
- loading, empty, disabled, optimistic update 여부를 판단한다.
- API 계약이 불명확하면 `확인 필요`로 남기고 단정하지 않는다.

## 7. 캐싱 전략 설계

데이터 freshness와 사용자 경험 사이의 균형을 설계한다.

- query key와 invalidation 조건을 표로 정리한다.
- staleTime, gc/cacheTime, prefetch, background refresh 여부를 결정한다.
- mutation 이후 invalidate, setQueryData, optimistic update 중 무엇을 사용할지 판단한다.
- pagination 또는 infinite query가 있으면 cache shape과 merge 전략을 명시한다.

## 8. 에러 처리와 복구 전략 설계

에러는 사용자 피드백과 복구 가능성을 기준으로 분류한다.

- validation error, network/server error, permission error, empty result를 구분한다.
- toast, inline message, fallback UI, error boundary 중 적절한 피드백 방식을 선택한다.
- retry, rollback, disabled state, 재입력 유도 같은 복구 전략을 포함한다.

## 9. 성능과 UX 고려사항 정리

현재 요구 수준에 필요한 frontend 성능과 UX 판단을 정리한다.

- rendering 최적화, memoization, list virtualization 필요 여부를 확인한다.
- skeleton, perceived latency, disabled interaction, focus management를 검토한다.
- responsive layout과 accessibility 영향이 있으면 명시한다.

## 10. 문서 저장과 문서 맵 갱신

최종 문서는 `docs/frontend/design/tdd-{feature-slug}.md`에 저장한다.

- `{feature-slug}`는 설계 대상의 핵심을 2~4개 영문 kebab-case 단어로 축약한다.
- 관련 설계 문서가 이미 있으면 새 파일보다 기존 문서 갱신이 적절한지 판단한다.
- 새 문서를 만들면 `docs/frontend/design/README.md` 문서 맵을 갱신한다.
- 완료 전 [frontend-tdd-template.md](frontend-tdd-template.md)의 완료 기준을 확인한다.

## 검증

- 상태, API, component, routing, cache, error 판단이 서로 연결되는가
- 확인되지 않은 API나 framework를 단정하지 않았는가
- 사용자 흐름과 edge state가 정상 흐름만 다루지 않는가
- 저장 경로와 문서 맵이 일치하는가
