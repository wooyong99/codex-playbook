# Frontend TDD 템플릿

## 목적

프론트엔드 기술설계문서의 최종 산출물 구조와 섹션별 작성 기준을 정의한다.

## 적용 범위

이 문서는 TDD의 목차, 섹션 책임, 저장 규칙을 소유한다. 문서를 작성하는 순서는 [frontend-tdd-workflow.md](frontend-tdd-workflow.md)가 소유한다.

## 전체 구조

````markdown
# {기능명} Frontend TDD

> 작성일: YYYY-MM-DD
> 상태: Draft | Reviewing | Approved | Superseded
> 대상 영역: {route/page/feature/widget/shared}

## 1. 설계 배경 및 목표

### 1.1 배경
{사용자 문제, 제품 맥락, 현재 frontend 구조의 제약}

### 1.2 목표
- {목표와 달성 기준}

### 1.3 비목표
- {이번 범위에서 제외하는 항목}

## 2. 사용자 흐름과 라우팅

### 2.1 진입점
- route: `{route}`
- page/layout: `{page 또는 layout}`

### 2.2 화면 흐름
{사용자 행동 순서와 화면 전환}

### 2.3 라우팅 결정
- 신규 route: {route}
- 기존 route 변경: {change}
- guard/redirect: {policy}
- URL state: {query/path state}

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
`-- {Widget}
    `-- {FeatureComponent}
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
{API client, query/mutation hook, type 위치}

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

- 렌더링 최적화: {decision}
- 리스트/페이지네이션: {decision}
- 접근성: {decision}
- 모바일/반응형: {decision}

## 10. 검증 계획

| 시나리오 | 검증 방식 | 기대 결과 |
|----------|-----------|-----------|
| {scenario} | unit/integration/e2e/browser/manual | {expected} |

## 11. 리스크와 미결정 사항
- {risk or open question}
````

## 섹션별 작성 기준

- 사용자 흐름과 라우팅: route, layout, guard, redirect, URL state를 포함한다.
- 폴더 구조: 프로젝트의 실제 frontend architecture 문서를 우선한다.
- 컴포넌트 구조: 책임 분리, props/state contract, public API 경계를 포함한다.
- 상태관리 구조: server, client, form, URL, derived state로 분류한다.
- API 연동 방식: endpoint, type, hook, loading/error, invalidation을 함께 설명한다.
- 캐싱 전략: query key, stale policy, invalidation, optimistic update 여부를 포함한다.
- 에러 처리: 사용자 피드백과 복구 전략까지 포함한다.
- 성능과 UX: 렌더링, 접근성, 반응형, perceived latency를 필요한 수준만 다룬다.

## 저장 규칙

- 기본 저장 위치: `docs/frontend/design/`
- 파일명: `tdd-{feature-slug}.md`
- `{feature-slug}`는 설계 대상의 핵심을 2~4개 영문 kebab-case 단어로 축약한다.
- 관련 설계 문서가 이미 있으면 새 파일을 만들기 전에 갱신 여부를 판단한다.
- 새 문서를 만들면 `docs/frontend/design/README.md`를 갱신한다.

## 검증

- 빈 섹션이 남아 있지 않은가
- 상태와 API, cache, error handling이 서로 연결되어 있는가
- 확인되지 않은 framework나 API 계약을 단정하지 않았는가
- 저장 위치와 문서 맵이 일치하는가
