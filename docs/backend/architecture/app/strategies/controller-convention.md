# Controller 컨벤션

이 문서는 `app` 단위 Controller가 HTTP 요청을 application UseCase 호출로 연결하는 전략을 정리한다.

## 목적

- Controller가 HTTP adapter 역할만 수행하게 한다.
- Request DTO, UseCase `Command`, Response DTO의 경계를 명확히 한다.
- Controller가 비즈니스 흐름 조율자나 예외 처리자가 되지 않게 한다.

## 적용 범위

- `@RestController` 클래스
- endpoint method의 request binding, validation, response 반환
- Controller가 주입받는 application UseCase 인터페이스

URI와 HTTP method 설계는 [resource-design-convention](resource-design-convention.md)이 소유한다.
Request/Response DTO field 설계는 [dto-convention](dto-convention.md)이 소유한다.
공통 응답 envelope는 [response-envelope-convention](response-envelope-convention.md)이 소유한다.

## 책임

- HTTP request를 framework DTO로 binding한다.
- `@Valid`와 request parameter validation으로 형식 검증을 수행한다.
- Request DTO를 application `Command`로 변환한다.
- `CommandUseCase` 또는 `QueryUseCase` 인터페이스를 호출한다.
- UseCase 결과를 HTTP status와 공통 응답으로 반환한다.

## 전체 흐름

```text
HTTP request
  -> Controller method
    -> Request DTO validation
    -> request.toCommand()
    -> CommandUseCase | QueryUseCase
    -> result.toResponse() optional
    -> BaseResponse.success(...)
```

## 세부 규칙

### Controller 구조

- 클래스에는 `@RestController`를 사용한다.
- 공통 resource path는 클래스 레벨 `@RequestMapping`에 둔다.
- method는 HTTP binding, DTO 변환, UseCase 호출, response 반환만 가진다.
- UseCase 구현체가 아니라 `{Entity}CommandUseCase`, `{Entity}QueryUseCase` 같은 인터페이스를 주입받는다.
- 인증 주체, tenant, locale 같은 request context는 Controller에서 받아 DTO 변환 시 Command에 반영한다.

```kotlin
@RestController
@RequestMapping("/api/v1/orders")
class OrderController(
    private val orderCommandUseCase: OrderCommandUseCase,
    private val orderQueryUseCase: OrderQueryUseCase,
) {
    @PostMapping
    fun create(
        @Valid @RequestBody request: CreateOrderRequest,
    ): ResponseEntity<BaseResponse<CreateOrderResponse>> {
        val result = orderCommandUseCase.create(request.toCommand())
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(BaseResponse.success(result.toResponse()))
    }
}
```

### Command와 Query 구분

- 상태 변경 endpoint는 `CommandUseCase`를 호출한다.
- 조회 endpoint는 `QueryUseCase`를 호출한다.
- Controller method 이름은 application method 이름과 맞추되 HTTP method 의미와 충돌하지 않게 한다.
- 같은 resource Controller에서 Command와 Query UseCase를 함께 주입받을 수 있다.

### Validation 위치

- Request DTO에는 syntactic validation만 둔다.
- DB 조회, 권한, 중복, 정책 판단은 application UseCase 구현체로 넘긴다.
- Controller에서 `if`로 정책을 판단하지 않는다.

### Response 반환

- 성공 응답은 [response-envelope-convention](response-envelope-convention.md)의 `BaseResponse.success(...)`를 따른다.
- 생성 성공은 `201 Created`, 일반 조회와 변경 성공은 `200 OK`, body 없는 삭제는 프로젝트 정책에 따라 `204 No Content` 또는 envelope 응답 중 하나로 통일한다.
- 오류 응답은 Controller에서 만들지 않고 [exception-response-convention](exception-response-convention.md)을 따른다.

## 금지 규칙

- Controller가 application 구현체인 Facade, Coordinator, Service를 직접 주입받지 않는다.
- Controller가 application `Command`를 `@RequestBody`로 직접 받지 않는다.
- Controller가 domain Entity, Value Object, storage Entity를 직접 반환하지 않는다.
- Controller method 안에서 비즈니스 규칙, 권한 정책, 중복 조회, 상태 전이를 구현하지 않는다.
- Controller별 `try-catch` 또는 `@ExceptionHandler`를 두지 않는다.
- Controller가 다른 Controller를 호출하지 않는다.
- Controller에서 외부 API client, repository, storage adapter를 직접 호출하지 않는다.

## 예외와 경계

- 파일 다운로드, streaming, redirect처럼 envelope 적용이 맞지 않는 endpoint는 명시적으로 예외를 둘 수 있다.
- Health check, actuator, static resource는 REST business API Controller 규칙과 별도로 둘 수 있다.
- 인증 callback처럼 provider protocol을 구현하는 endpoint는 URI와 DTO 규칙의 예외를 둘 수 있지만 application 경계는 유지한다.

## 완료 기준

- Controller method를 읽으면 HTTP binding과 UseCase 호출 흐름만 보인다.
- Request DTO와 application Command가 분리되어 있다.
- 성공 응답과 오류 응답이 각각 response envelope, exception response 규칙을 따른다.
