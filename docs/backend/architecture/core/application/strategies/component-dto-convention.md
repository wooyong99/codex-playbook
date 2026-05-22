# Component DTO 컨벤션

이 문서는 application 하위 컴포넌트 사이에서 DTO를 만들지 말지 판단하는 기준을 정리한다.

## 목적

- UseCase 외부 계약 DTO와 application 내부 전달 객체를 혼동하지 않게 한다.
- Service, Validator, Strategy 사이에 기계적인 DTO 복사를 만들지 않는다.
- DTO가 필요할 때도 컴포넌트 이름이 아니라 업무 개념 이름으로 경계를 드러낸다.

## 적용 범위

- Facade, Coordinator, Service, Validator, Strategy, Mapper, Port 사이의 인자와 반환 타입
- Service의 입력과 출력 타입
- application 내부 DTO 예외 생성 기준

HTTP Request/Response DTO는 `app/api`가 소유한다. 외부 API DTO는 `external/integration` adapter가 소유한다. JPA Entity와 QueryDsl 타입은 `internal/persistence` adapter가 소유한다.

## 책임

- UseCase `Command` / `Result`와 내부 전달 타입의 경계를 정의한다.
- 하위 컴포넌트 간 DTO 생성 금지 기준과 예외 기준을 정의한다.
- DTO를 둘 위치와 이름을 제한한다.

## 전체 흐름

```text
UseCase Command
  -> Facade | Coordinator | Service
    -> Service | Validator | Strategy | Port
      -> Domain object | Domain value | primitive | internal outcome exception
    -> Mapper
      -> UseCase Result
```

`Result`는 UseCase 반환 계약이다. Service, Validator, Strategy는 기본적으로 `Result`를 만들거나 반환하지 않는다.

## 세부 규칙

### 기본 원칙

- application 하위 컴포넌트 사이에는 별도 DTO를 기본값으로 만들지 않는다.
- 같은 operation 내부에서는 UseCase `Command`, Domain 객체, Domain value, 식별자, primitive, collection을 그대로 전달한다.
- Service는 application `Result`가 아니라 Domain 객체, Domain value, 또는 예외 승인된 내부 outcome을 반환한다.
- Validator와 Strategy는 필요한 데이터만 인자로 받는다.
- Mapper가 Domain 객체와 application DTO 사이의 변환을 담당한다.

### Service 입출력

- Service 입력은 같은 operation의 UseCase `Command` 또는 command 처리에 필요한 Domain 객체와 값으로 둔다.
- Service 출력은 저장된 aggregate, 변경된 Domain 객체, Domain value를 기본값으로 한다.
- 하나의 Domain 객체로 표현되지 않는 command 처리 결과만 내부 outcome 예외로 둘 수 있다.
- Service 결과를 UseCase `Result`로 바꾸는 책임은 Mapper 또는 UseCase 구현체의 Mapper 호출 흐름이 가진다.

### 내부 DTO 예외 조건

내부 DTO는 아래 조건 중 하나 이상을 만족할 때만 만든다.

- 둘 이상의 application 컴포넌트가 같은 업무 개념 입력 또는 출력을 공유한다.
- 단순 parameter 나열로는 의미가 숨고, 하나의 업무 개념 이름으로 묶어야 흐름이 명확해진다.
- 반환값이 Domain 객체나 Domain value 하나로 표현되지 않는 command outcome이다.
- 다른 개념 영역을 보호하는 Port 경계에서 anti-corruption 언어가 필요하다.

내부 DTO를 만들 때는 아래 규칙을 따른다.

- 이름은 `OrderServiceRequest`, `ValidatorCommand`, `StrategyContextDto`처럼 컴포넌트 이름을 쓰지 않는다.
- 이름은 `PriceCalculationInput`, `AuthorizationDecision`, `OrderCommandOutcome`처럼 업무 개념을 드러낸다.
- 한 컴포넌트에서만 쓰이면 파일로 분리하지 않고 해당 컴포넌트 내부 private 타입으로 둔다.
- 여러 컴포넌트가 공유하면 `dto/internal/` 아래에 두고 예외 사유를 코드 리뷰에서 설명할 수 있어야 한다.

### Port 결과 타입

- Port는 외부 자원 실패와 상태를 표현하기 위해 Port 전용 `Result`, `Status`, `ErrorCode`를 가질 수 있다.
- Port 전용 결과 타입은 외부 스키마 번역을 위한 경계이며 Service 전용 DTO 대체물이 아니다.
- Port 전용 타입에도 JPA Entity, QueryDsl 타입, 외부 API DTO, 외부 SDK 타입을 노출하지 않는다.

## 금지 규칙

- Service, Validator, Strategy를 호출하기 위해 `ServiceCommand`, `ServiceResult`, `ValidatorDto`, `StrategyDto` 같은 컴포넌트 전용 DTO를 만들지 않는다.
- UseCase `Command`를 `ServiceCommand`, `ValidatorCommand`, `StrategyCommand`로 기계적으로 복사하지 않는다.
- Service, Validator, Strategy가 UseCase `Result` 또는 `app/api` Response DTO를 반환하지 않는다.
- Service, Validator, Strategy 내부에서 UseCase `Result`를 조립하지 않는다.
- Mapper를 우회하기 위해 컴포넌트별 DTO 변환 함수를 private helper로 흩뜨리지 않는다.
- 단순 parameter 전달을 줄이기 위한 목적만으로 내부 DTO를 만들지 않는다.
- 내부 DTO를 `common`, `shared`, `util`에 두어 소유권을 숨기지 않는다.
- 외부 API DTO, HTTP DTO, persistence Entity를 내부 DTO처럼 application 컴포넌트 사이에 전달하지 않는다.

## 예외와 경계

- parameter가 많아도 한 번만 쓰이고 업무 개념 이름이 없다면 DTO를 만들지 않는다.
- 내부 DTO가 여러 컴포넌트에서 재사용되기 시작하면 `dto/internal/`로 이동할 수 있다.
- 내부 DTO가 Domain 불변식이나 상태를 표현하기 시작하면 Domain value object로 옮기는 것을 우선 검토한다.
- Query 결과 조립 DTO가 필요하면 Query Facade와 Mapper 책임을 먼저 검토한다.

## 완료 기준

- UseCase 외부 계약 DTO와 application 내부 전달 타입이 구분된다.
- Service는 UseCase `Result`를 반환하지 않는다.
- 하위 컴포넌트 간 DTO는 기본 금지이며, 예외가 업무 개념 이름과 위치로 설명된다.
- DTO 변환은 Mapper에 모여 있고 컴포넌트별 복사 DTO 체인이 없다.
