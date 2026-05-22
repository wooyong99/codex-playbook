# Domain Model 컨벤션

이 문서는 `domain` 단위에서 Entity, Value Object, 상태 enum, 도메인 행위 메서드를 작성하는 전략을 정리한다.

## 목적

- 도메인 모델을 외부 프레임워크와 저장소 구조에서 분리한다.
- 생성, 복원, 상태 변경 경로를 도메인 객체 내부에 명시한다.
- 외부 계층이 도메인 상태를 꺼내 판단하지 않게 한다.

## 적용 범위

- Entity와 Value Object 정의
- 정적 팩토리 메서드와 복원 경로
- 도메인 상태 전이와 비즈니스 판단 메서드
- 도메인 모델의 불변성, 동등성, 외부 의존 제한

도메인 예외 계층과 ErrorCode 설계는 [exception-convention](exception-convention.md)이 소유한다.

## 책임

- 도메인 언어로 비즈니스 개념과 상태를 표현한다.
- 생성 시점과 복원 시점의 검증 범위를 분리한다.
- 상태 변경을 행위 메서드로 캡슐화한다.
- Entity와 Value Object의 동등성 기준을 명확히 한다.

## 전체 흐름

```text
application
  -> Domain factory
    -> create | reconstitute | of | from
  -> Domain behavior
    -> validate state
    -> change state
    -> expose business query method
```

## 세부 규칙

### 외부 의존

- 도메인 모델은 순수 Kotlin / Java 표준 라이브러리만 사용한다.
- Spring, JPA, Jackson, HTTP 타입을 import하지 않는다.
- 도메인 모델과 JPA Entity 변환은 `internal/persistence` adapter가 소유한다.

```kotlin
// 금지
import org.springframework.stereotype.Component
import jakarta.persistence.Entity
import com.fasterxml.jackson.annotation.JsonProperty

// 허용
import java.time.LocalDateTime
import java.util.UUID
```

### 모델 종류

- Entity는 식별자 기준 동등성을 갖는 `class`로 정의한다.
- Value Object는 값 기준 동등성을 갖는 `data class`로 정의한다.
- 상태 enum은 도메인 행위 메서드 내부에서 해석한다.

```kotlin
class Order private constructor(
    val id: Long,
    val customerId: Long,
    private var _status: OrderStatus,
) {
    val status: OrderStatus get() = _status

    companion object {
        fun create(customerId: Long): Order {
            require(customerId > 0) { "customerId must be positive." }
            return Order(0L, customerId, OrderStatus.PENDING)
        }

        fun reconstitute(id: Long, customerId: Long, status: OrderStatus): Order =
            Order(id, customerId, status)
    }

    fun confirm() {
        check(_status == OrderStatus.PENDING) { "Only pending orders can be confirmed." }
        _status = OrderStatus.CONFIRMED
    }

    fun canCancel(): Boolean = _status != OrderStatus.SHIPPED

    override fun equals(other: Any?) = other is Order && id == other.id
    override fun hashCode() = id.hashCode()
}
```

### 팩토리 메서드

| 메서드명 | 용도 |
|---------|------|
| `create(...)` | 신규 도메인 객체 생성, 불변식 전체 적용 |
| `reconstitute(...)` | 저장된 데이터에서 복원, 생성 시점 규칙 생략 가능 |
| `of(...)` | Value Object 생성 |
| `from(...)` | 다른 표현에서 도메인 타입으로 변환 |

- `private constructor`와 `companion object` 팩토리 메서드를 기본으로 한다.
- 신규 생성은 `create`, 저장소 복원은 `reconstitute`로 분리한다.
- `init` 블록으로 모든 생성 경로에 같은 검증을 강제하지 않는다.

### 불변성과 상태 변경

- 필드는 `val`을 기본으로 한다.
- 상태 전이가 필요한 Entity만 내부 `private var`를 사용할 수 있다.
- 외부에는 `val` getter로만 노출하고 변경은 행위 메서드로 수행한다.
- `copy()`로 불변식을 우회할 수 있는 Value Object는 private constructor와 factory를 함께 사용한다.

### Tell Don't Ask

- 외부 계층이 enum이나 내부 상태를 직접 비교해 비즈니스 판단을 내리지 않는다.
- 상태 판단은 `is{State}()`, `can{Action}()`, `requires{Noun}()`, `has{Noun}()` 같은 도메인 메서드로 표현한다.

```kotlin
// 금지
if (order.status == OrderStatus.PENDING) {
    order.cancel()
}

// 권장
if (order.canCancel()) {
    order.cancel()
}
```

### 도메인 예외

- 입력값 전제조건은 `require`를 사용한다.
- 객체 상태 전제조건은 `check`를 사용한다.
- 클라이언트에 구조화된 실패로 전달해야 하는 비즈니스 규칙 위반은 `CoreException(errorCode)`를 사용한다.

## 금지 규칙

- Spring, JPA, Jackson, HTTP 타입을 도메인 모델에 import하지 않는다.
- 생성자를 public으로 노출하지 않는다.
- 비즈니스 검증을 `init` 블록에 몰아넣지 않는다.
- 외부에서 변경 가능한 public setter 또는 public `var`를 열지 않는다.
- 도메인 모델이 다른 도메인 모델을 직접 포함하지 않는다.
- 외부 계층에서 enum 또는 상태 값을 직접 비교해 비즈니스 판단을 내리지 않는다.
- Entity 동등성을 모든 필드 값 기준으로 정의하지 않는다.
- Value Object에 식별자 기반 동등성을 섞지 않는다.

## 예외와 경계

- 단순 매핑 또는 로깅을 위한 상태 값 노출은 가능하지만, 비즈니스 판단은 도메인 메서드로 옮긴다.
- 저장소 복원 시 과거 데이터가 현재 생성 규칙을 만족하지 않을 수 있으면 `reconstitute`에서 생성 시점 검증을 생략할 수 있다.
- 여러 aggregate를 조합해야 하는 규칙은 Domain이 아니라 application Service 또는 Coordinator에서 조합한다.

## 완료 기준

- 도메인 모델이 외부 framework 타입 없이 작성되어 있다.
- 생성과 복원 경로가 factory method 이름으로 구분된다.
- 상태 변경이 도메인 행위 메서드로만 가능하다.
- 비즈니스 상태 판단이 Tell Don't Ask 방식으로 캡슐화되어 있다.
