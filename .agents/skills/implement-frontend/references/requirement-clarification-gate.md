# Frontend Requirement Clarification Gate

이 문서는 `implement-frontend`가 frontend 구현을 시작하기 전에 사용자 요구사항의 모호성을 어떻게 분석하고, 어떤 정보가 부족하면 구현을 멈추고 질문해야 하는지 정의한다.

마일스톤 분할은 [milestone-planning.md](milestone-planning.md)가 소유하고, design/implementation/review 실행 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유한다. 이 문서는 그보다 앞선 요구사항 명확화 게이트만 소유한다.

## 목적

`implement-frontend`는 추상적인 frontend 요청을 바로 구현하지 않는다.

사용자가 "목록 화면 만들어줘", "폼 구현해줘", "검색 UI 추가해줘", "UI 개선해줘", "상태관리 구조 개선해줘"처럼 추상적으로 요청하면 메인 에이전트는 먼저 구현 방식에 영향을 주는 사용자 흐름, API 계약, 상태 소유권, cache/invalidation, UX 실패 처리, 접근성, 반응형, 성능, 검증 결정을 식별한다. 결정에 필요한 핵심 정보가 없으면 구현, TDD 작성, architecture review input 생성을 시작하지 않고 사용자에게 질문한다.

## 게이트 위치

요구사항 명확화 게이트는 모든 frontend 마일스톤 계획과 서브에이전트 호출보다 먼저 수행한다.

```text
Frontend request
  -> Main agent performs requirement clarification gate
  -> If decision-critical info is missing, stop and ask user
  -> Main agent records clarified frontend requirement context
  -> Main agent plans frontend milestones
  -> Frontend Design Writer / Implementation Engineer / Architecture Reviewer loop
```

## 분석 항목

메인 에이전트는 구현 전에 아래 항목을 확인한다.

- 사용자 흐름: 누가, 어느 화면에서, 어떤 순서로, 어떤 목적을 위해 기능을 사용하는가
- 진입 경로와 라우팅: route, page, deep link, redirect, guard, back navigation, URL state가 필요한가
- 화면 상태: loading, error, empty, success, disabled, pending, dirty, optimistic 상태가 필요한가
- interaction lifecycle: 클릭, 입력, submit, 취소, 재시도, 중복 실행 방지, focus 이동 흐름이 무엇인가
- API 계약: request/response shape, error shape, pagination, sorting/filtering, backend 선행 작업이 확정됐는가
- state ownership: server state, client state, form state, URL state, derived state, global state 중 어디가 소유하는가
- cache/invalidation: query key, stale time, invalidation, optimistic update, refetch, infinite query가 필요한가
- form/submit 정책: validation, 중복 제출 방지, 실패 복구, 저장 중 navigation guard, partial submit 허용 여부가 무엇인가
- error/loading/empty/success UX: 어떤 문구, 재시도, fallback, toast, inline error, boundary가 필요한가
- responsive/a11y: viewport별 layout, keyboard interaction, focus management, aria/semantic 요구가 있는가
- design source: Figma, 기존 design system, 기존 화면 관례, 문서화된 UI/UX 기준이 있는가
- 렌더링 성능: list size, virtualization, memoization, hydration, suspense, code splitting이 구현 방식에 영향을 주는가
- 브라우저 검증 기준: 어떤 화면, viewport, interaction, visual/a11y 시나리오를 성공으로 볼 것인가

## 질문 우선순위

질문은 구현 영향도가 큰 순서로 묻는다.

1. 사용자 흐름과 대상 화면
2. API 계약과 backend dependency
3. 상태 소유권과 interaction state
4. cache/invalidation 정책
5. UX 실패 처리와 복구 정책
6. responsive/a11y/design 제약
7. 성능 요구사항과 데이터 규모
8. 브라우저 검증 기준

한 번에 모든 항목을 묻지 않는다. 구현 구조를 결정하는 데 필요한 핵심 질문을 1~3개로 압축하고, 답변에 따라 다음 질문이 필요한지 판단한다.

## 추론 가능 항목

아래 항목은 저장소의 기존 코드와 문서 관례를 근거로 메인 에이전트가 합리적으로 추론할 수 있다.

- 코드 스타일
- 폴더와 component 배치 관례
- component, hook, query, store, DTO naming
- 기존 router, query/cache, form library 사용 방식
- design system token과 공통 component 사용 방식
- 기존 화면의 저위험 loading/error/empty 표시 패턴
- build/test/browser 검증 명령과 artifact 저장 방식

추론한 항목은 확정 요구사항이 아니라 "코드베이스 관례 기반 구현 선택"으로 다룬다.

## 추론 금지 항목

