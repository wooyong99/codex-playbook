# Service 컨벤션

이 문서는 aggregate command를 원자적으로 처리하는 application `Service` 전략을 정리한다.

## 목적

- 하나의 aggregate 상태 변경을 조회, 검증, 도메인 행위, 저장까지 한 트랜잭션으로 처리한다.
- application 실행 단위에서 원자성과 도메인 불변식을 보호한다.
- UseCase 구현체가 command 처리 세부 절차를 직접 품지 않게 한다.

## 적용 범위

- 하나의 aggregate command를 처리하는 application service
- 상태 변경이 있고 트랜잭션 경계가 필요한 업무 실행 단위
- Port, Validator, Strategy, Handler, Domain 메서드를 조합하는 command 처리 흐름

## 책임

- command 처리에 필요한 aggregate를 Port로 조회한다.
- 조회된 데이터와 command를 Validator로 검증한다.
- 정책 분기가 필요하면 Strategy에 위임한다.
- 다른 개념 영역의 재사용 로직은 Handler에 위임한다.
- 실제 상태 변경은 Domain 객체의 메서드로 수행하고 Port로 저장한다.

## 전체 흐름

```text
UseCase implementation
  -> Service
    -> Port.find
    -> Validator
    -> Strategy
    -> Handler
    -> Domain command method
    -> Port.save
```

## 세부 규칙

### 처리 순서

1. command 형식 검증은 Command 생성 시점에 끝낸다.
2. Service는 Port로 command 처리에 필요한 aggregate를 조회한다.
3. Validator는 조회된 데이터와 command로 규칙을 검증한다.
4. Strategy는 정책별 처리 방식을 선택한다.
5. Handler는 다른 개념 영역의 재사용 로직을 처리한다.
6. Domain 객체 메서드로 상태를 변경한다.
7. Port로 저장하고 변경된 domain 객체를 반환한다.

### 트랜잭션

- 쓰기 Service는 하나의 트랜잭션 경계를 가진다.
- 읽기 전용 Service라면 `readOnly` 경계를 사용하거나 UseCase/Facade 조회로 유지한다.
- 외부 API, 파일 I/O, 메시징 같은 장기 작업은 Service 트랜잭션 안에 넣지 않는다.

### Validator

- Validator는 Port를 주입받지 않는다.
- Service가 필요한 데이터를 조회한 뒤 Validator에 전달한다.
- 단순 존재 여부 확인은 Service에서 직접 처리할 수 있다.

## 금지 규칙

- Service가 다른 Service를 순차 조합하지 않는다. 여러 Service 조합은 Coordinator로 올린다.
- 외부 API, 파일 I/O, 메시징 같은 장기 작업을 Service 트랜잭션 안에서 수행하지 않는다.
- Domain 불변식이나 상태 판단을 Service에 직접 구현하지 않는다.
- Application Result DTO 조립을 Service에서 수행하지 않는다. DTO 변환은 Mapper를 사용한다.
- 단일 Port 호출만을 위해 별도 Service를 만들지 않는다.

## 예외와 경계

- 여러 aggregate command를 순차 조합하면 Coordinator로 올린다.
- 여러 도메인 뒤의 구조를 감추는 조회성 조합이면 Facade로 올린다.
- 단일 Port 호출만 있다면 별도 Service를 만들지 않고 UseCase 구현체에서 직접 호출할 수 있다.
- Domain 불변식은 Service에 구현하지 않고 Domain 객체로 내린다.

## 완료 기준

- 하나의 aggregate command가 하나의 원자적 Service 경계에서 처리된다.
- Service는 Port, Validator, Strategy, Handler를 조합하되 도메인 판단을 직접 구현하지 않는다.
- 외부 시스템 호출이 Service 트랜잭션 안에 포함되지 않는다.
