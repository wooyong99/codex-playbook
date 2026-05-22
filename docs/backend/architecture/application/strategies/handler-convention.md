# Handler 컨벤션

이 문서는 여러 개념 영역에서 재사용되는 로직과 경계 보호를 담당하는 `Handler` 전략을 정리한다.

## 목적

- 여러 Service, Facade, Coordinator에서 반복되는 조합 로직을 한곳에 모은다.
- 한 개념 영역이 다른 개념 영역의 Port나 세부 모델에 직접 결합되지 않게 한다.
- application 내부의 재사용 로직과 anti-corruption 경계를 명확히 한다.

## 적용 범위

- 파일 첨부, 알림, 공통 ACL처럼 여러 개념 영역에서 반복되는 application 로직
- 다른 도메인 Port 접근을 감싸야 하는 경계 보호 로직
- 여러 Port 또는 domain 객체를 조합하지만 독립 UseCase는 아닌 로직

하나의 aggregate command 원자성은 [service-convention](service-convention.md)이 소유한다. 여러 트랜잭션 조합은 [coordinator-convention](coordinator-convention.md)이 소유한다.

## 책임

- 재사용되는 application 로직을 캡슐화한다.
- 다른 개념 영역의 Port 변경이 Service나 Coordinator에 직접 전파되지 않도록 막는다.
- 필요한 Port와 Domain 객체를 조합하되 UseCase 구현체를 호출하지 않는다.

## 전체 흐름

```text
Service / Facade / Coordinator
  -> Handler
    -> Port
    -> Domain
```

## 세부 규칙

### 추출 기준

- 여러 개념 영역에서 같은 로직이 반복되면 Handler로 추출한다.
- 다른 개념 영역의 Port 접근이 필요하면 Handler로 경계를 만든다.
- 여러 Port 또는 domain 객체 조합이 재사용되면 Handler로 추출한다.

### 의존성

- Handler는 Port와 Domain 객체를 사용할 수 있다.
- Handler는 UseCase, Facade, Coordinator, Service를 호출하지 않는다.
- Handler는 다른 Handler를 연쇄 호출하지 않는 것을 기본값으로 한다.

### 사용 위치

- Service는 command 처리 중 필요한 재사용 로직을 Handler에 위임할 수 있다.
- Coordinator는 단계 조합 중 필요한 경계 보호 로직을 Handler에 위임할 수 있다.
- Facade는 조회 또는 결과 조합 중 반복되는 접근 로직을 Handler에 위임할 수 있다.

## 금지 규칙

- 단일 Port 호출만 감싸는 Handler를 만들지 않는다.
- Handler가 UseCase, Facade, Coordinator, Service를 호출하지 않는다.
- 한 Service에서만 쓰이는 로직을 Handler로 추출하지 않는다.
- Handler에 도메인 불변식이나 aggregate 상태 변경 규칙을 직접 구현하지 않는다.
- Handler를 여러 Handler의 연쇄 호출 구조로 만들지 않는다.

## 예외와 경계

- 한 Service에서만 쓰이는 로직은 Service의 private 메서드로 유지한다.
- 비즈니스 불변식은 Handler가 아니라 Domain 또는 Validator가 담당한다.

## 완료 기준

- Handler는 재사용 또는 경계 보호 목적이 분명하다.
- Handler가 UseCase 구현체를 호출하지 않는다.
- 다른 개념 영역 Port 접근이 Service나 Coordinator에 직접 흩어져 있지 않다.