아래 항목은 사용자 또는 명시 Source of Truth와 합의 없이 확정하지 않는다.

- 제품 UX 정책
- navigation flow와 route 구조
- backend API shape와 error semantics
- cache freshness, invalidation, refetch 정책
- optimistic update 적용 여부
- destructive action, submit, retry, cancel 정책
- form validation과 dirty state 정책
- design-critical responsive 또는 a11y 예외
- 사용자에게 노출되는 문구, 빈 상태, 실패 복구 UX

이 항목이 구현 방식에 영향을 주는데 입력에서 확인되지 않으면 구현을 시작하지 않는다.

## Frontend 운영 가능성 확인

frontend의 운영 가능성은 사용자와 운영자가 실제 화면에서 문제를 발견하고 복구할 수 있는 UX와 관측 가능성으로 취급한다.

- API 실패가 사용자 행동으로 복구 가능해야 하면 retry button, inline error, toast, form value preservation이 필요할 수 있다.
- 운영자가 실패 원인을 추적해야 하면 request id, error code, logging hook, monitoring event, user action trace가 필요할 수 있다.
- 중복 제출이나 중복 실행을 막아야 하면 disabled state, idempotency key 전달, pending lock, optimistic rollback 정책이 필요할 수 있다.
- 사용자에게 최신성이 중요한 데이터라면 stale indicator, refetch, invalidation, background update 정책이 필요할 수 있다.
- large list나 feed UX에서는 pagination 방식, virtualization, skeleton, scroll restoration, browser verification 기준이 아키텍처 요구사항이 될 수 있다.

"일단 아무 error toast만 띄운다", "cache는 기본값으로 둔다", "나중에 UX를 맞춘다" 같은 결정을 구현 영향도가 큰 정책으로 대체하지 않는다.

## 모호한 요청별 질문 예시

목록 화면:

- 관리자 목록인가, 사용자 feed/explore 목록인가
- route, 정렬/필터, pagination 방식, 데이터 규모는 무엇인가
- loading/error/empty와 row action 실패 UX를 어떻게 처리해야 하는가

폼 구현:

- validation은 client, server, hybrid 중 무엇인가
- submit 중 중복 제출, 취소, 저장 실패, 값 보존, 재시도 정책은 무엇인가
- 저장 후 이동, modal close, dirty navigation guard가 필요한가

검색 UI:

- 검색어를 URL state로 보존해야 하는가
- debounce, submit 검색, 자동완성, no-result UX 중 무엇이 필요한가
- API 계약, cache key, pagination, 대량 결과 렌더링 기준은 무엇인가

UI 개선:

- 기준 design source와 변경 가능한 범위는 무엇인가
- responsive, accessibility, visual regression 검증 기준은 무엇인가
- 기존 design system 또는 특정 화면 관례를 반드시 따라야 하는가

상태관리 구조 개선:

- 어떤 상태를 local, URL, server cache, global store 중 어디로 이동하려는가
- 기존 cache invalidation과 화면 간 동기화 정책을 바꿀 수 있는가
- 공개 component API 또는 기존 route 동작 변경은 제외되는가

## 확정 요구사항 컨텍스트

게이트를 통과하면 메인 에이전트는 이후 role input artifact에서 참조할 수 있도록 확정 frontend 요구사항 컨텍스트를 남긴다.

컨텍스트 템플릿과 저장 규칙은 [requirement-context-template.md](requirement-context-template.md)가 소유한다. role input artifact에는 이 컨텍스트의 본문을 복사하지 않고 경로만 기록한다.

## 중단 기준

아래 조건 중 하나라도 해당하면 frontend 구현을 시작하지 않고 사용자에게 질문한다.

- 대상 route/page 또는 사용자 흐름이 답변에 따라 달라진다.
- API 계약, error shape, pagination, backend 선행 작업 여부가 구현 방식을 바꾼다.
- state ownership, cache key, invalidation, optimistic update 선택이 여러 구현 대안으로 갈린다.
- form submit, 중복 실행 방지, 실패 복구, navigation guard 정책이 불명확하다.
- responsive/a11y/design source가 component 구조와 layout 선택을 바꾼다.
- 데이터 규모나 rendering 성능 요구에 따라 virtualization, infinite query, memoization 전략이 달라진다.
- 구조 개선 요청에서 변경 가능 범위와 성공 기준이 불명확하다.

단순 UI copy 수정이나 국소 component 스타일 조정처럼 결정 영향도가 낮고 기존 코드 관례가 충분히 명확하면, 메인 에이전트는 확정된 기본값과 가정을 기록한 뒤 마일스톤 계획으로 진행할 수 있다.
