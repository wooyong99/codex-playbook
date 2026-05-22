# 예외 처리 컨벤션

이 문서는 `domain` 단위에서 비즈니스 규칙 위반을 표현하는 ErrorCode와 CoreException 전략을 정리한다.

## 목적

- domain 모듈이 framework-independent 예외 계층을 갖게 한다.
- HTTP 상태 코드 매핑을 app 계층 책임으로 분리한다.
- 비즈니스 실패를 도메인별 ErrorCode와 `CoreException`으로 일관되게 표현한다.

## 적용 범위

- `CoreErrorType`
- `ErrorCode` 인터페이스
- `{Domain}ErrorCode` enum
- `CoreException`
- 도메인 전용 exception 클래스가 필요한 경우의 기준

app 계층의 HTTP 응답 변환은 [app exception handling convention](../../app/strategies/exception-handling-convention.md)이 소유한다.

## 책임

- 도메인 실패를 domain language 기반 code와 message로 표현한다.
- framework-independent error type으로 app 계층 매핑에 필요한 의미만 전달한다.
- 도메인별 error code 소유권을 명확히 한다.

## 전체 흐름

```text
domain behavior
  -> CoreException({Domain}ErrorCode)
    -> ErrorCode
      -> CoreErrorType

app GlobalExceptionHandler
  -> CoreErrorType
  -> HttpStatus
```

## 세부 규칙

### CoreErrorType

`CoreErrorType`은 HTTP 상태의 의미를 순수 enum으로 추상화한다. domain은 Spring `HttpStatus`를 직접 알지 않는다.

```kotlin
enum class CoreErrorType {
    BAD_REQUEST,
    UNAUTHORIZED,
    FORBIDDEN,
    NOT_FOUND,
    CONFLICT,
    INTERNAL_ERROR,
}
```

### ErrorCode

모든 도메인 error code enum은 `ErrorCode`를 구현한다.

```kotlin
interface ErrorCode {
    val code: String
    val message: String
    val errorType: CoreErrorType
}
```

### 도메인별 ErrorCode enum

- error code는 도메인별 enum으로 정의한다.
- enum key와 `code` 문자열 값은 동일하게 둔다.
- 여러 도메인이 공유하는 범용 error code enum을 만들지 않는다.

```kotlin
enum class OrderErrorCode(
    override val code: String,
    override val message: String,
    override val errorType: CoreErrorType,
) : ErrorCode {
    ORDER_NOT_FOUND("ORDER_NOT_FOUND", "주문을 찾을 수 없습니다.", CoreErrorType.NOT_FOUND),
    ORDER_ALREADY_CONFIRMED("ORDER_ALREADY_CONFIRMED", "이미 확정된 주문입니다.", CoreErrorType.CONFLICT),
}
```

### CoreException

`CoreException`은 domain error code를 담는 공통 exception이다.

```kotlin
open class CoreException(
    val errorCode: ErrorCode,
    cause: Throwable? = null,
) : RuntimeException(errorCode.message, cause)
```

### 예외 선택 기준

| 상황 | 방식 | 의미 |
|------|------|------|
| 함수 인자 전제조건 | `require(...)` | 프로그래머 실수 또는 잘못된 호출 |
| 객체 상태 전제조건 | `check(...)` | 내부 상태 전이 전제조건 위반 |
| 클라이언트에 구조화해 전달할 비즈니스 실패 | `throw CoreException(errorCode)` | 도메인 실패 응답 필요 |

### 도메인 전용 Exception 클래스

- 기본값은 `CoreException(errorCode)` 직접 사용이다.
- 추가 필드, cause 처리, 타입 기반 catch가 필요할 때만 `{Domain}Exception : CoreException`을 만든다.
- 단일 `CoreException` 처리로 충분하면 도메인별 exception 클래스를 만들지 않는다.

## 금지 규칙

- domain에서 Spring `HttpStatus`, `ResponseEntity`, app response DTO를 참조하지 않는다.
- 여러 도메인이 공유하는 `CommonErrorCode` 같은 범용 enum을 만들지 않는다.
- enum key와 `code` 문자열 값을 다르게 두지 않는다.
- `RuntimeException`, `IllegalStateException` 같은 미정의 exception을 비즈니스 실패 응답 용도로 직접 던지지 않는다.
- 클라이언트에 노출하지 않을 전제조건 위반까지 `CoreException`으로 래핑하지 않는다.
- 필요 없는 `{Domain}Exception` 클래스를 도메인마다 기계적으로 만들지 않는다.
- ErrorCode message에 HTTP 응답 포맷이나 transport 표현을 섞지 않는다.

## 예외와 경계

- `require`와 `check`는 domain 내부 전제조건 보호에 사용한다.
- 외부 입력 형식 검증 실패는 app 또는 application DTO 생성 책임을 우선 검토한다.
- 새 실패 케이스를 클라이언트가 구분해야 하면 기존 enum에 새 값을 append한다.
- 동일한 의미와 동일한 `CoreErrorType`이면 기존 enum 값을 재사용할 수 있다.

## 완료 기준

- 도메인 실패가 `{Domain}ErrorCode`와 `CoreException`으로 표현된다.
- domain이 HTTP나 Spring 타입에 의존하지 않는다.
- app 계층은 `CoreErrorType`만 보고 HTTP 상태로 매핑할 수 있다.
- 범용 error code enum 없이 도메인별 실패 소유권이 드러난다.
