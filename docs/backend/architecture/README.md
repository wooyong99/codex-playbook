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

## Source Of Truth 선택

backend 변경을 설계, 구현, 리뷰할 때는 변경 유형별로 가장 가까운 guideline, strategy, policy 문서를 Source of Truth로 삼는다.
상위 README는 문서 위치와 라우팅을 확인하는 진입점이며, 세부 규칙 위반의 단독 근거로 사용하지 않는다.

### 문서 선택 절차

1. 변경 파일의 코드 위치를 기준으로 가장 가까운 module guideline을 고른다.
2. 변경한 컴포넌트 역할에 맞는 strategy 문서를 추가한다.
3. 보안, 로깅, 트랜잭션, 동시성, 성능처럼 여러 계층에 걸치는 관심사가 있으면 policy 문서를 추가한다.
4. 특정 기능의 선행 설계가 있으면 `docs/backend/design`의 해당 TDD를 추가한다.
5. README는 문서 맵과 라우팅 확인에만 사용하고, 강제 규칙은 guideline, strategy, policy 문서에서 찾는다.

### 변경 유형별 필수 문서

| 변경 유형 | 반드시 확인할 문서 | 추가 판단 기준 |
|-----------|-------------------|----------------|
| HTTP endpoint, Controller, app DTO | `architecture/app/api/api-guidelines.md`, 관련 `app/api/strategies/*` | 공통 응답과 예외 응답이 있으면 `support/api/strategies/*`를 함께 본다. |
| UseCase, Service, Facade, Coordinator | `architecture/core/application/application-guidelines.md`, 관련 `core/application/strategies/*` | 트랜잭션 또는 외부 호출 조합이 있으면 `policies/transaction-and-consistency.md`를 함께 본다. |
| Port 인터페이스 | `core/application/strategies/port-convention.md`, `core/application/strategies/package-structure.md` | 저장소 Port면 `internal/persistence/strategies/storage-adapter-convention.md`도 함께 본다. |
| Domain model, value object, 상태 전이 | `architecture/core/domain/domain-guidelines.md`, `core/domain/strategies/domain-model-convention.md` | 실패 표현이 있으면 `core/domain/strategies/exception-convention.md`도 함께 본다. |
| ErrorCode, CoreException, HTTP 오류 응답 | `core/domain/strategies/exception-convention.md`, `support/api/strategies/exception-response-convention.md` | 외부 provider 오류 번역이면 `external/integration/strategies/errorcode-convention.md`를 함께 본다. |
| JPA Entity, Repository, QueryDsl, DDL | `architecture/internal/persistence/persistence-guidelines.md`, 관련 `internal/persistence/strategies/*` | application Port 계약 변경이 있으면 `core/application/strategies/port-convention.md`를 함께 본다. |
| in-memory runtime 저장소 | `internal/persistence/persistence-guidelines.md`, `internal/persistence/strategies/storage-adapter-convention.md` | 테스트 fake가 아니라 runtime bean이면 persistence adapter로 판정한다. |
| 외부 API 연동 | `architecture/external/integration/integration-guidelines.md`, 관련 `external/integration/strategies/*` | 민감 정보, token, 원문 payload가 있으면 `policies/security.md`, `policies/logging.md`를 함께 본다. |
| API 공통 응답, 예외, filter, tenant, trace, rate limit | `architecture/support/api/api-guidelines.md`, 관련 `support/api/strategies/*` | 인증/인가 또는 민감 header가 있으면 `policies/security.md`를 함께 본다. |
| 인증/인가, 비밀번호, 세션, token | `policies/security.md`, 변경 위치의 module guideline | 저장 또는 조회가 있으면 persistence/application Port 문서를 함께 본다. |
| 로깅, 모니터링, trace | `policies/logging.md`, `support/api` 또는 `external/integration` 관련 전략 | 민감 정보가 로그에 들어갈 수 있으면 `policies/security.md`를 함께 본다. |
| 동시성, idempotency, rate limit, 성능 병목 | `policies/concurrency-and-performance.md` | 정합성 경계가 있으면 `policies/transaction-and-consistency.md`를 함께 본다. |

### 섹션별 사용 방식

| 섹션 | 사용 방식 |
|------|-----------|
| `목적` | 문서가 어떤 결정을 소유하는지 확인한다. |
| `적용 범위` | 변경이 해당 문서 대상인지 확인한다. 범위 밖 문서를 세부 규칙 근거로 사용하지 않는다. |
| `책임`, `의존 경계`, `핵심 원칙` | 구현 방향과 계층 경계를 판단한다. |
| `세부 규칙` | 이름, 위치, 흐름, 변환 방식 등 구체 구현 기준으로 사용한다. |
| `금지 규칙` | 반드시 피해야 하는 코드, 문서, 설정 변경을 확인한다. |
| `예외와 경계` | 허용 가능한 예외와 조건을 확인한다. |
| `완료 체크리스트` | 변경이 문서 기준을 충족했는지 확인한다. |

## 공통 문서 템플릿

architecture 하위 문서는 문서 깊이에 따라 다음 섹션 순서를 기본으로 한다.

| 문서 유형 | 필수 섹션 | 예시 |
|-----------|-----------|------|
| 아키텍처 단위 README | 목적, 적용 범위, 모듈 맵, 의존 경계, 문서 운영 원칙 | `core/README.md`, `external/README.md` |
| 모듈 Guidelines | 코드 위치, 책임, 의존 경계, 핵심 원칙, 관련 정책, 금지 규칙, 주요 컴포넌트, 전략 문서, 완료 체크리스트 | `core/application/application-guidelines.md`, `external/integration/integration-guidelines.md` |
| Strategies README | 목적, 적용 범위, 전략 문서, 공통 의존 흐름 | `core/application/strategies/README.md`, `external/integration/strategies/README.md` |
| 개별 Strategy 문서 | 목적, 적용 범위, 책임, 전체 흐름 또는 전체 구조, 세부 규칙, 금지 규칙, 예외와 경계, 완료 체크리스트 | `*-convention.md` |

코드가 아직 없는 후보 모듈도 같은 Guidelines 템플릿을 따르되, 전략 문서가 없으면 `전략 문서 없음`으로 명시하고 구현 추가 시 보강해야 할 체크 항목은 `완료 체크리스트`에 둔다.

## 관련 정책

- [policies/security](../policies/security.md) - 인증/인가와 민감 정보 처리
- [policies/logging](../policies/logging.md) - 로깅 형식과 민감 정보 차단
- [policies/transaction-and-consistency](../policies/transaction-and-consistency.md) - 트랜잭션 경계와 정합성
- [policies/concurrency-and-performance](../policies/concurrency-and-performance.md) - 동시성 제어와 성능

## 운영 원칙

- architecture 단위가 추가·삭제·개편되면 이 README를 먼저 갱신한다.
- 세부 전략 문서 목록은 각 단위의 `{actual-unit}-guidelines.md`와 `strategies/README.md`가 소유한다.
- 백엔드 문서 홈은 이 README만 참조하고, 아키텍처 단위 내부 세부 링크는 각 단위 문서가 소유한다.
