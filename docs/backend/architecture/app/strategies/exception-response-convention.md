# Exception Response 컨벤션

이 문서는 app 계층에서 예외를 HTTP status와 공통 오류 응답으로 변환하는 전략을 정리한다.

## 목적

- 모든 API 오류 응답을 하나의 형식으로 유지한다.
- domain 예외가 Spring `HttpStatus`에 의존하지 않게 한다.
- 내부 예외 메시지와 stack trace가 클라이언트에 노출되지 않게 한다.

## 적용 범위

- `GlobalExceptionHandler`
- `CoreException`과 `CoreErrorType`의 HTTP status 매핑
- Spring, Jakarta, Jackson validation 예외 매핑
- 공통 오류 응답 DTO

Domain 예외 계층과 `{Domain}ErrorCode`는 [domain exception convention](../../domain/strategies/exception-convention.md)이 소유한다.
응답 envelope의 구조는 [response-envelope-convention](response-envelope-convention.md)이 소유한다.

## 책임

- 예외 타입을 HTTP status로 변환한다.
- 클라이언트에 노출할 error code와 message를 결정한다.
- 4xx와 5xx 로깅 수준을 구분한다.
- 예상하지 못한 예외를 내부 오류 응답으로 차단한다.

## 전체 흐름

```text
Exception
  -> GlobalExceptionHandler
    -> CoreException -> CoreErrorType.toHttpStatus()
    -> Framework exception -> BaseErrorCode
    -> Unknown exception -> INTERNAL_ERROR
  -> BaseResponse.error(BaseError(...))
```

## 세부 규칙

### Handler 위치

- app 전역에 `@RestControllerAdvice` 기반 `GlobalExceptionHandler`를 둔다.
- Controller별 예외 handler를 두지 않는다.
- error response body 생성은 `BaseResponse.error(...)`로 통일한다.

### ErrorType 매핑

`CoreErrorType`은 HTTP 의미를 추상화한 domain 타입이고, 실제 `HttpStatus` 변환은 app 계층에서 수행한다.

| `CoreErrorType` | HTTP status |
|-----------------|-------------|
| `BAD_REQUEST` | 400 |
| `UNAUTHORIZED` | 401 |
| `FORBIDDEN` | 403 |
| `NOT_FOUND` | 404 |
| `CONFLICT` | 409 |
| `INTERNAL_ERROR` | 500 |

### Framework 예외

- `MethodArgumentNotValidException`은 `INVALID_INPUT`으로 변환한다.
- `HttpMessageNotReadableException`은 `INVALID_REQUEST_BODY`로 변환한다.
- `MissingServletRequestParameterException`은 `MISSING_PARAMETER`로 변환한다.
- `HttpRequestMethodNotSupportedException`은 `METHOD_NOT_ALLOWED`로 변환한다.
- `HttpMediaTypeNotSupportedException`은 `UNSUPPORTED_MEDIA_TYPE`으로 변환한다.
- routing 실패는 `NOT_FOUND`로 변환한다.

### 메시지 노출

- 클라이언트 응답에는 `ErrorCode.message`만 노출한다.
- 내부 exception message, SQL, 외부 API 원문 오류, stack trace는 응답에 포함하지 않는다.
- 상세 진단 정보가 필요하면 로그와 tracing system에 남긴다.

### 로깅

- 4xx client error는 WARN으로 기록하고 stack trace는 기본 생략한다.
- 5xx server error는 ERROR로 기록하고 stack trace를 포함한다.
- validation 실패의 field 값에 민감 정보가 포함될 수 있으면 마스킹한다.

## 금지 규칙

- Controller에서 `try-catch`로 오류 응답을 직접 만들지 않는다.
- domain 모듈에서 Spring `HttpStatus`를 참조하지 않는다.
- 내부 예외 메시지를 그대로 `message`에 담아 응답하지 않는다.
- 도메인 규칙 위반을 `BaseErrorCode`에 추가하지 않는다.
- `GlobalExceptionHandler` 외부에 `@ExceptionHandler`를 분산하지 않는다.
- 5xx 예외를 WARN으로만 기록하지 않는다.
- 오류 응답에 `data`와 `error`를 동시에 담지 않는다.

## 예외와 경계

- 외부 provider webhook처럼 provider가 요구하는 오류 body가 있으면 별도 adapter endpoint에서 예외를 둘 수 있다.
- 인증 framework가 challenge header를 요구하면 HTTP header 처리는 보안 설정과 함께 예외로 둘 수 있다.
- 공개 API에서 field-level validation error를 제공해야 하면 response envelope 확장을 먼저 설계한다.

## 완료 기준

- 모든 business API 예외 응답이 `GlobalExceptionHandler`를 통과한다.
- `CoreErrorType`과 `HttpStatus` 매핑이 app 계층에만 존재한다.
- 오류 응답은 공통 envelope를 따르고 내부 구현 정보가 노출되지 않는다.
