# Frontend Architecture

## 목적

이 문서는 프론트엔드 코드의 최상위 구조를 **Feature-Sliced Design(FSD)** 기준으로 정의한다.

핵심 목표는 "어디에 어떤 코드를 둘 것인가", "무엇을 import할 수 있는가", "언제 slice를 분리할 것인가"를 일관되게 판단하게 만드는 것이다.

## 적용 범위

포함:

- FSD layer 책임과 금지 책임
- slice 설계 기준
- segment 사용 원칙
- Public API와 cross import 규칙
- shared 남용 방지 기준
- entity, feature, widget, page 경계

제외:

- 구체적인 파일명과 폴더 예시: [folder-structure](folder-structure.md)
- 상태 관리와 React Query/Zustand 기준: [state-management](state-management.md)
- routing과 composition 기준: [routing-and-composition](routing-and-composition.md)
- error/loading/testing/performance 세부 전략: [runtime-strategies](runtime-strategies.md), [testing-and-performance](testing-and-performance.md)

## 전체 구조

FSD layer는 위에서 아래로만 의존한다.

```text
app
pages
widgets
features
entities
shared
```

허용 의존 방향:

```text
app       -> pages, widgets, features, entities, shared
pages     -> widgets, features, entities, shared
widgets   -> features, entities, shared
features  -> entities, shared
entities  -> shared
shared    -> 외부 라이브러리와 자기 내부만
```

기본 원칙:

- 상위 layer는 하위 layer를 조합한다.
- 하위 layer는 상위 layer의 존재를 모른다.
- 같은 layer의 다른 slice를 직접 import하지 않는다.
- slice 외부에서는 해당 slice의 Public API만 import한다.

## Layer 책임

### app

책임:

- 애플리케이션 부트스트랩
- Router, QueryClient, 전역 provider, 전역 error boundary 구성
- 전역 스타일, 환경 설정, feature flag, 앱 초기화

허용:

- `pages` route 등록
- provider composition
- 앱 단위 guard와 layout route 연결

금지:

- 화면별 비즈니스 로직
- 특정 entity의 CRUD 처리
- feature 내부 hook 직접 구현
- widget/page에서 해결 가능한 UI 상태 보관

상태/API 기준:

- 앱 생명주기와 관련된 전역 설정 상태만 허용한다.
- 서버 데이터 조회는 원칙적으로 금지한다. 예외는 앱 초기화에 반드시 필요한 bootstrap query다.

안티패턴:

- `app`에 모든 route loader와 API 호출을 모으는 구조
- `app` provider가 특정 업무 도메인을 알고 있는 구조

### pages

책임:

- URL에 매핑되는 화면 단위 composition
- route params, search params, navigation intent 해석
- page-level layout과 data boundary 배치

허용:

- widgets/features/entities 조합
- route 단위 lazy loading
- page 전용 local UI state
- page 단위 permission guard 연결

금지:

- 재사용 가능한 업무 기능 직접 구현
- entity mutation orchestration을 page에 장기간 방치
- 공통 widget으로 분리 가능한 큰 UI 블록 누적
- 여러 페이지가 공유하는 business rule 보유

상태/API 기준:

- route params에서 파생되는 UI 상태는 허용한다.
- 서버 데이터는 page가 직접 호출하기보다 widget/feature/entity hook을 조합한다.
- 페이지 하나에서만 쓰는 단순 query 조합은 허용하되, 두 번째 사용처가 생기면 slice로 내린다.

안티패턴:

- `pages/*/index.tsx`가 form validation, API mutation, table transform, modal state를 모두 보유하는 구조
- page가 사실상 giant widget이 되는 구조

### widgets

책임:

- 페이지의 독립적인 큰 화면 블록 구성
- 여러 feature와 entity UI를 조합해 업무 문맥을 가진 section 제공
- page보다 작고 feature보다 큰 composition 단위 제공

허용:

- 복수 feature 조합
- entity 목록/상세 UI 조합
- widget 내부 local state
- widget 전용 query 조합

금지:

