# Testing And Performance

## 목적

이 문서는 FSD 구조에서 어떤 단위를 테스트하고, 어떤 기준으로 성능 최적화를 적용할지 정의한다.

핵심 목표는 slice 경계가 테스트 경계가 되도록 만들고, 성능 최적화를 근거 없이 남발하지 않게 하는 것이다.

## 적용 범위

포함:

- slice 단위 테스트 기준
- feature/widget/entity 테스트 범위
- mock, MSW, integration test 기준
- React.memo, useMemo, useCallback 사용 기준
- virtualization, code splitting 기준

제외:

- 테스트 도구 설치법
- CI 파이프라인 세부 설정
- 성능 측정 도구 사용법의 상세 절차

## 테스트 전략

### 테스트 피라미드

우선순위:

1. Pure function/model 테스트
2. Hook/query/mutation 테스트
3. Component interaction 테스트
4. Slice integration 테스트
5. Route-level smoke 테스트

원칙:

- 테스트는 Public API 기준으로 작성한다.
- 내부 구현 테스트는 pure helper나 복잡한 model logic에만 제한한다.
- 레이어 경계를 깨는 mock은 피한다.

## Layer별 테스트 범위

### shared

대상:

- pure utility
- UI primitive accessibility
- API error normalization
- config parser

기준:

- 비즈니스 fixture를 사용하지 않는다.
- 외부 라이브러리 wrapper는 public behavior만 테스트한다.

### entities

대상:

- mapper
- query key factory
- entity guard/predicate
- entity UI 표시
- read query hook

기준:

- entity model의 canonical shape를 검증한다.
- API response DTO는 mapper 테스트에서만 다룬다.
- 다른 entity를 mock하지 않는다. 필요한 값은 ID나 primitive fixture로 둔다.

### features

대상:

- 사용자 액션 flow
- form validation
- mutation success/error handling
- optimistic update rollback
- permission-based disabled state

기준:

- feature는 독립 사용 가능한 action 단위로 테스트한다.
- CRUD endpoint 호출 여부보다 사용자 결과를 검증한다.
- query invalidation은 key factory 기준으로 검증한다.

### widgets

대상:

- 여러 feature/entity 조합
- section loading/empty/error 상태
- tab/filter/panel local interaction

기준:

- widget은 page/router 없이도 렌더링 가능해야 한다.
- widget 테스트에서 route navigation을 과하게 mock하지 않는다.
- 내부 feature의 세부 validation은 feature 테스트에 맡긴다.

### pages

대상:

- route params/search params 해석
- guard에 따른 렌더링
- major widget composition
- route-level lazy fallback smoke

기준:

- page 테스트는 얕고 넓게 유지한다.
- business action detail은 feature/widget 테스트로 내린다.

## Mock 전략

### 기본 원칙

- 네트워크는 MSW로 mock한다.
- module mock은 외부 boundary나 비싼 dependency에 제한한다.
- slice 내부 구현을 mock해 테스트가 구조를 고정하게 만들지 않는다.

### MSW 사용 기준

사용한다:

- query/mutation hook 테스트
- feature interaction 테스트
- widget integration 테스트
- page smoke 테스트

사용하지 않는다:

- pure function 테스트
- query key factory 테스트
- 단순 presentational component 테스트

Handler 위치:

```text
entities/{entity}/testing/{entity}.handlers.ts
features/{action}/testing/{action}.handlers.ts
shared/testing/server.ts
```

Fixture 기준:

- entity fixture는 entity `testing`이 소유한다.
- feature-specific scenario fixture는 feature `testing`이 소유한다.
- shared fixture는 비즈니스 의미가 없어야 한다.

## Integration Test 기준

integration test가 필요한 경우:

- feature가 form + mutation + toast + invalidation을 함께 수행한다.
- widget이 여러 entity query 상태를 조합한다.
- route guard와 page composition이 연결된다.
- regression 위험이 큰 workflow다.

integration test를 피할 경우:

