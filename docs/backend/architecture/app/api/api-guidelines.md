# App API Guidelines

이 문서는 `backend/app/api` 단위의 HTTP API 애플리케이션 책임, 의존 경계, 전략 문서 체계를 정리한다.

## 코드 위치

- `backend/app/api/admin` - 관리자 API HTTP endpoint를 담당한다.
- `backend/app/api/operator` - 운영자 API HTTP endpoint를 담당한다.
- `backend/app/api/user` - 플랫폼 사용자 API HTTP endpoint를 담당한다.

## 목적

- HTTP API 계약을 `core/application` 서비스 계약으로 변환하는 경계를 고정한다.
- Controller, Request/Response DTO, resource 설계, API 문서가 서로의 책임을 침범하지 않게 한다.
- API를 추가하거나 변경할 때 URI, 버전, DTO, 문서화, 패키지 구조를 같은 기준으로 판단하게 한다.

## 적용 범위

- REST Controller와 HTTP endpoint
- Request/Response DTO와 DTO 변환 Extension
- API version path, OpenAPI 문서화, API 모듈 내부 패키지 구조

공통 응답 DTO, 예외 응답, filter 기반 공통 관심사는 [support/api guidelines](../../support/api/api-guidelines.md)가 소유한다.
Application 계약은 [core/application guidelines](../../core/application/application-guidelines.md)가 소유한다.
Domain 모델과 예외의 원천 규칙은 [core/domain guidelines](../../core/domain/domain-guidelines.md)가 소유한다.

## 책임

- HTTP 요청을 수신하고 syntactic validation을 수행한다.
- Request DTO를 application `Command`로 변환하고 UseCase를 호출한다.
- application 결과를 API 응답 DTO로 변환한다.
- HTTP status, header, OpenAPI, serialization 같은 표현 계층 관심사를 app 내부에 가둔다.
- API 공통 응답과 전역 예외 처리는 `support/api` 규약을 따른다.

## 의존 경계

- depends on: `support/api`, `core/application`, `core/domain`
- used by: Client / API caller
- allowed: app DTO -> application 입력/출력 변환
- forbidden: domain 모델 직접 노출, application Command 직접 HTTP binding, Controller 내부 비즈니스 로직

```text
Client
  -> Controller
    -> Request DTO
    -> DTO Extension
    -> core/application service
    -> Response DTO | BaseResponse
```

## 핵심 원칙

- app 단위는 HTTP 계약을 application 계약으로 변환하는 adapter다.
- Controller는 흐름을 조율하지 않고 binding, validation, application 호출, response 반환만 수행한다.
- API 계약은 URI, DTO, OpenAPI, versioning 문서가 함께 바뀌어야 한다.
- 공통 응답과 예외 응답은 `support/api` 전역 규약으로 통일한다.
- DTO의 nullable과 optional 의미는 API 계약에서 명시한다.

## 관련 정책

- [security](../../../policies/security.md) - 인증 컨텍스트와 민감 정보 처리
- [logging](../../../policies/logging.md) - 요청 추적과 예외 로깅

## 금지 규칙

- Controller 안에 비즈니스 규칙, 계산, 상태 판단을 구현하지 않는다.
- core/application 입력 타입을 `@RequestBody`로 직접 수신하지 않는다.
- Response DTO에 domain Entity나 Value Object를 직접 노출하지 않는다.
- Controller별 `try-catch`나 분산된 `@ExceptionHandler`를 만들지 않는다.
- API breaking change를 version 정책 없이 기존 endpoint에 덮어쓰지 않는다.
- OpenAPI 문서 없이 신규 public endpoint를 추가하지 않는다.
- `nullable` 필드를 단순 편의로 열어두지 않는다. null의 계약 의미를 문서화한다.
- `common`, `shared`, `util` 패키지에 도메인별 Controller, DTO, 변환 로직을 넣지 않는다.

## 주요 컴포넌트

- Controller: `{Domain}Controller`
- Request DTO: `{Action}{Resource}Request`
- Response DTO: `{Resource}Response`
- DTO Extension: `{Resource}DtoExtension`
- API documentation: OpenAPI operation and schema
- API version path: `/api/v{major}`

## 전략 문서

- [controller-convention](./strategies/controller-convention.md) - Controller 책임과 UseCase 호출 흐름
- [resource-design-convention](./strategies/resource-design-convention.md) - REST URI와 resource 단위 설계
- [dto-convention](./strategies/dto-convention.md) - Request/Response DTO, nullable, optional 처리
- [api-documentation-convention](./strategies/api-documentation-convention.md) - OpenAPI 문서화 규칙
- [api-versioning-convention](./strategies/api-versioning-convention.md) - API version 관리 규칙
- [package-structure](./strategies/package-structure.md) - app 패키지 구조
- [naming-convention](./strategies/naming-convention.md) - URI, class, method, OpenAPI 네이밍
- [support/api response envelope](../../support/api/strategies/response-envelope-convention.md) - 공통 응답 DTO와 pagination envelope
- [support/api exception response](../../support/api/strategies/exception-response-convention.md) - 예외 응답과 HTTP status 매핑
- [support/api common concern](../../support/api/strategies/common-concern-convention.md) - 표현 계층 전역 관심사

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 신규 API의 URI, DTO, 응답 envelope, 예외 응답, OpenAPI, version 정책이 각 소유 문서 기준과 대조되어 있다.
- [ ] Controller가 `core/application` 계약만 호출한다.
- [ ] HTTP 표현 계층 관심사가 `core`, `internal`, `external`로 새어 나가지 않는다.
- [ ] `app/api` 하위 문서 맵이 실제 전략 문서와 일치한다.