- 사용자 액션의 핵심 mutation rule을 직접 소유
- URL ownership 보유
- 다른 widget 직접 import
- 모든 화면을 하나의 widget에 몰아넣기

상태/API 기준:

- widget 내부 표시 상태, 탭, 필터 초안, 열림 상태는 허용한다.
- 서버 상태는 entity query와 feature mutation을 조합한다.
- widget 전용 aggregate query가 필요하면 `model`에 두되 재사용되면 entity/feature로 내린다.

Widget과 page 차이:

- page는 URL과 navigation boundary를 소유한다.
- widget은 URL을 소유하지 않고 page 내부 section을 소유한다.

Widget과 feature 차이:

- widget은 화면 블록이다.
- feature는 사용자 액션이다.

안티패턴:

- giant widget: 페이지 대부분의 상태·API·mutation·form을 한 widget이 보유
- layout component를 widget으로 둔갑시키기

### features

책임:

- 사용자가 수행하는 독립적인 액션 단위
- 업무 규칙이 포함된 command, mutation, form, interaction 제공
- widgets/pages에서 재사용 가능한 행위 제공

허용:

- 사용자 액션 중심 UI: `login`, `approve-request`, `assign-user-role`
- mutation hook과 command orchestration
- action-specific form validation
- feature 내부에서 필요한 entity query 조합

금지:

- CRUD 명사 단위로 feature 만들기
- 다른 feature 직접 import
- page route ownership 보유
- entity의 공통 모델을 feature 내부에 숨기기

상태/API 기준:

- mutation 상태, form 상태, optimistic update context는 허용한다.
- 서버 조회는 액션 수행에 필요한 최소 범위만 허용한다.
- feature가 여러 entity를 조합할 수 있지만, 공통 entity rule을 소유하면 안 된다.

Feature 생성 기준:

- 사용자 관점에서 독립적인 행위 이름으로 설명된다.
- 여러 화면에서 재사용될 가능성이 있거나 page/widget을 단순화한다.
- mutation, validation, permission, side effect 중 하나 이상을 포함한다.
- 단순 버튼/표시 컴포넌트가 아니라 행동을 완결한다.

CRUD 기준 금지:

- `user-create`, `user-update`, `user-delete`를 기계적으로 만들지 않는다.
- 업무 언어로 `invite-user`, `change-user-status`, `assign-user-role`처럼 만든다.

안티패턴:

- feature가 다른 feature를 호출해 workflow를 숨기는 구조
- feature가 entity model을 자체 복제하는 구조

### entities

책임:

- 비즈니스 핵심 개념의 모델, 식별자, query, 표시용 최소 UI
- 여러 feature/widget/page에서 공유되는 도메인 데이터 기준

허용:

- entity type, schema, mapper
- entity query key와 read query
- entity 전용 pure helper
- entity를 표현하는 작은 UI: avatar, name cell, status badge

금지:

- 사용자 액션 mutation의 업무 절차
- page/widget composition
- 특정 화면 전용 view model
- 다른 entity의 내부 구현 deep import

상태/API 기준:

- read query와 cache key는 entity가 소유한다.
- mutation은 원칙적으로 feature가 소유한다. 단, entity 자체의 범용 mutation이 제품 전반에서 동일하게 쓰이면 entity에 둘 수 있다.
- entity UI는 표시 중심이어야 하며 API 호출을 직접 수행하지 않는다.

Entity 승격 기준:

- 동일한 도메인 데이터가 두 개 이상의 feature/widget/page에서 필요하다.
- id, name, status, permission 같은 공통 모델 해석이 반복된다.
- query key와 조회 캐시를 하나의 기준으로 묶어야 한다.

Entity 간 의존:

- 기본적으로 entity 간 직접 의존은 금지한다.
- ID 참조 타입은 허용한다.
- 복수 entity를 결합한 view는 widget 또는 feature에서 조합한다.

### shared

책임:

- 비즈니스 의미가 없는 범용 기술 자산
- UI primitive, low-level lib, 공통 config, 공통 type utility

허용:

