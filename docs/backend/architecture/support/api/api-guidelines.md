# Support API Guidelines

## 목적

`backend/support/api` 모듈의 API 공통 지원 책임과 전략 문서 체계를 정리한다.

## 적용 범위

- 공통 응답과 오류 응답
- `GlobalExceptionHandler`, `ApiException`
- idempotency, monitoring, rate limit, tenant, trace, security headers, web filter

Controller, resource, API DTO 같은 endpoint별 계약은 [app/api](../../app/api/api-guidelines.md)가 소유한다.

## 책임

- 여러 API 애플리케이션이 공유하는 HTTP 공통 관심사를 제공한다.
- 필터, 응답 envelope, 예외 응답 변환, 요청 모니터링, trace id, tenant context를 일관되게 적용한다.
- 공통 지원 모듈이 업무 도메인 로직을 소유하지 않도록 경계를 유지한다.

## 의존 경계

`build.gradle.kts` 기준 의존 대상은 `core/application`, `core/domain`이다.

## 전략 문서

- [response-envelope-convention](./strategies/response-envelope-convention.md) - 공통 응답 DTO와 pagination envelope
- [exception-response-convention](./strategies/exception-response-convention.md) - 예외 응답과 HTTP status 매핑
- [common-concern-convention](./strategies/common-concern-convention.md) - API 전역 관심사와 filter 배치
