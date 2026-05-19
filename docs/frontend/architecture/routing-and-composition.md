# Routing And Composition

## 목적

이 문서는 FSD 구조에서 routing과 component composition의 책임 경계를 정의한다.

핵심 목표는 route ownership을 명확히 하고, page/widget/feature가 서로의 역할을 침범하지 않게 만드는 것이다.

## 적용 범위

포함:

- AppRouter 책임
- route ownership과 protected route 기준
- route 단위 lazy loading
- layout route 기준
- page, widget, layout component 차이
- children composition, compound component, render props, prop drilling 기준

제외:

- 폴더 구조와 naming 세부: [folder-structure](folder-structure.md)
- 상태 위치 판단: [state-management](state-management.md)

## Routing 책임

### AppRouter

책임:

- route tree 구성
- lazy page 연결
- layout route 연결
- global guard와 error boundary 연결
- fallback/loading boundary 배치

금지:

- page 내부 UI 구현
- page별 query/mutation orchestration
- feature action 직접 실행
- 업무 API 호출을 route 정의 안에 작성

### Page

책임:

- route params와 search params 해석
- page title, page-level layout, main widget composition
- 해당 URL에서 필요한 widget/feature/entity 조합

금지:

- 여러 route에서 재사용되는 큰 UI block 직접 구현
- 사용자 action mutation 로직 장기 보유
- app-level guard를 page마다 중복 구현

## Route Ownership

route는 `pages`가 소유한다.

기준:

- URL path 하나는 page slice 하나에 대응한다.
- 동일 page가 하위 route를 갖는 경우 page slice 안에서 route-specific composition을 분리할 수 있다.
- route params 타입과 search params parser는 page `model`이 소유한다.

예시:

```text
pages/
└── approval-detail/
    ├── model/
    │   ├── approvalDetailRoute.ts
    │   └── useApprovalDetailPage.ts
    ├── ui/
    │   └── ApprovalDetailPage.tsx
    └── index.ts
```

## Protected Route 기준

protected route는 app/router에서 선언하고, permission 해석은 인증/권한 slice의 public API를 사용한다.

허용:

- 로그인 필요 여부
- 권한 code 기반 접근 제한
- 인증 만료 시 redirect
- layout route 단위 guard

금지:

- page 내부에서 모든 protected logic을 반복
- feature 내부에서 route redirect를 직접 수행
- API interceptor와 route guard가 서로 다른 기준으로 인증 만료를 판단

기준:

- 인증 여부는 app-level guard가 먼저 처리한다.
- 세부 권한은 route metadata로 선언한다.
- guard는 UI를 그리기 전에 접근 가능성을 결정한다.

## Route Lazy Loading

원칙:

- page는 route 단위로 lazy loading한다.
- 무거운 widget이나 editor는 widget 내부에서 추가 lazy loading할 수 있다.
- feature 단위 lazy loading은 chunk가 충분히 크거나 사용 빈도가 낮을 때만 적용한다.

권장:

```ts
const ApprovalDetailPage = lazy(() => import("@/pages/approval-detail"))
```

주의:

- shared primitive를 lazy loading하지 않는다.
- 작은 feature를 과도하게 split하지 않는다.
- route fallback은 app/router 또는 layout route에서 일관되게 제공한다.

## Layout Route 기준

layout route는 반복되는 화면 frame을 소유한다.

허용:

- sidebar/header/footer shell
- 인증된 사용자 영역 layout
- public auth layout
- route outlet

금지:

- 특정 page의 table/filter/form 상태
- 특정 feature action 버튼 orchestration
- page별 API 호출

Layout component와 widget 차이:

- layout component는 화면 frame과 outlet 배치를 소유한다.
- widget은 특정 업무 section을 소유한다.
- layout은 업무 도메인을 몰라야 한다.

## Page, Widget, Feature Composition

권장 흐름:

```text
Page
  -> Widget
      -> Feature
      -> Entity UI
      -> Shared UI
```

Page는 조합한다:

```tsx
export function OrganizationSettingsPage() {
  return (
    <PageLayout>
      <OrganizationTreePanel />
      <DepartmentPermissionPanel />
    </PageLayout>
  )
}
```

Widget은 업무 section을 완성한다:

```tsx
export function OrganizationTreePanel() {
  return (
    <section>
      <OrganizationTree />
      <CreateDepartmentButton />
    </section>
  )
}
```

Feature는 action을 완성한다:

```tsx
export function AssignDepartmentLeaderButton({ departmentId }: Props) {
  const mutation = useAssignDepartmentLeaderMutation()
  return <Button onClick={() => mutation.mutate({ departmentId })}>리더 지정</Button>
}
```

## Composition 원칙

### children 우선

단순한 slot 조합은 children을 우선한다.

```tsx
<Panel title="부서">
  <DepartmentTree />
</Panel>
```

사용 기준:

- 부모가 layout만 제공한다.
- 자식의 데이터 요구사항을 부모가 몰라도 된다.
- prop 수가 줄고 의존 방향이 단순해진다.

### Compound Component

관련 UI 조각이 같은 상태/문맥을 공유할 때 사용한다.

```tsx
<DataTable>
  <DataTable.Toolbar />
  <DataTable.Content />
  <DataTable.Pagination />
</DataTable>
```

사용 기준:

- 하나의 UI primitive 또는 widget 내부에서 문맥이 강하게 묶인다.
- 외부 사용자는 조합 순서를 제어해야 한다.
- 내부 context가 prop drilling을 줄인다.

주의:

- compound component를 feature orchestration 숨김 용도로 쓰지 않는다.
- 여러 업무 slice를 compound component 하나에 묶지 않는다.

### Render Props

상태나 계산 결과를 caller가 렌더링해야 할 때 제한적으로 사용한다.

사용 기준:

- hook만으로는 제어권 전달이 어렵다.
- UI customization이 핵심 요구사항이다.
- children composition보다 명확하다.

주의:

- render props가 깊어지면 가독성이 떨어진다.
- 대부분은 custom hook + children composition으로 대체 가능하다.

### Prop Drilling

허용:

- 1~2단계 props 전달
- 단순 callback 전달
- page -> widget -> feature 정도의 명확한 조합

개선 필요:

- 3단계 이상 같은 props 반복
- unrelated component가 같은 state를 필요로 함
- props가 route/page를 넘어 재사용됨

대안:

- children composition
- slice local context
- React Query hook을 필요한 위치에서 직접 사용
- Zustand는 unrelated slice 전역 공유가 필요할 때만 사용

## Anti-Patterns

- AppRouter에 업무 API 호출 작성
- page가 모든 widget/feature 내부 상태를 직접 제어
- layout component가 특정 entity를 알고 있음
- widget이 route navigation ownership을 가짐
- feature가 `navigate()`를 직접 호출해 route policy를 숨김
- compound component로 거대한 업무 화면을 감춤
- prop drilling을 피하려고 모든 값을 Zustand에 저장

## 검토 체크리스트

- URL ownership은 page에 있는가?
- AppRouter는 route tree와 guard만 소유하는가?
- protected route 기준이 route metadata로 표현되는가?
- page가 widget/feature를 조합하는 수준에 머무르는가?
- widget은 URL을 모르고 section만 완성하는가?
- feature는 사용자 액션 단위로 독립 사용 가능한가?
- children composition으로 해결할 수 있는 문제를 전역 상태로 풀지 않았는가?