- Button, Dialog, Input 같은 design primitive
- HTTP client, date formatter, storage wrapper
- 범용 hook: debounce, media query, intersection observer
- 환경 변수, route path builder의 기술적 기반

금지:

- 업무 도메인 단어 포함 코드
- 특정 entity/feature를 아는 helper
- "여러 곳에서 쓰일 수도 있음"만으로 올린 코드
- 비즈니스 validation, permission rule, API endpoint 묶음

상태/API 기준:

- shared store는 원칙적으로 금지한다.
- HTTP client 같은 transport만 허용하고, 업무 API 함수는 entity/feature가 소유한다.

Shared 승격 기준:

- 최소 두 개 이상의 서로 다른 slice에서 실제 중복이 발생했다.
- 비즈니스 용어 없이 설명 가능하다.
- 하위 의존이 없고 독립 테스트가 가능하다.
- shared로 올려도 도메인 변경 이유로 수정될 가능성이 낮다.

안티패턴:

- `shared/utils/business.ts`
- `shared/hooks/useUserList`
- `shared/constants/permissions`
- `shared/components/DepartmentSelect`

## Slice 설계 기준

Slice는 layer 내부의 업무 단위다.

좋은 slice 조건:

- 이름만 보고 책임이 예측된다.
- 외부로 노출하는 API가 작다.
- 내부 변경이 같은 layer의 다른 slice에 전파되지 않는다.
- 테스트를 slice 단위로 작성할 수 있다.

분리 기준:

- 책임이 다른 변경 이유가 생겼다.
- 같은 파일 안에서 상태, API, UI가 서로 다른 업무 흐름을 가진다.
- 두 개 이상의 page/widget에서 재사용된다.
- 독립 배포 또는 독립 테스트 단위로 설명 가능하다.

분리하지 않는 기준:

- 코드 줄 수만 많고 변경 이유가 하나다.
- 단순 스타일 차이만 있다.
- 한 화면의 사소한 하위 컴포넌트다.
- 추상화 이름이 업무 언어보다 모호하다.

Slice 크기 기준:

- slice root의 Public API가 5~7개 export를 넘으면 책임 분리를 검토한다.
- `ui` 컴포넌트가 서로 다른 사용자 액션을 다수 포함하면 feature 분리를 검토한다.
- `model`이 여러 서버 자원과 mutation을 동시에 orchestrate하면 widget/page 재구성을 검토한다.

재사용 기준:

- "재사용 가능할 것 같다"는 분리 근거가 아니다.
- 두 번째 실제 사용처가 생기면 공통화를 검토한다.
- 세 번째 사용처가 생기면 slice/public API 안정화를 우선한다.

## Segment 활용 원칙

Segment는 slice 내부의 기술 역할 단위다. 모든 slice가 모든 segment를 가질 필요는 없다.

공식 segment:

- `ui`: React component, view-only component, style binding
- `model`: state, hook, query/mutation orchestration, business-facing adapter
- `api`: transport function, repository/client call, DTO mapper
- `lib`: slice 전용 pure helper
- `config`: slice 전용 상수와 설정
- `types`: 외부 라이브러리와 분리된 타입 보조 파일
- `testing`: slice 테스트 fixture, builder, MSW handler

Layer별 차이:

- `entities`: `model`, `api`, `ui`, `lib`, `testing` 중심
- `features`: `ui`, `model`, `api`, `lib`, `testing` 중심
- `widgets`: `ui`, `model`, `config`, `testing` 중심
- `pages`: `ui`, `model` 정도만 허용하고 복잡해지면 하위 layer로 내린다.
- `shared`: `ui`, `lib`, `api`, `config`, `types`를 사용할 수 있지만 업무 의미를 담지 않는다.

생성 기준:

- 같은 slice 안에서 기술 역할이 두 개 이상 뚜렷하게 분리된다.
- 테스트와 import boundary가 명확해진다.
- 세그먼트 이름이 역할을 설명한다.

과분할 금지:

