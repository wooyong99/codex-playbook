# Naming 컨벤션

이 문서는 app 계층의 URI, class, DTO, method, OpenAPI naming 기준을 정리한다.

## 목적

- API 계약과 코드 이름이 같은 resource 언어를 사용하게 한다.
- Controller, DTO, Extension, OpenAPI operationId를 일관되게 찾을 수 있게 한다.
- 파일 수가 늘어도 이름만 보고 역할과 scope를 알 수 있게 한다.

## 적용 범위

- URI segment와 query parameter 이름
- Controller class와 method 이름
- Request/Response DTO class와 file 이름
- DTO 변환 Extension file과 function 이름
- OpenAPI tag와 operationId

## 책임

- resource, action, DTO, operation 이름의 표준 형식을 정한다.
- 다른 전략 문서에서 사용하는 이름 기준의 단일 출처가 된다.
- 축약어, 대소문자, 복수형 사용 기준을 제한한다.

## 전체 흐름

```text
Resource term
  -> URI segment
  -> Controller name
  -> DTO file and class
  -> UseCase method call
  -> OpenAPI tag and operationId
```

## 세부 규칙

### URI

- URI segment는 복수형 명사와 kebab-case를 사용한다.
- query parameter는 lower camelCase를 사용한다.
- path variable은 `{resourceId}` 형식을 사용한다.

```text
/api/v1/order-items/{orderItemId}?createdFrom=2026-01-01
```

### Controller

- Controller class는 `{Entity}Controller`를 사용한다.
- admin 전용 Controller는 `Admin{Entity}Controller`를 사용할 수 있다.
- method는 `create`, `get`, `search`, `update`, `delete`, `cancel`처럼 application UseCase method와 맞춘다.

### DTO

- Request file은 `dto/{Domain}Requests.kt`를 기본으로 한다.
- Response file은 `dto/{Domain}Responses.kt`를 기본으로 한다.
- Request class는 `{Action}{Entity}Request`를 사용한다.
- Response class는 `{Action}{Entity}Response`를 사용한다.
- API 전용 wrapper가 아니면 `Dto`, `Vo`, `Model` suffix를 붙이지 않는다.

```text
CreateOrderRequest
SearchOrderRequest
GetOrderDetailResponse
```

### Extension

- DTO 변환 파일은 `{Domain}DtoExtension.kt`를 사용한다.
- Request to Command는 `request.toCommand()` 형식의 extension function을 사용한다.
- Result to Response는 `result.toResponse()` 형식의 extension function을 사용한다.
- 이름 충돌이 있으면 action이 드러나도록 `toCreateCommand`, `toDetailResponse`처럼 구체화한다.

### OpenAPI

- tag는 resource 단위 복수형 또는 도메인 이름을 사용한다.
- operationId는 `{verb}{Resource}`를 사용한다.
- version이 다르면 operationId도 충돌하지 않게 version 또는 action을 구체화한다.

```text
createOrder
getOrder
searchOrders
cancelOrder
```

## 금지 규칙

- URI segment에 snake_case, camelCase, PascalCase를 사용하지 않는다.
- Controller 이름에 `Api`, `Rest`, `Endpoint` suffix를 중복해서 붙이지 않는다.
- DTO 이름에 의미 없는 `Data`, `Info`, `Payload`, `Param`을 남용하지 않는다.
- Request와 Response class를 같은 이름으로 만들지 않는다.
- OpenAPI operationId를 framework 자동 생성값에 맡기지 않는다.
- 축약어를 팀 내 표준 없이 사용하지 않는다.
- v1/v2 차이를 `New`, `Old`, `Legacy` suffix만으로 표현하지 않는다.

## 예외와 경계

- 외부 provider callback은 provider 용어를 일부 유지할 수 있다.
- OAuth, SSO, URL, ID처럼 널리 쓰이는 약어는 대문자 표기를 유지할 수 있다.
- 기존 public API 이름을 바꾸면 breaking change가 될 수 있으므로 versioning 정책을 먼저 확인한다.

## 완료 기준

- URI, Controller, DTO, operationId가 같은 resource 용어를 사용한다.
- 파일명만 보고 Request, Response, 변환 Extension의 위치와 역할을 알 수 있다.
- OpenAPI operationId가 중복되지 않는다.
