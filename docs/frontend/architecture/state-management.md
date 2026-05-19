# State Management

## 목적

이 문서는 FSD 구조 안에서 상태를 어디에 두고, 서버 캐시를 어떻게 관리하며, mutation 후 화면을 어떻게 갱신할지 정의한다.

핵심 원칙은 **서버 상태는 React Query, 전역 클라이언트 상태는 Zustand, 단기 UI 상태는 local state**로 분리하는 것이다.

## 적용 범위

포함:

- layer별 상태 위치 기준
- React Query 위치와 query key 전략
- Zustand 사용 기준
- local state와 derived state 기준
- mutation, invalidation, optimistic update, rollback 기준

제외:

- error/loading UI 표현 기준: [runtime-strategies](runtime-strategies.md)
- 성능 최적화의 memoization 기준: [testing-and-performance](testing-and-performance.md)

## 상태 분류

| 분류 | 소유 도구 | 예시 | 위치 |
| --- | --- | --- | --- |
| 서버 상태 | React Query | 사용자 목록, 부서 상세, 결재 문서 | `entities/*/api`, `features/*/model` |
| 전역 클라이언트 상태 | Zustand | 인증 세션, 테마, 사이드바 열림 | `app` 또는 제한된 `shared/config`/전용 slice |
| route 상태 | Router/search params | page, tab, filter query string | `pages/*/model` |
| local UI 상태 | `useState`, `useReducer` | modal open, focused item, selected row draft | 해당 컴포넌트 또는 가까운 부모 |
| form 상태 | form library 또는 local state | 입력값, validation error | `features/*/model` 또는 form component |
| derived state | 변수 또는 `useMemo` | count, filtered list, disabled 여부 | 저장하지 않음 |

## Layer별 상태 기준

### app

허용:

- provider 초기화 상태
- 인증 세션 복원 상태
- feature flag, theme, locale 같은 앱 전역 설정

금지:

- 특정 화면의 filter, modal, selected row
- 업무 entity 목록을 전역 store에 저장
- React Query data를 Zustand로 복사

### pages

허용:

- route params/search params 해석
- page-level tab, filter draft, selected id
- page composition에 필요한 local state

금지:

- 재사용 가능한 action state
- 공통 entity cache
- 복잡한 mutation orchestration

기준:

- URL로 복원되어야 하는 값은 search params에 둔다.
- URL과 무관한 단기 UI 상태는 local state로 둔다.

### widgets

허용:

- section 내부 표시 상태
- table column visibility, local sorting draft, panel open state
- 여러 feature/entity를 조합하는 view model

금지:

- widget 외부에서도 필요한 global state를 숨김
- feature mutation 결과를 자체 store에 복사

### features

허용:

- action form state
- mutation state
- optimistic update context
- 액션 수행에 필요한 짧은 lived state

금지:

- read model cache를 feature local store에 장기 보관
- 여러 feature가 공유해야 하는 entity model 소유

### entities

허용:

- entity query key
- read query hook
- entity model mapper
- entity display helper

금지:

- 사용자 액션별 mutation workflow
- 화면 전용 filter draft
- 다른 entity의 cache 직접 수정

### shared

허용:

- 상태 도구의 기술적 adapter
- storage wrapper
- 범용 event bus는 매우 제한적으로 허용

금지:

- 업무 store
- entity/feature 이름이 들어간 store
- 서버 상태 cache 대체 store

## React Query 위치 기준

기본 위치:

- entity read query: `entities/{entity}/api`
- entity query key: `entities/{entity}/model`
- feature mutation: `features/{action}/model`
- feature 전용 API call: `features/{action}/api`
- app bootstrap query: `app/providers` 또는 `app/model`

Entity query 예시:

```ts
// entities/department/model/departmentKeys.ts
export const departmentKeys = {
  all: ["department"] as const,
  lists: () => [...departmentKeys.all, "list"] as const,
  list: (params: DepartmentListParams) => [...departmentKeys.lists(), params] as const,
  details: () => [...departmentKeys.all, "detail"] as const,
  detail: (id: DepartmentId) => [...departmentKeys.details(), id] as const,
}
```

```ts
// entities/department/api/useDepartmentDetailQuery.ts
export function useDepartmentDetailQuery(id: DepartmentId) {
  return useQuery({
    queryKey: departmentKeys.detail(id),
    queryFn: () => departmentApi.getDetail(id),
  })
}
```

Feature mutation 예시:

```ts
// features/assign-department-leader/model/useAssignDepartmentLeaderMutation.ts
export function useAssignDepartmentLeaderMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: assignDepartmentLeaderApi,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: departmentKeys.detail(variables.departmentId) })
      queryClient.invalidateQueries({ queryKey: departmentKeys.lists() })
    },
  })
}
```

## Query Key 전략

원칙:

- query key는 entity 기준으로 grouping한다.
- key factory는 entity `model`이 소유한다.
- 문자열 literal을 컴포넌트에 직접 흩뿌리지 않는다.
- 목록, 상세, 검색, 통계 key를 계층적으로 둔다.

Naming:

- root key는 entity singular: `["department"]`
- list group: `lists()`
- specific list: `list(params)`
- detail group: `details()`
- specific detail: `detail(id)`
- aggregate/stat: `stats(params)` 또는 `summary(params)`

금지:

```ts
useQuery({ queryKey: ["department-list"], queryFn: ... })
useQuery({ queryKey: ["getDepartment", id], queryFn: ... })
```

허용:

```ts
useQuery({ queryKey: departmentKeys.detail(id), queryFn: ... })
```

