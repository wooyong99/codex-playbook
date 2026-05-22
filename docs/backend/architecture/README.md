# Backend Architecture

백엔드 아키텍처 문서의 단일 진입점.

## 목적

이 문서는 `settings.gradle.kts`에 등록된 실제 백엔드 모듈 구조를 기준으로 아키텍처 단위와 전략 문서의 위치를 안내한다.

## 적용 범위

- `backend/app/**`
- `backend/support/**`
- `backend/core/**`
- `backend/internal/**`
- `backend/external/**`

정책 원문은 [policies](../policies/README.md)가 소유하고, 각 모듈 안의 반복 구현 방식은 가장 가까운 `strategies/README.md`가 소유한다.

## 아키텍처 단위

| 단위 | 코드 위치 | 주요 책임 | 전략 문서 |
|------|-----------|-----------|-----------|
| `app/api` | `backend/app/api/{admin,operator,user}` | 외부 HTTP API 애플리케이션과 Controller 진입점 | [app/api](./app/api/README.md) |
| `app/batch` | `backend/app/batch` | 배치 애플리케이션 진입점과 Job 구성 | 전용 문서 없음 |
| `app/worker` | `backend/app/worker` | 비동기 worker 애플리케이션 진입점 | 전용 문서 없음 |
| `support/api` | `backend/support/api` | API 공통 응답, 예외, 필터, tenant, trace, rate limit | [support/api](./support/api/api-guidelines.md) |
| `core/application` | `backend/core/application` | 유스케이스 실행, 서비스 조합, 포트 계약 | [core/application](./core/application/application-guidelines.md) |
| `core/domain` | `backend/core/domain` | 도메인 모델과 도메인 규칙 | [core/domain](./core/domain/domain-guidelines.md) |
| `internal/persistence` | `backend/internal/persistence` | JPA, QueryDsl, 저장소 adapter | [internal/persistence](./internal/persistence/persistence-guidelines.md) |
| `internal/*` | `backend/internal/{cache,messaging,observability,object-storage,security}` | 내부 인프라 adapter 후보 모듈 | [internal](./internal/README.md) |
| `external/*` | `backend/external/{integration,webhook}` | 외부 시스템 연동 adapter 후보 모듈 | [external](./external/README.md) |

## 의존 방향

```text
app/api -> support/api -> core/application -> core/domain
app/batch -> core/application -> core/domain
app/worker -> core/application -> core/domain

internal/* -> core/application -> core/domain
external/* -> core/application -> core/domain
```

`backend/app/api/admin`은 현재 `backend/internal/persistence`를 직접 참조한다. 이는 `build.gradle.kts`에서 확인되는 실제 의존이며, 신규 기능에서 유지할지 축소할지는 별도 설계 판단이 필요하다.

## 문서 구조

- [app](./app/README.md) - API, batch, worker 애플리케이션 진입점
- [support](./support/README.md) - API 공통 지원 모듈
- [core](./core/README.md) - application, domain 핵심 모듈
- [internal](./internal/README.md) - 내부 인프라 모듈
- [external](./external/README.md) - 외부 연동 모듈

## 공통 문서 템플릿

architecture 하위 문서는 문서 깊이에 따라 다음 섹션 순서를 기본으로 한다.

| 문서 유형 | 필수 섹션 | 예시 |
|-----------|-----------|------|
| 아키텍처 단위 README | 목적, 적용 범위, 모듈 맵, 의존 경계, 문서 운영 원칙 | `core/README.md`, `external/README.md` |
| 모듈 Guidelines | 코드 위치, 책임, 의존 경계, 핵심 원칙, 관련 정책, 금지 규칙, 주요 컴포넌트, 전략 문서, 완료 기준 | `core/application/application-guidelines.md`, `external/integration/integration-guidelines.md` |
| Strategies README | 목적, 적용 범위, 전략 문서, 공통 의존 흐름 | `core/application/strategies/README.md`, `external/integration/strategies/README.md` |
| 개별 Strategy 문서 | 목적, 적용 범위, 책임, 전체 흐름 또는 전체 구조, 세부 규칙, 금지 규칙, 예외와 경계, 완료 기준 | `*-convention.md` |

코드가 아직 없는 후보 모듈도 같은 Guidelines 템플릿을 따르되, 전략 문서가 없으면 `전략 문서 없음`으로 명시하고 구현 추가 시 보강해야 할 기준은 `완료 기준`에 둔다.

## 관련 정책

- [policies/security](../policies/security.md) - 인증/인가와 민감 정보 처리
- [policies/logging](../policies/logging.md) - 로깅 형식과 민감 정보 차단
- [policies/transaction-and-consistency](../policies/transaction-and-consistency.md) - 트랜잭션 경계와 정합성
- [policies/concurrency-and-performance](../policies/concurrency-and-performance.md) - 동시성 제어와 성능

## 운영 원칙

- architecture 단위가 추가·삭제·개편되면 이 README를 먼저 갱신한다.
- 세부 전략 문서 목록은 각 단위의 `{actual-unit}-guidelines.md`와 `strategies/README.md`가 소유한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 단위 내부 세부 링크는 각 단위 문서가 소유한다.
