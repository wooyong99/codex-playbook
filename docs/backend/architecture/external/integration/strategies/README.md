# External Strategies

이 문서는 `backend/external/integration` 모듈의 역할형 전략 문서 맵을 소유한다.

## 목적

- external integration 내부 컴포넌트의 책임을 전략별로 분리한다.
- Adapter, ApiClient, DTO, Exception, ErrorCode, Config, Mock Adapter의 선택 기준을 한곳에서 찾게 한다.
- 레거시 템플릿 대신 현재 전략 문서의 용어를 기준으로 external 구조를 설명한다.

## 적용 범위

- outbound Port 구현과 외부 API 호출
- Provider DTO, 예외 계층, 외부 error code 번역
- Provider별 HTTP client 설정, 호출 로깅, local mock

## 전략 문서

| 전략 | 문서 | 책임 |
|------|------|------|
| Adapter | [adapter-convention](adapter-convention.md) | Outbound Port 구현과 외부 예외의 Port Result 변환 |
| ApiClient | [api-client-convention](api-client-convention.md) | HTTP 호출, Provider 예외 변환, token 처리 |
| ApiClient HTTP Client | [api-client-http-client](api-client-http-client.md) | Provider 전용 HTTP client 주입 방식 |
| ApiClient Logging | [api-client-logging](api-client-logging.md) | 외부 API 호출 로그와 민감 정보 차단 |
| DTO | [dto-convention](dto-convention.md) | 외부 요청/응답 스키마 표현 |
| Exception | [exception-convention](exception-convention.md) | Provider 예외 계층 |
| ErrorCode | [errorcode-convention](errorcode-convention.md) | 외부 error code와 Port ErrorCode 번역 |
| Config | [config-convention](config-convention.md) | Provider properties와 HTTP client bean 구성 |
| Mock Adapter | [mock-adapter-convention](mock-adapter-convention.md) | local profile에서 실제 외부 호출 대체 |

## 공통 의존 흐름

```text
application Port
  -> {Provider}{Function}Adapter
    -> {Provider}ApiClient
      -> {Provider}Dtos
      -> {Provider}Exception
    -> {Provider}ErrorCode
    -> Port Result

local profile
  -> Mock{Function}Adapter
```
