# Support API Strategies

이 문서는 `backend/support/api` 모듈의 역할형 전략 문서 맵을 소유한다.

## 목적

- support/api 내부 공통 응답, 예외 응답, 전역 관심사 책임을 전략별로 분리한다.
- response envelope, exception response, common concern의 선택 기준을 한곳에서 찾게 한다.
- endpoint별 API 계약과 공통 HTTP 지원 경계가 서로의 책임을 침범하지 않게 한다.

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

## 공통 의존 흐름

```text
app/api Controller
  -> support/api response envelope
  -> support/api exception response
  -> support/api common concern

support/api
  -> core/application
  -> core/domain
```

Endpoint별 Controller, URI, DTO, OpenAPI 문서화는 [app/api strategies](../../../app/api/strategies/README.md)가 소유한다.
