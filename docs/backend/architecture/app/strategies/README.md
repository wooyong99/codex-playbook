# App Strategies

이 디렉토리는 `app` 단위의 HTTP API 계약, DTO, 응답, 예외, 문서화, 패키지 구조 전략을 소유한다.

## 목적

- API 추가와 변경 시 반복되는 표현 계층 판단을 문서별 책임으로 나눈다.
- REST URI, OpenAPI, version, DTO, response envelope, exception response가 서로 중복 정의되지 않게 한다.
- Controller가 application UseCase를 호출하는 경계와 HTTP 계약의 외부 노출 방식을 분리한다.

## 적용 범위

- REST API endpoint 설계
- app 계층 Request/Response DTO 설계
- 공통 응답, 예외 응답, OpenAPI 문서화, API versioning
- app module/package 내부 배치와 네이밍

## 문서 책임

| 문서 | 소유하는 책임 |
|------|---------------|
| [controller-convention](controller-convention.md) | Controller의 HTTP adapter 책임과 UseCase 호출 흐름 |
| [resource-design-convention](resource-design-convention.md) | REST URI naming, resource 단위 설계, method, path/query 기준 |
| [dto-convention](dto-convention.md) | Request/Response DTO, nullable, optional, mapping 기준 |
| [response-envelope-convention](response-envelope-convention.md) | `BaseResponse`, `BaseError`, pagination envelope 같은 공통 응답 DTO |
| [exception-response-convention](exception-response-convention.md) | 예외를 HTTP status와 오류 응답으로 변환하는 규칙 |
| [api-documentation-convention](api-documentation-convention.md) | OpenAPI tag, operation, schema, response 문서화 규칙 |
| [api-versioning-convention](api-versioning-convention.md) | `/api/v{N}` version path와 breaking change 관리 |
| [package-structure](package-structure.md) | app 패키지와 파일 배치 기준 |
| [naming-convention](naming-convention.md) | URI segment, class, DTO, method, operationId 네이밍 |
| [common-concern-convention](common-concern-convention.md) | app 전역 관심사 패키지 분류 기준 |

## 전체 흐름

```text
Resource design
  -> Version policy
  -> Controller
    -> Request DTO
    -> CommandUseCase | QueryUseCase
    -> Response DTO | Response envelope
  -> OpenAPI documentation
  -> Exception response
```

## 분리 원칙

- REST resource와 URI는 [resource-design-convention](resource-design-convention.md)이 소유한다.
- DTO field, nullable, optional 의미는 [dto-convention](dto-convention.md)이 소유한다.
- `{ data }`, `{ error }`, page metadata 같은 응답 envelope는 [response-envelope-convention](response-envelope-convention.md)이 소유한다.
- 오류 code와 message가 HTTP 응답으로 나가는 방식은 [exception-response-convention](exception-response-convention.md)이 소유한다.
- OpenAPI annotation과 문서 완성 기준은 [api-documentation-convention](api-documentation-convention.md)이 소유한다.
- 이름이 충돌하면 [naming-convention](naming-convention.md)을 우선 확인하고, 구조 위치가 충돌하면 [package-structure](package-structure.md)을 우선 확인한다.

## 금지 규칙

- 하나의 전략 문서에 URI, DTO, 응답, 예외, OpenAPI 세부 규칙을 모두 섞지 않는다.
- Controller 문서가 DTO nullable, response envelope, versioning 세부 정책까지 소유하지 않는다.
- OpenAPI 문서화 규칙을 Controller 구현 예시 안에만 숨기지 않는다.
- 공통 응답 DTO와 예외 응답 DTO를 도메인별 DTO 문서에 섞지 않는다.
- package 구조 문서가 각 컴포넌트의 세부 설계 규칙까지 중복 정의하지 않는다.

## 완료 기준

- 신규 API 설계 항목을 어느 전략 문서에서 확인해야 하는지 바로 찾을 수 있다.
- 각 문서는 목적, 적용 범위, 책임, 세부 규칙, 금지 규칙, 완료 기준을 가진다.
- 기존 app 전략 문서에 레거시 템플릿 섹션이 남아 있지 않다.
