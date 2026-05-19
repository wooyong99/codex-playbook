# Runtime Strategies

## 목적

이 문서는 UI 실행 시점에 필요한 비즈니스 로직 위치, API 실패 처리, 인증 만료 처리, toast, form error, loading/skeleton/empty/retry 전략을 정의한다.

핵심 목표는 component 내부에 업무 로직과 side effect가 과도하게 쌓이지 않도록 역할을 분리하는 것이다.

## 적용 범위

포함:

- 비즈니스 로직 위치 기준
- component, hook, service/api 역할 구분
- global error boundary
- API error 처리 기준
- 인증 만료 처리
- toast 표시 기준
- form error 처리 기준
- loading, skeleton, empty state, retry 정책

제외:

- React Query key/mutation cache 전략: [state-management](state-management.md)
- UI 디자인 세부 표현: `docs/frontend/ui-ux`

## 비즈니스 로직 위치 기준

### Component

책임:

- props와 hook 결과를 UI로 표현
- 사용자 이벤트를 feature/model hook에 전달
- 간단한 표시용 계산

허용:

- `isDisabled` 같은 단순 derived value
- event handler에서 hook action 호출
- UI-only conditional rendering

금지:

- API 호출 직접 작성
- 복잡한 validation rule 직접 작성
- mutation 성공 후 여러 query invalidation 직접 수행
- 서버 DTO를 화면 model로 직접 변환

### Model Hook

책임:

- UI와 domain/application logic 사이 adapter
- query/mutation 호출
- form state와 validation 연결
- side effect orchestration

허용:

- `useSubmitApprovalMutation`
- `useDepartmentPermissionForm`
- `useOrganizationTreePanelState`

금지:

- JSX 반환
- 다른 feature의 내부 hook 호출
- shared utility로 올릴 수 없는 업무 rule을 shared에 위임

### API/Service

책임:

- transport 호출
- request/response DTO mapping
- endpoint boundary
- 기술적 error normalization

허용:

- `getDepartmentDetail`
- `updateDepartment`
- DTO -> entity model mapper 호출

금지:

- toast 표시
- navigation
- React state 접근
- UI component import

### Lib

책임:

- pure business helper
- formatter, guard, predicate

허용:

- `isApprovalEditable(document, user)`
- `formatDepartmentPath(department)`

금지:

- API 호출
- React hook 호출
- global store 접근

## Error Handling 전략

### Global Error Boundary

app layer가 소유한다.

책임:

- 예상하지 못한 render error 격리
- fallback UI 제공
- error logging 연결

금지:

- 모든 API error를 global boundary로 던지기
- form validation error를 boundary로 처리
- 인증 만료 toast를 boundary에서 처리

기준:

- boundary는 "복구 불가능한 UI 예외"를 처리한다.
- API 실패는 query/mutation 수준에서 처리한다.

### API Error

처리 위치:

- transport normalization: `shared/api`
- entity/feature specific message mapping: 해당 slice `model`
- 사용자 표시: feature/widget/page boundary

기본 분류:

| Error | 처리 |
| --- | --- |
| 400 validation | form field error 또는 inline error |
| 401 session expired | auth 만료 처리 단일 경로 |
| 403 forbidden | 접근 권한 없음 UI 또는 toast |
| 404 not found | empty/not found state |
| 409 conflict | conflict 안내와 재조회 |
| 500+ server | fallback + retry 가능성 제공 |
| network | retry 또는 네트워크 안내 |

### 인증 만료

원칙:

- 인증 만료 처리는 단일 경로에서 수행한다.
- 여러 컴포넌트가 각각 alert/toast/redirect를 실행하지 않는다.
- 401 반복 발생 시 중복 안내를 방지한다.

기준:

- API interceptor 또는 auth session manager가 401을 감지한다.
- public route 요청은 인증 만료 처리를 트리거하지 않는다.
- session expired 이벤트는 idempotent하게 처리한다.
- redirect 대상은 app/router guard와 일관되어야 한다.

금지:

