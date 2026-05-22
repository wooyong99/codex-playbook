# Facade 컨벤션

이 문서는 여러 도메인 또는 하위 application 컴포넌트의 복잡도를 감추는 `Facade` 전략을 정리한다.

## 목적

- 외부 호출자가 여러 도메인 구조와 내부 조합 순서를 알지 못하게 한다.
- 여러 조회, 검증, 결과 조립을 하나의 UseCase 구현체 뒤에 숨긴다.
- 단일 요청을 이해하기 쉬운 application 진입점으로 제공한다.

## 적용 범위

- 여러 도메인 개념을 읽거나 조합해 하나의 결과를 반환하는 UseCase 구현체
- Controller가 여러 Service, Handler, Port를 직접 알아야 할 때의 경계 정리
- 복잡한 내부 구조를 외부 계약에서 감추는 application facade

트랜잭션 조합, 이벤트, 외부 시스템 호출, 비동기 확장 가능성이 중심이면 [coordinator-convention](coordinator-convention.md)을 우선한다.

## 책임

- `UseCase` 인터페이스를 구현한다.
- 여러 도메인 또는 하위 컴포넌트 호출 순서를 감춘다.
- 결과 조립은 [mapper-convention](mapper-convention.md)에 위임한다.
- 반복되는 경계 보호 로직은 [handler-convention](handler-convention.md)로 내린다.

## 전체 흐름

```text
UseCase interface
  -> Facade implementation
    -> Service / Handler / Port
    -> Mapper
```

## 세부 규칙

### 선택 기준

- 한 요청이 여러 도메인 정보를 조합하지만 원자적 상태 변경은 중심이 아니다.
- 외부 호출자가 내부 도메인 구조를 알면 결합이 커진다.
- 단일 UseCase 결과를 만들기 위해 여러 하위 컴포넌트 호출이 필요하다.

### 트랜잭션

- Facade는 넓은 트랜잭션을 기본값으로 갖지 않는다.
- 하나의 aggregate command 원자성이 필요하면 [service-convention](service-convention.md)으로 분리한다.
- 여러 트랜잭션 단계를 조합해야 하면 [coordinator-convention](coordinator-convention.md)으로 분리한다.

### 의존 규칙

- Facade는 UseCase를 구현할 수 있다.
- Facade가 다른 UseCase를 호출하지 않는다.
- Facade가 Port를 직접 참조할 수는 있지만, 반복되거나 도메인 경계를 넘는 접근은 Handler 또는 Service로 내린다.

## 금지 규칙

- 단일 Service 호출만 감싸는 Facade를 만들지 않는다.
- Facade가 다른 UseCase를 호출하지 않는다.
- Facade에 도메인 불변식이나 aggregate 상태 변경 규칙을 직접 구현하지 않는다.
- 편의를 위해 여러 조회와 외부 호출을 하나의 긴 트랜잭션으로 묶지 않는다.
- 결과 조립 로직을 Facade 내부에 반복해서 인라인으로 작성하지 않는다.

## 예외와 경계

- 조회 결과 조립만 복잡한 경우에는 Facade 내부 조합과 Mapper 분리만으로 충분하다.
- Facade가 비즈니스 규칙을 직접 구현하기 시작하면 Service, Validator, Strategy로 책임을 분리한다.

## 완료 기준

- 외부 진입점은 Facade 구현체가 아니라 UseCase 인터페이스에 의존한다.
- 여러 도메인 조합 방식이 Facade 뒤에 숨겨져 있다.
- 반복 로직은 Handler, 변환 로직은 Mapper, 원자적 command 처리는 Service로 분리되어 있다.
