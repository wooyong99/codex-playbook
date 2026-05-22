# Support API Strategies

## 목적

`backend/support/api` 모듈이 소유하는 API 공통 응답, 예외 응답, 전역 관심사 전략을 정리한다.

## 적용 범위

- 공통 response envelope와 pagination envelope
- 전역 예외 응답 변환
- idempotency, monitoring, rate limit, tenant, trace, security header filter

## 전략 문서

| 전략 | 문서 | 책임 |
|------|------|------|
| Response Envelope | [response-envelope-convention](response-envelope-convention.md) | `ApiResponse`, `ErrorResponse`, page response 같은 공통 응답 구조 |
| Exception Response | [exception-response-convention](exception-response-convention.md) | 예외를 HTTP status와 오류 응답으로 변환하는 규칙 |
| Common Concern | [common-concern-convention](common-concern-convention.md) | API 공통 filter, handler, configuration 배치 기준 |

## 경계

Endpoint별 Controller, URI, DTO, OpenAPI 문서화는 [app/api strategies](../../../app/api/strategies/README.md)가 소유한다.
