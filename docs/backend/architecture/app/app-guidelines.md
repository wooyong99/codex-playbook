# App Guidelines

이 문서는 `app` 단위의 HTTP 표현 계층 책임, 의존 경계, 전략 문서 체계를 정리한다.

## 목적

- HTTP API 계약을 application UseCase 계약으로 변환하는 경계를 고정한다.
- Controller, Request/Response DTO, 공통 응답, 예외 응답, OpenAPI 문서가 서로의 책임을 침범하지 않게 한다.
- API를 추가하거나 변경할 때 URI, 버전, DTO, 문서화, 패키지 구조를 같은 기준으로 판단하게 한다.

## 적용 범위

- REST Controller와 HTTP endpoint
- Request/Response DTO와 DTO 변환 Extension
- 공통 응답 DTO와 예외 응답
- API version path, OpenAPI 문서화, 표현 계층 공통 관심사

Application UseCase, Command, Result 계약은 [application guidelines](../application/application-guidelines.md)가 소유한다.
Domain 예외와 ErrorCode의 원천 규칙은 [domain exception convention](../domain/strategies/exception-convention.md)이 소유한다.

## 책임

- HTTP 요청을 수신하고 syntactic validation을 수행한다.
- Request DTO를 application `Command`로 변환하고 UseCase를 호출한다.
- application `Result`를 API 응답 DTO 또는 공통 응답 envelope로 변환한다.
- HTTP status, header, OpenAPI, serialization 같은 표현 계층 관심사를 app 내부에 가둔다.
- 전역 예외를 일관된 HTTP 오류 응답으로 변환한다.

## 의존 경계

- depends on: `application`
- used by: Client / API caller
- allowed: app DTO -> application Command/Result 변환
- forbidden: domain 모델 직접 노출, application Command 직접 HTTP binding, Controller 내부 비즈니스 로직

```text
Client
  -> Controller
    -> Request DTO
    -> DTO Extension
    -> CommandUseCase | QueryUseCase
    -> Response DTO | BaseResponse
```

## 핵심 원칙

- app 단위는 HTTP 계약을 application 계약으로 변환하는 adapter다.
- Controller는 흐름을 조율하지 않고 binding, validation, UseCase 호출, response 반환만 수행한다.
- API 계약은 URI, DTO, OpenAPI, versioning 문서가 함께 바뀌어야 한다.
- 공통 응답과 예외 응답은 전역 규약으로 통일한다.
- DTO의 nullable과 optional 의미는 API 계약에서 명시한다.

## 관련 정책

- [security](../../policies/security.md) - 인증 컨텍스트와 민감 정보 처리
- [logging](../../policies/logging.md) - 요청 추적과 예외 로깅

## 금지 규칙

- Controller 안에 비즈니스 규칙, 계산, 상태 판단을 구현하지 않는다.
- application 계층 `Command`를 `@RequestBody`로 직접 수신하지 않는다.
- Response DTO에 domain Entity나 Value Object를 직접 노출하지 않는다.
- Controller별 `try-catch`나 분산된 `@ExceptionHandler`를 만들지 않는다.
- API breaking change를 version 정책 없이 기존 endpoint에 덮어쓰지 않는다.
- OpenAPI 문서 없이 신규 public endpoint를 추가하지 않는다.
- `nullable` 필드를 단순 편의로 열어두지 않는다. null의 계약 의미를 문서화한다.
- `common`, `shared`, `util` 패키지에 도메인별 Controller, DTO, 변환 로직을 넣지 않는다.

## 전략 문서

- [controller-convention](./strategies/controller-convention.md) - Controller 책임과 UseCase 호출 흐름
- [resource-design-convention](./strategies/resource-design-convention.md) - REST URI와 resource 단위 설계
- [dto-convention](./strategies/dto-convention.md) - Request/Response DTO, nullable, optional 처리
- [response-envelope-convention](./strategies/response-envelope-convention.md) - 공통 응답 DTO와 pagination envelope
- [exception-response-convention](./strategies/exception-response-convention.md) - 예외 응답과 HTTP status 매핑
- [api-documentation-convention](./strategies/api-documentation-convention.md) - OpenAPI 문서화 규칙
- [api-versioning-convention](./strategies/api-versioning-convention.md) - API version 관리 규칙
- [package-structure](./strategies/package-structure.md) - app 패키지 구조
- [naming-convention](./strategies/naming-convention.md) - URI, class, method, OpenAPI 네이밍
- [common-concern-convention](./strategies/common-concern-convention.md) - 표현 계층 전역 관심사

## 완료 기준

- 신규 API의 URI, DTO, 응답 envelope, 예외 응답, OpenAPI, version 정책을 문서 기준으로 설명할 수 있다.
- Controller가 application UseCase 인터페이스만 호출한다.
- HTTP 표현 계층 관심사가 application, domain, storage, external로 새어 나가지 않는다.
- app 하위 문서 맵이 실제 전략 문서와 일치한다.

## Playbook compatibility

- 이 단위는 기존 playbook의 `app` 개념 계층과 동일하다.
- 실제 프로젝트에서 app 모듈명이 `api`, `admin`, `web`처럼 나뉘면 `$reverse-engineer-backend-docs`의 `migrate` 모드에서 실제 진입점 단위로 분리한다.
