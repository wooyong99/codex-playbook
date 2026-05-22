# Common Concern 컨벤션

이 문서는 `support/api` 전역 관심사 패키지에 둘 수 있는 책임을 정리한다.

## 목적

- `common/`이 도메인별 API 코드의 임시 보관소가 되지 않게 한다.
- 여러 resource가 공유하는 표현 계층 기술 관심사를 한 곳에 모은다.
- 공통화할 수 있는 것과 도메인 패키지에 남겨야 하는 것을 구분한다.

## 적용 범위

- response envelope와 error body
- global exception handler
- OpenAPI 설정과 공통 schema
- web config, argument resolver, interceptor
- security, logging, request tracing
- 여러 도메인이 공유하는 syntactic validator

## 책임

- 표현 계층 전체에 적용되는 기술 정책을 담는다.
- domain 지식 없이 유지 가능한 공통 구성요소만 담는다.
- 세부 구현 규칙은 전용 전략 문서로 연결한다.

## 전체 흐름

```text
common/
  -> response
  -> exception
  -> openapi
  -> web
  -> security
  -> logging
```

## 세부 규칙

### 둘 수 있는 것

- `BaseResponse`, `BaseError`, page envelope 같은 공통 응답 DTO
- `GlobalExceptionHandler`, `ErrorTypeExtension`, framework error code
- OpenAPI common response, security scheme, tag grouping 설정
- JSON serialization, CORS, locale, argument resolver 같은 web 설정
- 인증 필터, 현재 사용자 resolver, tenant context resolver
- request ID, MDC, access logging, 민감 정보 마스킹
- 전화번호, 이메일, 날짜 형식 같은 공통 형식 validator

### 둘 수 없는 것

- 특정 도메인 Controller
- 특정 도메인 Request/Response DTO
- 특정 도메인 변환 Extension
- 비즈니스 권한 판단
- DB 조회가 필요한 validation
- application UseCase 호출 흐름

### 판단 기준

아래 질문에 모두 가깝게 답할 수 있을 때만 common에 둔다.

- 여러 도메인 API가 함께 쓰는가?
- HTTP 표현 계층의 기술 책임인가?
- 특정 domain model 없이 이해하고 테스트할 수 있는가?

## 금지 규칙

- common 패키지가 도메인 패키지의 Controller, DTO, Extension을 import하지 않는다.
- 도메인별 response type을 common response envelope에 포함하지 않는다.
- 공통 security filter에서 비즈니스 권한을 판단하지 않는다.
- 공통 validator에서 repository나 Port를 호출하지 않는다.
- logging 공통 처리에서 password, token, secret 원문을 기록하지 않는다.
- common 패키지를 순환 의존을 피하기 위한 우회 경로로 사용하지 않는다.

## 예외와 경계

- provider callback protocol처럼 특정 도메인처럼 보여도 여러 provider가 공유하는 web 기술 처리는 common 후보가 될 수 있다.
- 공통 validator가 도메인 정책을 포함하기 시작하면 application Validator 또는 domain value object로 옮긴다.
- common response와 exception의 세부 규칙은 각각 [response-envelope-convention](response-envelope-convention.md), [exception-response-convention](exception-response-convention.md)을 따른다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] common 패키지의 각 클래스가 표현 계층 전역 관심사임이 이름, 패키지, 참조 관계에서 확인된다.
- [ ] common 패키지가 도메인별 API 계약을 소유하지 않는다.
- [ ] 전역 관심사와 도메인별 API 코드가 package 구조에서 분리되어 있다.
