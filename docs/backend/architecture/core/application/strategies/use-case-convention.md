# UseCase 컨벤션

이 문서는 `application` 단위가 외부에 공개하는 `UseCase` 추상 인터페이스 전략을 정리한다.

## 목적

- app, event, CLI 같은 외부 진입점이 application 구현체가 아니라 추상 계약에 의존하게 한다.
- 업무 기능의 입력과 출력을 `Command` / `Result` 계약으로 고정하되, UseCase 파일 수는 Command/Query 단위로 제어한다.
- `Facade`, `Coordinator`, `Service` 구현체를 외부 호출자에게 노출하지 않는다.

## 적용 범위

- Controller, EventListener, CLI Adapter가 호출하는 application 경계
- 외부 요청을 application 내부 실행 전략으로 연결하는 추상 인터페이스
- application 내부 DTO인 `Command`, `Result` 계약

UseCase 구현 방식은 이 문서가 아니라 [facade-convention](facade-convention.md), [coordinator-convention](coordinator-convention.md), [service-convention](service-convention.md)이 소유한다.
하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)이 소유한다.

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

UseCase는 추상 인터페이스다. 기본 네이밍은 `{Entity}CommandUseCase`와 `{Entity}QueryUseCase`다.

```kotlin
interface OrderCommandUseCase {
    fun create(command: CreateOrder.Command): CreateOrder.Result
    fun cancel(command: CancelOrder.Command): CancelOrder.Result
}

interface OrderQueryUseCase {
    fun get(id: Long): GetOrder.Result
    fun search(command: SearchOrder.Command): SearchOrder.Result
}
```

- 구현체를 직접 타입으로 노출하지 않는다.
- 외부 진입점은 `OrderCommandUseCase`, `OrderQueryUseCase` 같은 인터페이스만 주입받는다.
- UseCase 인터페이스는 다른 UseCase를 호출하지 않는다.
- 같은 entity라도 Query와 Command는 별도 UseCase로 나눈다.
- 세부 action은 UseCase 파일을 늘리지 않고 메서드로 표현한다.

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

- 파일명은 `dto/{Action}{Entity}.kt`를 사용한다.
- Command `init`에는 값 존재 여부, 길이, 형식 같은 입력 형식 검증만 둔다.
- DB 조회, 권한, 중복, 정책 검증은 UseCase 구현체 또는 Service에서 처리한다.
- 같은 operation 내부에서는 UseCase `Command`를 Service, Validator, Strategy에 그대로 전달할 수 있다.
- UseCase `Result`는 외부 반환 계약이며 Service, Validator, Strategy의 반환 타입으로 사용하지 않는다.

### 구현체 선택

UseCase 구현체는 책임으로 결정하되, 이름은 구현하는 Command/Query 계약과 맞춘다.

| 구현체 | 선택 기준 |
|--------|-----------|
| `{Entity}CommandFacade` | Command UseCase에서 여러 도메인 세부 구조를 감출 때 |
| `{Entity}CommandCoordinator` | Command UseCase에서 여러 트랜잭션, 이벤트, 외부 시스템, 비동기 확장 가능성을 조합할 때 |
| `{Entity}CommandService` | Command UseCase에서 하나의 aggregate command를 원자적으로 처리할 때 |
| `{Entity}QueryFacade` | Query UseCase에서 여러 조회와 결과 조립을 감출 때 |

## 금지 규칙

- UseCase 인터페이스에 구현 로직을 넣지 않는다.
- UseCase 인터페이스가 다른 UseCase를 호출하거나 의존하지 않는다.
- UseCase 계약에 HTTP Request/Response DTO, JPA Entity, 외부 API DTO를 노출하지 않는다.
- Command `init`에서 Port 조회, 권한 확인, 중복 확인, 정책 판단을 수행하지 않는다.
- 외부 진입점이 Facade, Coordinator, Service 구현체를 직접 주입받게 하지 않는다.
- action마다 `{Action}{Entity}UseCase` 파일을 기본값으로 만들지 않는다.
- UseCase `Command`를 컴포넌트별 `ServiceCommand`, `ValidatorCommand`, `StrategyCommand`로 복사하지 않는다.
- Service, Validator, Strategy가 UseCase `Result`를 만들거나 반환하게 하지 않는다.

## 예외와 경계

- 프로젝트가 작고 구현체가 하나뿐이면 인터페이스와 구현체 분리를 늦출 수 있다.
- 외부 진입점이 둘 이상이거나 구현체 교체 가능성이 있으면 UseCase 인터페이스를 먼저 둔다.
- 특정 action이 별도 권한, 별도 actor, 별도 배포 경계, 독립적인 외부 계약을 가지면 action 단위 UseCase 분리를 검토할 수 있다.

## 완료 기준

- 외부 진입점이 구현체가 아니라 UseCase 인터페이스를 참조한다.
- Command와 Result가 application 내부 계약으로 정의되어 있다.
- UseCase 계약이 Command/Query 단위로 나뉘고, 구현체 책임이 Facade, Coordinator, Service 중 하나로 설명된다.
