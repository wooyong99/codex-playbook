# Support API Guidelines

이 문서는 `backend/support/api` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `backend/support/api` - API 공통 응답, 예외, 필터, tenant, trace, rate limit을 담당한다.

## 책임

- 여러 API 애플리케이션이 공유하는 HTTP 공통 관심사를 제공한다.
- 필터, 응답 envelope, 예외 응답 변환, 요청 모니터링, trace id, tenant context를 일관되게 적용한다.
- 공통 지원 모듈이 업무 도메인 로직을 소유하지 않도록 경계를 유지한다.
- Controller, resource, API DTO 같은 endpoint별 계약은 [app/api](../../app/api/api-guidelines.md)에 위임한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, web framework
- used by: `app/api/admin`, `app/api/operator`, `app/api/user`
- 금지되는 방향: endpoint별 Controller/DTO 소유, domain별 업무 흐름 구현, 외부 API 연동 구현

## 핵심 원칙

- support/api는 여러 API 애플리케이션이 공유하는 HTTP 공통 관심사만 소유한다.
- 공통 응답과 오류 응답은 API 전체에서 동일한 envelope와 error mapping 기준을 따른다.
- filter, tenant, trace, rate limit 같은 cross-cutting concern은 domain별 Controller와 분리한다.

## 관련 정책

- [security](../../../policies/security.md) - 보안 header, 인증 컨텍스트, 민감 정보 처리
- [logging](../../../policies/logging.md) - 요청 추적과 예외 로깅
- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - rate limit과 요청 처리 성능

## 금지 규칙

- support/api에 domain별 Controller, Request/Response DTO, use case 조합 로직을 두지 않는다.
- Controller별로 응답 envelope나 예외 응답 포맷을 따로 만들지 않는다.
- trace id, tenant context, security header 같은 공통 관심사를 app/api 각 모듈에 중복 구현하지 않는다.

## 주요 컴포넌트

- Response envelope: `BaseResponse`, pagination response
- Exception handler: `GlobalExceptionHandler`, `ApiException`
- Request context: tenant, trace, monitoring, rate limit
- Web filter: security header, trace, tenant, idempotency

## 전략 문서

- [response-envelope-convention](./strategies/response-envelope-convention.md) - 공통 응답 DTO와 pagination envelope
- [exception-response-convention](./strategies/exception-response-convention.md) - 예외 응답과 HTTP status 매핑
- [common-concern-convention](./strategies/common-concern-convention.md) - API 전역 관심사와 filter 배치

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 모든 API 애플리케이션이 같은 응답 envelope와 예외 응답 포맷을 사용한다.
- [ ] endpoint별 계약과 업무 흐름은 `app/api`와 `core/application`에 남아 있다.
- [ ] trace, tenant, rate limit, security header 같은 공통 관심사의 구현 위치가 `support/api` 경계로 한정되어 있다.
