# Folder Structure

## 목적

이 문서는 FSD 목표 구조를 실제 파일 배치, naming, barrel export 기준으로 변환한다.

현재 레거시 폴더를 설명하지 않고, 신규 기능과 리팩토링에서 도달해야 할 표준 구조를 정의한다.

## 적용 범위

포함:

- layer별 표준 폴더 구조
- slice와 segment 생성 기준
- file naming, component naming, hook naming
- Public API와 barrel export depth
- deep import 방지 기준

제외:

- layer 책임과 import 정책의 원칙 설명: [frontend-architecture](frontend-architecture.md)
- 상태와 query key 배치 기준: [state-management](state-management.md)

## 표준 구조

```text
src/
├── app/
│   ├── providers/
│   ├── router/
│   ├── styles/
│   └── index.tsx
│
├── pages/
│   └── {route-name}/
│       ├── ui/
│       ├── model/
│       └── index.ts
│
├── widgets/
│   └── {widget-name}/
│       ├── ui/
│       ├── model/
│       ├── config/
│       ├── testing/
│       └── index.ts
│
├── features/
│   └── {action-name}/
│       ├── ui/
│       ├── model/
│       ├── api/
│       ├── lib/
│       ├── testing/
│       └── index.ts
│
├── entities/
│   └── {entity-name}/
│       ├── ui/
│       ├── model/
│       ├── api/
│       ├── lib/
│       ├── testing/
│       └── index.ts
│
└── shared/
    ├── ui/
    ├── lib/
    ├── api/
    ├── config/
    ├── types/
    └── testing/
```

## Layer별 구조 기준

### app

```text
app/
├── providers/
│   ├── AppProviders.tsx
│   └── query-client.ts
├── router/
│   ├── AppRouter.tsx
│   ├── routeConfig.tsx
│   └── guards.tsx
├── styles/
│   └── globals.css
└── index.tsx
```

기준:

- 앱 초기화와 provider composition만 둔다.
- route별 화면 구현은 `pages`에 둔다.
- 업무 slice를 `app` 내부에 만들지 않는다.

### pages

```text
pages/
└── user-management/
    ├── ui/
    │   └── UserManagementPage.tsx
    ├── model/
    │   └── useUserManagementPageState.ts
    └── index.ts
```

기준:

- page slice 이름은 route 목적을 설명한다.
- page는 URL owner다.
- page 내부 `model`은 route params, filter draft, selected tab처럼 page boundary 상태만 소유한다.
- 복잡한 form/mutation은 feature로 내린다.

### widgets

```text
widgets/
└── organization-tree-panel/
    ├── ui/
    │   ├── OrganizationTreePanel.tsx
    │   └── OrganizationTreeToolbar.tsx
    ├── model/
    │   └── useOrganizationTreePanel.ts
    ├── config/
    │   └── treePanelConfig.ts
    └── index.ts
```

기준:

- widget 이름은 화면 영역 또는 section을 설명한다.
- widget은 여러 feature/entity를 조합할 수 있다.
- widget끼리 직접 import하지 않는다.
- layout shell은 widget이 아니라 shared/app layout 기준으로 판단한다.

### features

```text
features/
└── assign-department-leader/
    ├── ui/
    │   └── AssignDepartmentLeaderButton.tsx
    ├── model/
    │   ├── useAssignDepartmentLeaderMutation.ts
    │   └── assignDepartmentLeader.schema.ts
    ├── api/
    │   └── assignDepartmentLeaderApi.ts
    ├── testing/
    │   └── assignDepartmentLeader.handlers.ts
    └── index.ts
```

기준:

- feature 이름은 사용자 액션 동사로 시작한다.
- `create/update/delete` 같은 CRUD 기술어만으로 이름을 만들지 않는다.
- feature 하나는 독립적으로 사용 가능한 action boundary여야 한다.

### entities

```text
entities/
└── department/
    ├── ui/
    │   ├── DepartmentName.tsx
    │   └── DepartmentStatusBadge.tsx
    ├── model/
    │   ├── department.types.ts
    │   ├── department.mapper.ts
    │   └── departmentKeys.ts
    ├── api/
    │   └── departmentQueries.ts
    ├── lib/
    │   └── departmentGuards.ts
    └── index.ts
```

기준:

- entity 이름은 핵심 비즈니스 명사다.
- entity `ui`는 표시 컴포넌트만 허용한다.
- entity `model`은 타입, key, mapper, pure rule을 소유한다.
- entity가 다른 entity의 hook/ui/api를 import하지 않는다.

### shared

```text
shared/
├── ui/
│   ├── button/
│   │   ├── Button.tsx
│   │   └── index.ts
│   └── dialog/
│       ├── Dialog.tsx
│       └── index.ts
├── lib/
│   ├── cn.ts
│   └── formatDate.ts
├── api/
│   ├── httpClient.ts
│   └── apiError.ts
├── config/
│   └── env.ts
├── types/
│   └── utility.ts
└── testing/
    └── renderWithProviders.tsx
```

