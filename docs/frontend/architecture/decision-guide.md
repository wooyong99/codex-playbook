# Decision Guide

## 목적

이 문서는 FSD 구조에서 애매한 설계 결정을 빠르게 내리기 위한 판단 기준을 제공한다.

핵심 질문은 세 가지다.

- 언제 분리하는가?
- 언제 추상화하는가?
- 언제 shared로 올리는가?

## 적용 범위

포함:

- page/widget/feature/entity/shared 선택 기준
- slice 분리 기준
- abstraction 기준
- shared 승격 기준
- legacy 리팩토링 판단 기준

제외:

- 각 layer의 상세 책임: [frontend-architecture](frontend-architecture.md)
- 파일 배치 예시: [folder-structure](folder-structure.md)

## 의사결정 기본 원칙

1. 현재 변경 이유를 먼저 식별한다.
2. 가장 낮은 layer에 둘 수 있는지 검토한다.
3. 재사용 가능성보다 실제 사용처와 변경 이유를 우선한다.
4. 추상화는 중복 제거보다 의미 명확화가 먼저다.
5. shared 승격은 마지막 선택이다.

## 어디에 둘 것인가

### Page로 둔다

조건:

- URL과 직접 연결된다.
- route params/search params를 해석한다.
- 여러 widget/feature를 단순 조합한다.
- 한 route에서만 의미가 있다.

예시:

- `approval-detail-page`
- `organization-settings-page`

Page에서 내려야 하는 신호:

- 동일 UI block이 다른 page에도 필요하다.
- action form/mutation이 길어진다.
- route와 무관한 업무 rule이 생긴다.

### Widget으로 둔다

조건:

- page의 독립 section이다.
- 여러 entity/feature를 조합한다.
- URL을 소유하지 않는다.
- 사용자에게 하나의 화면 블록으로 인식된다.

예시:

- `organization-tree-panel`
- `approval-board`
- `messenger-room-list-panel`

Feature로 내려야 하는 신호:

- widget 내부에 독립 action이 반복된다.
- action이 다른 widget/page에서도 필요하다.
- mutation, validation, toast, invalidation이 특정 버튼/form에 묶인다.

### Feature로 둔다

조건:

- 사용자 액션으로 설명된다.
- 독립적으로 렌더링하고 사용할 수 있다.
- mutation, validation, side effect 중 하나 이상을 포함한다.
- 여러 page/widget에서 재사용될 수 있다.

예시:

- `assign-department-leader`
- `submit-approval`
- `invite-user`

Entity로 올려야 하는 신호:

- feature 내부 model이 다른 feature에서도 필요하다.
- 같은 query key와 read query가 반복된다.
- 비즈니스 핵심 명사와 관련된 공통 표시/해석이 생긴다.

### Entity로 둔다

조건:

- 핵심 비즈니스 명사다.
- 여러 feature/widget/page에서 공유된다.
- read query, model, mapper, display helper가 필요하다.
- 사용자 action보다 데이터 개념이 중심이다.

예시:

- `user`
- `department`
- `approval-document`

Feature로 내려야 하는 신호:

- 사용자의 특정 행위를 수행한다.
- mutation workflow가 있다.
- form validation과 side effect가 action에 묶인다.

### Shared로 둔다

조건:

- 비즈니스 의미 없이 설명 가능하다.
- 여러 slice에서 실제로 사용 중이다.
- 하위 layer 의존이 없다.
- 도메인 변경 이유로 수정될 가능성이 낮다.

예시:

- `Button`
- `Dialog`
- `formatDate`
- `httpClient`

Shared로 올리면 안 되는 신호:

- 이름에 도메인 단어가 들어간다.
- 특정 API endpoint를 안다.
- 특정 permission이나 업무 상태를 해석한다.
- "곧 재사용될 것 같다"는 추측뿐이다.

## 언제 분리하는가

분리한다:

- 변경 이유가 두 개 이상이다.
- 테스트 시나리오가 독립적으로 설명된다.
- Public API로 계약을 만들 수 있다.
- 두 번째 실제 사용처가 생겼다.
- 파일이 커진 이유가 단일 책임이 아니라 책임 혼합이다.

분리하지 않는다:

- 줄 수가 많지만 책임이 하나다.
- 사용처가 하나뿐이고 분리 이름이 모호하다.
- props 전달을 줄이기 위한 임시 분리다.
- UI 스타일만 다르고 동작은 같다.

질문:

- 이 코드가 바뀌는 이유는 무엇인가?
- 같은 이유로 함께 바뀌는 코드인가?
- 분리 후 이름이 더 명확해지는가?
- 분리 후 import 방향이 더 단순해지는가?

## 언제 추상화하는가

추상화한다:

- 중복된 코드가 같은 개념을 표현한다.
- 호출부가 더 업무 언어에 가까워진다.
- 테스트 경계가 명확해진다.
- 변경 가능성이 한 곳으로 모인다.

추상화하지 않는다:

- 우연히 모양만 같은 코드다.
- abstraction 이름이 `manager`, `handler`, `helper`처럼 모호하다.
- 호출부보다 추상화 내부가 더 이해하기 어렵다.
- 미래 요구를 추측해 만든다.

기준:

- 2회 중복: 기다리거나 local helper 검토
- 3회 중복: 공통 abstraction 검토
- 다른 layer에 걸친 중복: 먼저 책임 위치가 잘못됐는지 검토

## 언제 Shared로 올리는가

검토 순서:

1. 같은 slice 내부 `lib`로 충분한가?
2. 같은 entity/feature의 Public API로 충분한가?
3. widget/page composition 문제인가?
4. 비즈니스 의미 없이 shared로 설명 가능한가?

승격 조건:

- 실제 사용처가 둘 이상이다.
- 도메인 단어 없이 이름을 지을 수 있다.
- 테스트가 domain fixture 없이 가능하다.
- shared가 어떤 entity/feature도 import하지 않는다.

금지 예시:

- `shared/lib/departmentPermission.ts`
- `shared/hooks/useApprovalList.ts`
- `shared/constants/userRole.ts`
- `shared/ui/DepartmentLeaderSelect.tsx`

## CRUD 기능 분해 기준

금지:

- `create-user`, `update-user`, `delete-user`를 자동으로 feature로 만든다.

대신 질문한다:

- 사용자가 실제로 어떤 업무를 수행하는가?
- 권한/검증/side effect가 같은가?
- 화면과 문맥이 독립적인가?

예시:

| 나쁜 이름 | 더 나은 이름 |
| --- | --- |
| `create-user` | `invite-user` |
| `update-role` | `assign-user-role` |
| `delete-document` | `withdraw-approval-draft` |
| `update-department` | `rename-department`, `assign-department-permission` |

## Legacy 리팩토링 기준

레거시 코드를 FSD로 바꿀 때 한 번에 전체 구조를 갈아엎지 않는다.

순서:

1. 변경 중인 사용자 액션을 식별한다.
2. action boundary를 feature로 분리한다.
3. 반복되는 도메인 model/query를 entity로 승격한다.
4. page는 composition만 남기도록 줄인다.
5. shared에 있는 업무 코드는 entity/feature로 되돌린다.

금지:

- 폴더 이동만 하고 책임을 그대로 둔다.
- 기존 shared 남용을 유지한 채 import path만 바꾼다.
- 모든 API를 `shared/api`로 모은다.
- 모든 store를 app/global store로 모은다.

## 최종 판단 체크리스트

Layer:

- 이 코드는 어떤 layer의 책임인가?
- 더 낮은 layer로 내려갈 수 있는가?
- 같은 layer의 다른 slice를 import하지 않는가?

Slice:

- slice 이름이 책임을 설명하는가?
- Public API가 작고 안정적인가?
- 내부 구현을 deep import하지 않아도 되는가?

State:

- 서버 상태와 클라이언트 상태가 분리되어 있는가?
- query data를 store에 복사하지 않았는가?
- derived state를 저장하지 않았는가?

Runtime:

- component 내부 로직이 UI 표현을 넘어서지 않는가?
- toast/error/loading이 일관된 위치에서 처리되는가?
- mutation 후 cache 갱신 기준이 명확한가?

Shared:

- shared로 올린 코드에 비즈니스 단어가 없는가?
- 실제 사용처가 둘 이상인가?
- 도메인 변경 때문에 shared가 자주 바뀌지 않는가?
