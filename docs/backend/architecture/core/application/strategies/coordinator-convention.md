# Coordinator 컨벤션

이 문서는 여러 트랜잭션 흐름, 이벤트, 외부 시스템 호출을 조합하는 `Coordinator` 전략을 정리한다.

## 목적

- 독립적인 application 실행 단위를 한 UseCase 흐름으로 조합한다.
- 트랜잭션 내부 작업과 커밋 이후 부수 효과를 명확히 나눈다.
- 동기 흐름을 나중에 이벤트, outbox, job queue 같은 비동기 구조로 확장할 수 있게 한다.

## 적용 범위

- 여러 Service 실행 결과를 순서대로 조합하는 UseCase 구현체
- DB 커밋 이후 이벤트 발행, 알림, 외부 API, 메시징이 이어지는 흐름
- 지금은 동기 처리지만 비동기 전환 가능성이 높은 application 절차

하나의 aggregate command를 한 트랜잭션으로 처리하는 경우는 [service-convention](service-convention.md)을 따른다.
하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 책임

- 주로 `CommandUseCase` 인터페이스를 구현한다.
- 어떤 작업이 같은 트랜잭션에 묶이고 어떤 작업이 커밋 이후로 분리되는지 결정한다.
- Service, 이벤트 발행, 외부 Port 호출의 순서를 조율한다.
- 외부 시스템 호출 실패가 핵심 트랜잭션에 미치는 영향을 정책으로 드러낸다.

## 전체 흐름

```text
{Entity}CommandUseCase
  -> {Entity}CommandCoordinator
    -> Service transaction A
    -> Service transaction B
    -> publish event / call external port
    -> Mapper
```

## 세부 규칙

### 선택 기준

- 여러 원자적 작업을 하나의 사용자 요청으로 묶어야 한다.
- 커밋 후 이벤트 또는 외부 시스템 호출이 있다.
- 실패 보상, 재시도, 비동기 전환 가능성을 고려해야 한다.
- 하나의 큰 트랜잭션보다 작은 트랜잭션들의 조합이 더 안전하다.
- 같은 entity의 Command 조율 흐름은 기본적으로 `{Entity}CommandCoordinator`에 메서드로 묶는다.

### 트랜잭션 경계

- Coordinator 전체에 넓은 `@Transactional`을 거는 것은 예외로 둔다.
- 원자성이 필요한 변경은 Service 내부 트랜잭션으로 처리한다.
- 외부 API, 파일 I/O, 메시징은 DB 커밋 이후 실행하도록 분리한다.
- 커밋 이후 처리는 필요하면 `@TransactionalEventListener(phase = AFTER_COMMIT)` 또는 outbox로 옮긴다.

### 의존 규칙

- Coordinator는 주로 CommandUseCase를 구현한다.
- Coordinator가 다른 UseCase를 호출하지 않는다.
- Coordinator는 Service, Port, Mapper를 조합할 수 있다.
- 도메인 상태 변경 규칙은 Coordinator에 직접 구현하지 않고 Service 또는 Domain으로 내린다.

### DTO 경계

- Coordinator는 단계 간 전달값을 Domain 객체, Domain value, Service outcome으로 유지한다.
- 여러 Service 결과를 UseCase `Result`로 변환하는 책임은 Mapper 호출 흐름에 둔다.
- 단계 연결만을 위한 Coordinator 전용 DTO를 기본값으로 만들지 않는다.

## 금지 규칙

- 외부 API, 파일 I/O, 메시징 호출을 긴 DB 트랜잭션 안에서 수행하지 않는다.
- 독립적인 여러 Service 단계를 하나의 큰 트랜잭션으로 묶지 않는다.
- Coordinator가 다른 UseCase를 호출하지 않는다.
- Coordinator에 aggregate 상태 변경 규칙이나 도메인 불변식을 직접 구현하지 않는다.
- 커밋 이후 부수 효과의 실패 정책을 숨긴 채 호출만 추가하지 않는다.
- 단계 연결을 위해 `CoordinatorStepDto`, `ServiceResultDto`, `NextServiceCommand` 같은 DTO를 만들지 않는다.
- Coordinator 또는 Service가 UseCase `Result`를 조립하게 하지 않는다.
- action마다 `{Action}{Entity}Coordinator` 파일을 기본값으로 만들지 않는다.

## 예외와 경계

- 여러 단계가 반드시 하나의 원자성을 가져야 하면 Coordinator가 아니라 하나의 Service 경계로 재설계한다.
- 단순히 여러 조회 결과를 감추는 책임이면 Facade가 더 적합하다.
- 비동기 전환이 확정된 흐름은 이벤트 발행, outbox, job queue 책임을 함께 설계한다.

## 완료 기준

- 트랜잭션 내부 작업과 커밋 이후 작업이 분리되어 있다.
- 외부 시스템 호출이 긴 DB 트랜잭션 안에 들어가지 않는다.
- 각 단계 실패 시 처리 정책이 코드와 문서에서 드러난다.
- Coordinator 이름이 구현하는 CommandUseCase 계약과 맞춰져 있다.