- 각 feature mutation에서 401 alert 직접 표시
- 로그인 페이지 진입 중 session expired alert 반복
- API client와 router guard가 서로 다른 storage 상태를 기준으로 판단

### Toast 표시 기준

toast는 사용자에게 필요한 "결과 알림"만 표시한다.

표시한다:

- mutation 성공/실패 결과
- 사용자가 방금 실행한 액션의 완료
- 복구 가능한 오류와 다음 행동

표시하지 않는다:

- 최초 목록 query 실패마다 반복 toast
- form field validation error
- skeleton으로 충분한 loading 상태
- 자동 background refetch 실패

위치:

- feature mutation hook에서 message 정책을 소유하거나
- page/widget에서 action 결과를 받아 표시한다.

기준:

- 같은 실패가 반복 발생하면 dedupe한다.
- toast message는 업무 언어로 작성한다.
- 개발자용 error message를 그대로 노출하지 않는다.

### Form Error

처리 기준:

- field error는 field 근처에 표시한다.
- form-level error는 submit 영역 근처에 표시한다.
- 서버 validation error는 form library의 `setError`로 매핑한다.
- toast는 form submit 자체가 실패했음을 보조적으로 알릴 때만 사용한다.

금지:

- 모든 field error를 toast로 표시
- 서버 validation response를 component마다 직접 parsing
- form error를 global store에 저장

## Loading / Skeleton 전략

### Loading UI 기준

| 상황 | UI |
| --- | --- |
| 최초 page 진입 | page skeleton 또는 section skeleton |
| 작은 button action | button pending state |
| modal detail loading | modal 내부 spinner/skeleton |
| background refetch | 기존 데이터 유지 + subtle indicator |
| route lazy loading | route fallback |

원칙:

- 전체 화면 spinner는 앱 초기화나 route 전환처럼 큰 boundary에서만 사용한다.
- 이미 데이터가 있으면 skeleton으로 화면을 지우지 않는다.
- mutation pending은 action control 주변에 표시한다.

### Skeleton 사용 기준

사용한다:

- layout shape가 예측 가능하다.
- 데이터 로딩이 300ms 이상 체감될 수 있다.
- table/card/list처럼 구조 반복이 명확하다.

사용하지 않는다:

- 아주 짧은 loading
- 버튼 하나의 pending
- shape가 자주 바뀌어 skeleton이 오히려 혼란스러운 화면

### Empty State 기준

empty state는 "정상적으로 데이터가 없음"을 의미한다.

포함해야 할 내용:

- 무엇이 없는지
- 사용자가 할 수 있는 다음 행동
- 권한이 없어서 못 보는 것인지, 진짜 없는 것인지 구분

금지:

- API error를 empty state로 숨김
- 권한 없음과 데이터 없음 혼동

### Retry 정책

React Query retry 기준:

- GET query는 네트워크/5xx에 제한적으로 retry 허용
- 400/401/403/404는 retry하지 않는다.
- mutation은 기본적으로 자동 retry하지 않는다.

UI retry:

- 사용자가 다시 시도할 수 있는 버튼을 제공한다.
- destructive action은 자동 retry하지 않는다.

## Runtime Anti-Patterns

- UI component 내부 API 호출 과다
- component가 DTO parsing, toast, navigation, invalidation을 모두 수행
- 인증 만료 alert를 여러 위치에서 표시
- loading 중 기존 데이터를 지워 화면이 깜빡임
- 모든 query error를 toast로 표시
- form validation error를 toast로만 표시
- empty state로 권한 부족 또는 API 실패를 숨김
- API service가 React hook이나 router를 import

## 검토 체크리스트

- component는 UI 표현에 집중하는가?
- mutation orchestration은 feature/model에 있는가?
- API service가 toast/navigation/state를 알지 않는가?
- 401 처리 경로가 하나인가?
- toast가 사용자 액션 결과에만 제한되는가?
- form error가 field/form 위치에 표시되는가?
- 최초 loading, background refetch, mutation pending UI가 구분되는가?
- retry가 error type에 맞게 제한되는가?