Invalidation 범위:

- 생성: list group invalidation
- 수정: detail + 관련 list invalidation
- 삭제: detail remove 또는 invalidate + list invalidation
- 순서 변경: affected list invalidation
- 권한/인증 변경: session 또는 permission 관련 root invalidation

## Mutation 전략

기본 원칙:

- mutation 후에는 invalidation을 우선한다.
- cache 직접 수정은 즉각적인 UX가 중요하거나 서버 응답이 충분히 신뢰 가능한 경우만 허용한다.
- optimistic update는 rollback을 반드시 구현한다.

Invalidation 우선:

```ts
onSuccess: (_, variables) => {
  queryClient.invalidateQueries({ queryKey: departmentKeys.detail(variables.id) })
  queryClient.invalidateQueries({ queryKey: departmentKeys.lists() })
}
```

Cache 직접 수정 허용 기준:

- 단일 entity detail 갱신처럼 영향 범위가 명확하다.
- 서버 응답이 최신 canonical model이다.
- list ordering, permission, aggregate count에 영향을 주지 않는다.

Optimistic update 허용 기준:

- 토글, 즐겨찾기, 단일 필드 변경처럼 실패 시 복구가 단순하다.
- 사용자 체감 latency가 중요하다.
- 실패하면 이전 snapshot으로 복구할 수 있다.

Optimistic update 금지 또는 주의:

- 결재 승인, 결제, 재고, 권한 변경처럼 업무 영향이 큰 mutation
- 서버에서 복잡한 cascade가 발생하는 mutation
- 목록 정렬과 count가 복잡하게 바뀌는 mutation

Rollback 기본 구조:

```ts
onMutate: async (variables) => {
  await queryClient.cancelQueries({ queryKey: departmentKeys.detail(variables.id) })
  const previous = queryClient.getQueryData(departmentKeys.detail(variables.id))

  queryClient.setQueryData(departmentKeys.detail(variables.id), draft => ({
    ...draft,
    name: variables.name,
  }))

  return { previous }
},
onError: (_, variables, context) => {
  queryClient.setQueryData(departmentKeys.detail(variables.id), context?.previous)
},
onSettled: (_, __, variables) => {
  queryClient.invalidateQueries({ queryKey: departmentKeys.detail(variables.id) })
}
```

## Zustand 사용 기준

Zustand는 서버 상태 캐시가 아니라 전역 클라이언트 상태 저장소다.

허용:

- 인증 세션과 client-side auth 상태
- theme, layout preference, sidebar open
- 앱 전체에서 공유되는 ephemeral UI preference

금지:

- React Query data 복사
- entity list/detail 보관
- form state 전역화
- mutation 결과를 store에 저장하고 query invalidation 생략

Store 위치:

- 앱 전역 store: `app/model` 또는 `app/providers` 주변
- 순수 기술 preference: `shared/config` 또는 별도 app-level store
- 업무 slice 전용 store: 해당 feature/widget `model`

Store 설계:

- store는 작게 유지한다.
- action 이름은 업무 의도를 드러낸다.
- persist는 필요한 state만 whitelist한다.
- 서버 동기화가 필요한 값은 persist하지 않는다.

## Local State 기준

local state를 우선한다:

- 한 컴포넌트 또는 가까운 하위 트리에서만 사용한다.
- URL 복원이 필요 없다.
- 서버와 동기화할 필요가 없다.
- 닫히면 사라져도 되는 값이다.

가까운 부모로 올린다:

- sibling 컴포넌트 둘 이상이 같은 값을 사용한다.
- children composition으로 전달 가능하다.

전역으로 올리지 않는다:

- props drilling을 피하고 싶다는 이유만으로는 부족하다.
- 2단계 전달은 허용한다.
- 3단계 이상이면 composition 또는 slice 재설계를 먼저 검토한다.

## Derived State 금지

저장하지 않는다:

- `items.length`
- `selectedIds.includes(id)`
- `query.data`에서 계산 가능한 filtered list
- props에서 계산 가능한 disabled 여부

허용 방식:

```ts
const selectedIdSet = useMemo(() => new Set(selectedIds), [selectedIds])
const visibleItems = useMemo(() => filterItems(items, filters), [items, filters])
const isSubmitDisabled = !form.name || mutation.isPending
```

금지 방식:

```ts
const [count, setCount] = useState(0)
useEffect(() => setCount(items.length), [items])
```

## Form State 기준

단순 form:

- 필드 1~3개
- validation 단순
- submit side effect 단순
- local state 허용

복잡한 form:

- 필드 4개 이상
- nested field 또는 conditional field
- 서버 validation error mapping 필요
- React Hook Form + schema validation 권장

위치:

- 사용자 action form은 feature `model/ui`가 소유한다.
- page 전용 filter form은 page 또는 widget `model`이 소유한다.
- entity는 form state를 소유하지 않는다.

## 검토 체크리스트

- 이 값은 서버 canonical data인가? 그렇다면 React Query에 둔다.
- 이 값은 URL로 복원되어야 하는가? 그렇다면 route/search params를 우선한다.
- 이 값은 닫히면 사라져도 되는가? 그렇다면 local state다.
- 이 값은 여러 unrelated slice에서 필요한가? 그렇다면 Zustand를 검토한다.
- derived state를 저장하고 있지 않은가?
- query data를 Zustand로 복사하지 않았는가?
- mutation 후 cache 갱신 범위가 query key factory로 표현되는가?
- optimistic update에는 rollback이 있는가?