- 단순 presentational component
- pure helper
- 단순 query key factory
- 라이브러리 기본 동작 재검증

## 성능 최적화 원칙

성능 최적화는 측정 가능한 문제나 구조적으로 명확한 비용이 있을 때 적용한다.

우선순위:

1. 불필요한 state ownership 제거
2. 큰 DOM 줄이기
3. 서버 데이터 중복 저장 제거
4. list virtualization
5. code splitting
6. memoization

## React.memo 기준

사용한다:

- props가 안정적이고 렌더 비용이 큰 component
- list item/card처럼 반복 렌더링되는 component
- parent state 변경과 무관하게 유지되어야 하는 subtree

사용하지 않는다:

- props가 매 렌더 새로 만들어지는 component
- 렌더 비용이 매우 작은 component
- memo 때문에 코드 이해가 어려워지는 경우

전제:

- callback과 object/array props가 안정적이어야 한다.
- memo 전후로 실제 렌더 감소가 예상되어야 한다.

## useMemo 기준

사용한다:

- 큰 list filter/sort/group
- Set/Map 생성 후 membership check가 반복됨
- expensive derived value
- memoized child에 전달하는 object/array props

사용하지 않는다:

- 단순 문자열/숫자 계산
- 의존성이 매번 바뀌는 계산
- side effect가 있는 로직

금지:

- derived state를 `useState + useEffect`로 동기화
- `useMemo` 안에서 mutation 수행

## useCallback 기준

사용한다:

- memoized child에 전달하는 handler
- dependency array에 안정적인 함수가 필요함
- event handler 생성이 list item 대량 렌더에 영향을 줌

사용하지 않는다:

- 일반 DOM element에만 전달되는 단순 handler
- dependency가 항상 바뀌어 안정성이 없는 handler
- 가독성만 떨어뜨리는 경우

## Virtualization 기준

사용한다:

- list row 100개 이상이 한 화면 또는 scroll container에 렌더링됨
- table row/cell이 복잡함
- tree/list expand 시 DOM이 급격히 증가함
- mobile에서 scroll jank가 발생함

대안:

- pagination
- server-side filtering
- collapsed group rendering
- detail modal로 분리

주의:

- virtualization은 accessibility와 keyboard navigation을 검토해야 한다.
- row height가 동적이면 구현 복잡도가 커진다.

## Code Splitting 기준

Route splitting:

- 모든 page는 lazy loading 대상이다.
- route fallback은 app/router에서 일관되게 제공한다.

Component splitting:

- editor, chart, rich table, calendar처럼 큰 dependency가 있을 때 적용한다.
- modal 내부 heavy content는 open 시점 lazy load를 검토한다.

금지:

- 작은 shared UI component를 과도하게 split
- feature 단위 split으로 chunk 수만 증가
- 사용 빈도가 높은 core UI의 lazy loading

## 렌더링 Anti-Patterns

- parent page가 모든 modal/form state를 보유해 큰 subtree가 매번 rerender
- hover 상태를 React state로 관리해 list item이 계속 rerender
- 큰 배경 위에 blur overlay를 걸고 잦은 state update 발생
- query data를 Zustand로 복사해 두 cache가 따로 갱신
- list item 내부에서 매 렌더 expensive sort/filter 수행
- memoized child에 inline object/function props 전달
- table/list 전체를 key 변경으로 강제 remount

## 성능 검토 체크리스트

- state를 가장 가까운 소유자에 두었는가?
- route/page state 변경이 큰 widget 전체를 다시 그리지 않는가?
- list DOM 크기가 제한되어 있는가?
- hover/focus 같은 transient 상태를 CSS로 처리할 수 있는가?
- skeleton/loading이 기존 content를 불필요하게 지우지 않는가?
- memoization보다 데이터 구조/소유권 개선을 먼저 했는가?
- virtualization이 필요한 row 수와 복잡도를 넘었는가?
- lazy loading이 사용자 체감과 chunk 전략에 도움이 되는가?