- 파일 1~2개뿐이고 역할이 단순하면 segment를 만들지 않는다.
- `hooks`, `components`, `utils`처럼 프레임워크 중심 이름을 남발하지 않는다.
- `common`, `misc`, `helpers`, `services`는 의미가 흐려지므로 금지한다.

금지 segment:

- `common`
- `shared` inside slice
- `helpers`
- `misc`
- `components`
- `containers`
- `store` 단독 segment

## Public API 규칙

모든 slice는 외부 사용자가 import할 수 있는 최소 표면만 `index.ts`로 공개한다.

원칙:

- 외부에서 필요한 component/hook/type만 export한다.
- 내부 구현 파일 경로를 외부에서 import하지 않는다.
- export는 명시적으로 작성한다.
- Public API는 안정적인 계약으로 취급한다.

허용:

```ts
export { UserAvatar } from "./ui/UserAvatar"
export { useUserDetailQuery } from "./model/useUserDetailQuery"
export type { User, UserId } from "./model/types"
```

금지:

```ts
export * from "./ui"
export * from "./model"
export * from "./api"
```

Wildcard export 기준:

- slice root의 wildcard export는 금지한다.
- shared primitive 묶음처럼 순환 가능성이 낮고 외부 계약이 명확한 경우에만 제한적으로 허용한다.
- 테스트 fixture export에는 사용할 수 있지만 production public API와 분리한다.

내부 타입 노출 기준:

- 외부 layer가 props나 hook return type으로 알아야 하는 타입만 export한다.
- DTO, form internal state, mapper intermediate type은 export하지 않는다.
- 서버 응답 타입을 그대로 외부 계약으로 노출하지 않는다. entity model로 변환한다.

## Cross Import 규칙

기본 규칙:

- 상위 layer -> 하위 layer import만 허용한다.
- 같은 layer의 다른 slice import는 금지한다.
- slice 내부 deep import는 같은 slice 내부에서만 허용한다.

같은 layer slice 간 import:

- `features/a` -> `features/b`: 금지
- `widgets/a` -> `widgets/b`: 금지
- `entities/a` -> `entities/b`: 원칙적으로 금지

entities 간 참조:

- ID 타입이나 primitive 참조는 허용한다.
- entity A가 entity B의 UI/hook/api를 직접 import하는 것은 금지한다.
- 결합 view는 widget이나 feature에서 만든다.

features 간 참조:

- 직접 참조 금지.
- 두 feature가 협력해야 하면 상위 widget/page에서 orchestrate한다.
- 공통 action rule이 있다면 entity나 shared가 아니라 별도 feature 재설계를 검토한다.

shared 내부 규칙:

- `shared/ui`는 `shared/lib`, `shared/config` 정도만 참조한다.
- `shared/lib`는 React와 UI에 의존하지 않는 pure utility를 우선한다.
- `shared/api`는 transport client만 소유하고 업무 endpoint를 소유하지 않는다.
- shared 내부에서도 순환 import는 금지한다.

## Anti-Patterns

금지 또는 강한 경고 대상:

- shared 남용: 업무 의미가 있는 코드를 shared로 올림
- giant widget: 화면 전체 로직을 하나의 widget에 집중
- feature 간 직접 참조
- slice Public API를 우회하는 deep import
- derived state 저장
- query data를 Zustand로 복사
- UI component 내부에서 API 호출 남발
- CRUD 이름만으로 feature 생성
- `common`, `helpers`, `misc` 폴더 증가
- page가 모든 form/mutation/toast/navigation 로직을 직접 보유
- entity UI가 mutation과 side effect를 실행

## 검토 체크리스트

- 이 코드는 현재 layer보다 낮은 layer로 내려갈 수 있는가?
- 이 코드는 현재 layer보다 높은 layer를 알고 있지 않은가?
- slice 이름이 업무 언어로 설명되는가?
- 외부 import가 Public API를 통하는가?
- shared에 비즈니스 단어가 들어가지 않았는가?
- query data를 다른 store로 복사하지 않았는가?
- feature가 사용자 액션 단위인가?
- widget이 URL이나 route ownership을 갖고 있지 않은가?
