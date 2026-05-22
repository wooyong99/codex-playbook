# Strategy 컨벤션

이 문서는 정책에 따라 처리 방식이 달라지는 지점을 캡슐화하는 `Strategy` 전략을 정리한다.

## 목적

- 조건 분기별 처리 방식을 독립된 구현체로 분리한다.
- 신규 정책 추가 시 기존 Service 또는 Coordinator 코드를 덜 수정하게 한다.
- 정책 선택 기준과 실행 알고리즘을 한 컴포넌트에 모은다.

## 적용 범위

- 결제, 배송, 할인, 권한, 정산, 할당처럼 정책 유형이 늘어날 가능성이 있는 분기
- 같은 입력을 정책별로 다르게 처리하는 application 로직
- 구현체 위치가 의존성에 따라 application 또는 infrastructure로 갈릴 수 있는 전략

하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 책임

- 특정 정책 유형을 자신이 처리할 수 있는지 판단한다.
- 처리 알고리즘을 실행한다.
- 호출자가 정책별 세부 분기를 알지 않게 한다.

## 전체 흐름

```text
Service / Coordinator
  -> List<Strategy>
    -> supports(context)
    -> execute(context)
```

## 세부 규칙

### 선택 기준

- 정책 유형이 둘 이상이고 추가 가능성이 있다.
- 각 정책의 알고리즘이 독립적으로 변경될 수 있다.
- 단순 `when` 분기가 Service의 핵심 흐름을 가린다.

### 디스패치

- `List<Strategy>` 주입과 `supports()` 패턴을 기본으로 한다.
- 호출자가 구현체 이름이나 순서를 직접 알지 않게 한다.
- 지원하는 Strategy가 없으면 application 예외로 실패시킨다.

### 구현체 위치

- 외부 의존이 없는 순수 계산은 application에 둔다.
- DB 조회가 필요하면 `internal/persistence` 또는 관련 infrastructure 구현체로 둔다.
- 외부 API 호출이 필요하면 external 구현체로 둔다.

### DTO 경계

- Strategy 입력은 정책 판단에 필요한 Domain 객체, Domain value, UseCase `Command`, primitive로 둔다.
- 정책 알고리즘 결과가 업무 개념이면 Domain value 또는 예외 승인 내부 outcome으로 표현한다.
- Strategy 선택과 실행만을 위한 Strategy 전용 DTO를 만들지 않는다.

## 금지 규칙

- 확장 가능성이 낮은 단순 분기를 성급하게 Strategy로 분리하지 않는다.
- Strategy가 UseCase를 호출하지 않는다.
- Strategy가 aggregate 저장, 트랜잭션 경계, 전체 command 처리를 소유하지 않는다.
- Strategy 선택을 호출 측의 복잡한 `when` 분기로 흩뜨리지 않는다.
- Strategy 인터페이스에 외부 API DTO, JPA Entity, framework 타입을 노출하지 않는다.
- Strategy 호출을 위해 `StrategyCommand`, `StrategyContextDto`, `StrategyResultDto`를 만들지 않는다.
- Strategy가 UseCase `Result`나 `app/api` Response DTO를 반환하지 않는다.

## 예외와 경계

- 정책이 두세 줄짜리 단순 분기이고 확장 가능성이 낮다면 Service 내부 `when`으로 유지한다.
- Strategy가 aggregate 상태를 직접 저장하지 않는다. 저장 책임은 Service가 가진다.

## 완료 기준

- 정책별 처리 방식이 구현체로 분리되어 있다.
- 호출자는 `supports()` 또는 동등한 선택 메서드로 Strategy를 선택한다.
- 신규 정책 추가 시 기존 핵심 흐름의 수정 범위가 작다.