기준:

- shared는 업무 도메인을 알면 안 된다.
- shared UI는 primitive 또는 design-system level component만 둔다.
- `shared/api`는 endpoint가 아니라 transport를 소유한다.

## Segment 생성 기준

세그먼트는 역할이 필요할 때만 만든다.

생성한다:

- UI와 상태/hook이 분리되어야 한다.
- API transport와 model mapper가 분리되어야 한다.
- 테스트 fixture가 production 코드와 섞이면 가독성이 떨어진다.
- slice 내부 pure helper가 둘 이상의 파일에서 사용된다.

생성하지 않는다:

- 파일 하나를 담기 위해 폴더를 만든다.
- `components`, `hooks`, `utils`처럼 FSD 역할이 아닌 React 기술 단어로 나눈다.
- `common`, `misc`, `helpers`처럼 의미 없는 이름으로 모은다.

## Naming Convention

### Slice naming

| Layer | 규칙 | 예시 |
| --- | --- | --- |
| pages | route 목적, kebab-case | `approval-list`, `organization-settings` |
| widgets | 화면 section, kebab-case | `approval-board`, `organization-tree-panel` |
| features | 사용자 액션, verb-object | `submit-approval`, `assign-user-role` |
| entities | 비즈니스 명사, singular | `user`, `department`, `approval-document` |
| shared | 기술 역할 | `ui`, `lib`, `api`, `config` |

### File naming

| 대상 | 규칙 | 예시 |
| --- | --- | --- |
| React component | PascalCase | `DepartmentName.tsx` |
| hook | `use` prefix + Pascal/camel | `useDepartmentQuery.ts` |
| query key factory | `{entity}Keys.ts` | `departmentKeys.ts` |
| mutation hook | `use{Action}Mutation.ts` | `useAssignUserRoleMutation.ts` |
| mapper | `{domain}.mapper.ts` | `department.mapper.ts` |
| schema | `{action}.schema.ts` | `assignRole.schema.ts` |
| test | `{unit}.test.tsx` | `AssignRoleForm.test.tsx` |
| MSW handler | `{slice}.handlers.ts` | `department.handlers.ts` |

### Component naming

- Entity UI는 명사 중심: `UserAvatar`, `DepartmentName`
- Feature UI는 액션 중심: `AssignRoleForm`, `SubmitApprovalButton`
- Widget UI는 영역 중심: `ApprovalBoard`, `OrganizationTreePanel`
- Page UI는 `*Page` suffix를 사용한다.

### Hook naming

- Query hook: `useDepartmentDetailQuery`
- Mutation hook: `useAssignDepartmentLeaderMutation`
- UI state hook: `useOrganizationTreePanelState`
- Pure behavior hook: `useDebouncedValue`

## Public API와 Barrel Export

각 slice root의 `index.ts`는 외부 계약이다.

허용:

```ts
export { DepartmentName } from "./ui/DepartmentName"
export { useDepartmentDetailQuery } from "./api/departmentQueries"
export { departmentKeys } from "./model/departmentKeys"
export type { Department, DepartmentId } from "./model/department.types"
```

금지:

```ts
export * from "./ui"
export * from "./model"
export * from "./api"
```

Depth 제한:

- 외부 import는 slice root까지만 허용한다.
- 같은 slice 내부에서는 segment deep import를 허용한다.
- `index.ts`가 다른 `index.ts`를 연쇄로 export하는 depth는 1단계까지만 허용한다.

순환 참조 방지:

- `index.ts`에서 내부 파일이 다시 slice root를 import하지 않는다.
- public API에서 test fixture를 export하지 않는다.
- `shared/ui/index.ts`처럼 넓은 barrel은 순환 가능성을 점검한 뒤 제한적으로 사용한다.

## Import 예시

허용:

```ts
import { AssignDepartmentLeaderButton } from "@/features/assign-department-leader"
import { DepartmentName } from "@/entities/department"
import { Button } from "@/shared/ui/button"
```

금지:

```ts
import { AssignDepartmentLeaderButton } from "@/features/assign-department-leader/ui/AssignDepartmentLeaderButton"
import { useDepartmentDetailQuery } from "@/entities/department/api/departmentQueries"
import { UserAvatar } from "@/entities/user/ui/UserAvatar"
```

예외:

- 같은 slice 내부 파일끼리는 deep import를 허용한다.
- 테스트 파일은 테스트 대상 내부 구현을 검증해야 할 때만 제한적으로 deep import할 수 있다.

## 폴더 구조 검토 체크리스트

- slice 이름이 layer의 책임과 맞는가?
- segment가 역할 기준으로 나뉘었는가?
- `common`, `helpers`, `misc`, `components`, `hooks` 폴더가 늘어나지 않았는가?
- root `index.ts`가 최소 public API만 export하는가?
- 외부 import가 slice 내부 경로를 찌르지 않는가?
- entity/feature/widget/page 이름이 서로 다른 추상화 수준을 유지하는가?
