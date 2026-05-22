# Validator 컨벤션

이 문서는 조회된 데이터와 입력값으로 비즈니스 규칙을 검증하는 `Validator` 전략을 정리한다.

## 목적

- 검증 규칙을 Service, Facade, Coordinator 내부 흐름에서 분리한다.
- 조회 책임과 규칙 판단 책임을 섞지 않는다.
- 같은 입력으로 판단 가능한 비즈니스 규칙을 재사용 가능한 단위로 만든다.

## 적용 범위

- command 처리 중 필요한 비즈니스 규칙 검증
- UseCase 전체 실행 전 확인해야 하는 선행 조건 검증
- 여러 Service 또는 UseCase 구현체에서 공유되는 규칙 검증

입력 형식 검증은 Command 생성 시점이 담당한다. Domain 불변식은 Domain 객체가 담당한다.
하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 책임

- 이미 조회된 domain 객체, 값, 상태를 받아 규칙을 판단한다.
- 규칙 위반 시 application이 사용하는 예외로 실패를 표현한다.
- 상태 변경, 데이터 조회, 외부 시스템 호출은 수행하지 않는다.

## 전체 흐름

```text
Service / Facade / Coordinator
  -> Port.find
  -> Validator
  -> Domain command method
```

## 세부 규칙

### 의존성

- Validator는 Port를 주입받지 않는다.
- Validator는 다른 Validator를 단순 조합하기 위해 존재하지 않는다.
- Validator는 Domain 객체와 값 타입만 받아 검증한다.

### 호출 위치

- Service 내부 command 처리 규칙은 Service에서 호출한다.
- UseCase 전체 선행 조건은 Facade 또는 Coordinator에서 호출할 수 있다.
- 검증에 필요한 데이터는 호출 측이 Port로 조회한 뒤 Validator에 전달한다.

### 메서드 경계

- 같은 입력과 같은 컨텍스트로 판단 가능한 규칙은 하나의 public 메서드로 묶는다.
- 중간에 Port 조회, Strategy 선택, 외부 호출이 필요하면 public 메서드를 분리한다.
- 생성, 수정, 삭제처럼 적용 규칙이 다르면 메서드를 분리한다.

### DTO 경계

- Validator는 이미 조회된 Domain 객체, Domain value, UseCase `Command`, primitive를 받을 수 있다.
- Validator 호출만을 위해 별도 검증 DTO를 만들지 않는다.
- Validator는 DTO를 반환하지 않고 성공 또는 application 예외로 결과를 표현한다.

## 금지 규칙

- Validator에 Port, repository, 외부 API client, messaging client를 주입하지 않는다.
- Validator가 데이터를 직접 조회하거나 저장하지 않는다.
- Validator가 Domain 객체 상태를 변경하지 않는다.
- 여러 Validator를 순서대로 호출만 하는 UseCase 전용 Validator를 만들지 않는다.
- 입력 형식 검증, 존재 여부 확인, 비즈니스 규칙 검증을 하나의 숨겨진 검증 메서드로 뭉치지 않는다.
- Validator 호출을 위해 `ValidatorCommand`, `ValidationRequest`, `ValidationResultDto`를 만들지 않는다.
- Validator가 UseCase `Result`나 `app/api` Response DTO를 반환하지 않는다.

## 예외와 경계

- 단순 존재 여부 확인은 호출 측에서 직접 처리할 수 있다.
- Validator가 Port를 필요로 한다면 조회 책임을 호출 측으로 올린다.
- UseCase 전용 Validator처럼 여러 검증을 순서대로 호출만 하는 묶음은 만들지 않는다.

## 완료 기준

- Validator는 Port와 infrastructure 구현체에 의존하지 않는다.
- 검증에 필요한 데이터 조회가 호출 흐름에 드러난다.
- Validator는 상태 변경 없이 규칙 판단만 수행한다.
