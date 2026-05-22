# UseCase 컨벤션

이 문서는 `application` 단위가 외부에 공개하는 `UseCase` 추상 인터페이스 전략을 정리한다.

## 목적

- app, event, CLI 같은 외부 진입점이 application 구현체가 아니라 추상 계약에 의존하게 한다.
- 업무 기능의 입력과 출력을 `Command` / `Result` 계약으로 고정한다.
- `Facade`, `Coordinator`, `Service` 구현체를 외부 호출자에게 노출하지 않는다.

## 적용 범위

- Controller, EventListener, CLI Adapter가 호출하는 application 경계
- 외부 요청을 application 내부 실행 전략으로 연결하는 추상 인터페이스
- application 내부 DTO인 `Command`, `Result` 계약

UseCase 구현 방식은 이 문서가 아니라 [facade-convention](facade-convention.md), [coordinator-convention](coordinator-convention.md), [service-convention](service-convention.md)이 소유한다.

## 책임

- 외부 호출자가 사용할 메서드 시그니처를 정의한다.
- 입력은 application 내부 `Command`로 받고 결과는 application 내부 `Result`로 반환한다.
- 구현체 선택과 내부 조합 방식은 감춘다.

## 전체 흐름

```text
app / event / CLI
  -> UseCase interface
    -> Facade | Coordinator | Service implementation
      -> Domain / Port / Mapper
```

## 세부 규칙

### 추상 계약

UseCase는 추상 인터페이스다.

```kotlin
interface CreateOrderUseCase {
    fun create(command: CreateOrder.Command): CreateOrder.Result
}
```

- 구현체를 직접 타입으로 노출하지 않는다.
- 외부 진입점은 `CreateOrderUseCase` 같은 인터페이스만 주입받는다.
- UseCase 인터페이스는 다른 UseCase를 호출하지 않는다.

### Command와 Result

Command와 Result는 operation 단위 파일 하나에 함께 정의한다.

```kotlin
class CreateOrder {
    data class Command(
        val customerId: Long,
        val items: List<OrderItemCommand>,
    )

    data class Result(
        val orderId: Long,
        val status: OrderStatus,
    )
}
```

- 파일명은 `{Action}{Entity}.kt`를 사용한다.
- Command `init`에는 값 존재 여부, 길이, 형식 같은 입력 형식 검증만 둔다.
- DB 조회, 권한, 중복, 정책 검증은 UseCase 구현체 또는 Service에서 처리한다.

### 구현체 선택

UseCase 구현체는 책임으로 결정한다.

| 구현체 | 선택 기준 |
|--------|-----------|
| `Facade` | 여러 도메인이나 하위 컴포넌트를 감추는 단일 진입점이 필요할 때 |
| `Coordinator` | 여러 트랜잭션, 이벤트, 외부 시스템, 비동기 확장 가능성을 조합할 때 |
| `Service` | 하나의 aggregate command를 원자적으로 처리할 때 |

## 금지 규칙

- UseCase 인터페이스에 구현 로직을 넣지 않는다.
- UseCase 인터페이스가 다른 UseCase를 호출하거나 의존하지 않는다.
- UseCase 계약에 HTTP Request/Response DTO, JPA Entity, 외부 API DTO를 노출하지 않는다.
- Command `init`에서 Port 조회, 권한 확인, 중복 확인, 정책 판단을 수행하지 않는다.
- 외부 진입점이 Facade, Coordinator, Service 구현체를 직접 주입받게 하지 않는다.

## 예외와 경계

- 프로젝트가 작고 구현체가 하나뿐이면 인터페이스와 구현체 분리를 늦출 수 있다.
- 외부 진입점이 둘 이상이거나 구현체 교체 가능성이 있으면 UseCase 인터페이스를 먼저 둔다.

## 완료 기준

- 외부 진입점이 구현체가 아니라 UseCase 인터페이스를 참조한다.
- Command와 Result가 application 내부 계약으로 정의되어 있다.
- 구현체 책임이 Facade, Coordinator, Service 중 하나로 설명된다.
