---
name: write-frontend-tech-design-doc
description: 프론트엔드 기술설계문서(TDD)를 작성하는 스킬. 상태관리 구조, API 연동 방식, 컴포넌트 구조, 라우팅, 캐싱 전략, 에러 처리, 폴더 구조를 포함한 frontend 설계 문서가 필요할 때 사용한다. 신규 화면/기능 설계, 프론트엔드 리팩토링 설계, React/Vue/Svelte 등 클라이언트 앱의 상태/API/cache/component/routing 설계가 필요한 요청에서 사용한다.
---

# write-frontend-tech-design-doc — 프론트엔드 기술설계문서 작성

## 역할

- 프론트엔드 기능 구현 전 기술설계문서(TDD)를 작성한다.
- 문서는 "무엇을 만들지"보다 "상태, API, 컴포넌트, 라우팅, 캐싱, 에러 처리를 왜 이렇게 구성하는지"에 집중한다.
- 실제 프로젝트 문서와 코드에서 확인한 사실만 근거로 삼는다.
- 기본 저장 위치는 `docs/frontend/design/tdd-{feature}.md`다.

## 입력 정리

1. 설계 대상 기능 또는 리팩토링 범위를 한 문장으로 고정한다.
2. 명시적 제외사항을 분리한다.
3. 사용자 흐름, 진입 라우트, 주요 화면, API 계약, 상태 범위, 성능/UX 제약을 확인한다.
4. 정보가 부족하면 구현 전에 질문한다. 단, 저장소 문서와 코드에서 확인 가능한 내용은 먼저 확인한다.

## 근거 수집

필요한 문서만 선별해 읽는다.

- `docs/frontend/README.md`
- `docs/frontend/getting-started.md`
- `docs/frontend/architecture/**`
- `docs/frontend/conventions/**`
- `docs/frontend/performance/**`
- `docs/frontend/ui-ux/**`
- 관련 frontend 코드의 route/page/widget/feature/entity/shared 경로
- 관련 API client, query key, cache invalidation, 상태 store, form, validation, error boundary 코드

backend API 계약이 설계에 필요하면 확인된 API 문서나 타입만 사용한다. backend 구현을 추측하지 않는다.

## 문서 구조

아래 섹션을 포함한다. 해당 없는 섹션도 "해당 없음" 또는 "확인 필요"로 명시해 빈 설계를 만들지 않는다.

````markdown
# {기능명} Frontend TDD

## 1. 설계 배경 및 목표

### 1.1 배경
{사용자 문제, 제품 맥락, 현재 frontend 구조의 제약}

### 1.2 목표
- {목표 1}
- {목표 2}

### 1.3 비목표
- {이번 범위에서 제외하는 항목}

## 2. 사용자 흐름과 라우팅

### 2.1 진입점
- route: `{route}`
- page/layout: `{page 또는 layout}`

### 2.2 화면 흐름
{사용자 행동 순서와 화면 전환}

### 2.3 라우팅 결정
- 신규 route:
- 기존 route 변경:
- guard/redirect:

## 3. 폴더 구조

```text
{관련 frontend 폴더 구조}
```

### 3.1 신규 파일
| 파일 | 역할 |
|------|------|
| `{path}` | {role} |

### 3.2 변경 파일
| 파일 | 변경 이유 |
|------|-----------|
| `{path}` | {reason} |

## 4. 컴포넌트 구조

### 4.1 컴포넌트 트리
```text
{Page}
└── {Widget}
    └── {FeatureComponent}
```

### 4.2 책임 분리
| 컴포넌트 | 책임 | props/state |
|----------|------|-------------|
| `{Component}` | {responsibility} | {contract} |

### 4.3 재사용과 public API
{외부 import 경계, index export, shared/ui 사용 기준}

## 5. 상태관리 구조

### 5.1 상태 분류
| 상태 | 종류 | 소유 위치 | 이유 |
|------|------|-----------|------|
| `{state}` | server/client/form/url/derived | `{owner}` | {reason} |

### 5.2 상태 흐름
{상태 생성, 갱신, 초기화, 동기화 흐름}

### 5.3 폼과 검증
{form library, validation schema, submit lifecycle}

## 6. API 연동 방식

### 6.1 API 계약
| API | 요청 | 응답 | 사용 위치 |
|-----|------|------|-----------|
| `{method path}` | `{request}` | `{response}` | `{usage}` |

### 6.2 Client/Hook 설계
{API client, query/mutation hook, 타입 위치}

### 6.3 로딩/빈 상태
{loading, skeleton, empty, disabled 상태}

## 7. 캐싱 전략

### 7.1 Query Key
| 데이터 | query key | invalidation 조건 |
|--------|-----------|-------------------|
| `{data}` | `{key}` | `{condition}` |

### 7.2 Cache Lifetime
{staleTime, gc/cacheTime, prefetch, optimistic update 여부}

### 7.3 동기화
{mutation 후 갱신, background refresh, pagination/infinite query}

## 8. 에러 처리

### 8.1 에러 분류
| 에러 | 처리 방식 | 사용자 피드백 |
|------|-----------|---------------|
| validation | {handling} | {feedback} |
| network/server | {handling} | {feedback} |
| permission | {handling} | {feedback} |

### 8.2 복구 전략
{retry, rollback, fallback UI, error boundary}

## 9. 성능과 UX 고려사항

- 렌더링 최적화:
- 리스트/페이지네이션:
- 접근성:
- 모바일/반응형:

## 10. 검증 계획

| 시나리오 | 검증 방식 | 기대 결과 |
|----------|-----------|-----------|
| {scenario} | unit/integration/e2e/browser/manual | {expected} |

## 11. 리스크와 미결정 사항

- {risk or open question}
````

## 작성 원칙

- 상태는 server state, client state, form state, URL state, derived state로 분류한다.
- API 연동은 endpoint 나열이 아니라 타입, hook, loading/error, invalidation까지 포함한다.
- 컴포넌트 구조는 책임과 데이터 흐름을 보여야 한다.
- 라우팅은 route, layout, guard, redirect, URL state를 포함한다.
- 캐싱 전략은 query key, stale policy, invalidation, optimistic update 여부를 포함한다.
- 에러 처리는 사용자 피드백과 복구 전략까지 포함한다.
- 폴더 구조는 프로젝트의 실제 architecture 문서를 우선한다.
- 문서에 없는 프레임워크나 라이브러리를 임의로 도입하지 않는다.

## 저장 규칙

- 기본 경로: `docs/frontend/design/tdd-{feature}.md`
- `{feature}`는 소문자 kebab-case로 작성한다.
- 관련 설계 문서가 이미 있으면 새 파일을 만들기 전에 기존 문서를 갱신할지 새 문서로 분리할지 판단한다.
- 새 문서를 만들면 `docs/frontend/design/README.md` 문서 맵을 갱신한다.

## 완료 전 확인

- 상태관리 구조가 server/client/form/url/derived 기준으로 분류되었다.
- API 연동 방식이 타입, hook, loading/error, invalidation까지 설명한다.
- 컴포넌트 구조가 책임 분리와 public API 경계를 포함한다.
- 라우팅과 URL state가 명시되었다.
- 캐싱 전략과 에러 처리가 사용자 경험과 연결되었다.
- 폴더 구조가 `docs/frontend/architecture/**`와 충돌하지 않는다.
- 검증 계획이 unit/integration/e2e/browser/manual 중 필요한 방식을 포함한다.
