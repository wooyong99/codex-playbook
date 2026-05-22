# Port 컨벤션

이 문서는 repository, 외부 API, messaging 같은 외부 자원 접근을 추상화하는 `Port` 전략을 정리한다.

## 목적

- application이 인프라 구현체와 외부 스키마에 직접 결합되지 않게 한다.
- 저장소, 외부 API, 파일, 메시징 접근을 application 언어의 인터페이스로 표현한다.
- infrastructure 교체와 테스트 대역 구성을 쉽게 한다.

## 적용 범위

- repository 접근 추상화
- 외부 API 호출 추상화
- 파일 스토리지, 메시징, 캐시, 내부 시스템 호출 추상화
- application에서 infrastructure 구현체를 직접 참조하지 않도록 막는 경계

Port 구현체 규칙은 [storage adapter convention](../../storage/strategies/storage-adapter-convention.md), [external adapter convention](../../external/strategies/adapter-convention.md)이 소유한다.
하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 책임

- application이 필요한 작업을 구현 기술이 아닌 업무 언어로 정의한다.
- domain 객체 또는 application 내부 DTO를 입출력으로 사용한다.
- JPA Entity, HTTP DTO, 외부 SDK 타입을 application 경계 밖으로 밀어낸다.

## 전체 흐름

```text
Service / Coordinator / Facade
  -> Port interface
    -> storage / external adapter
```

## 세부 규칙

### 참조 범위

Port는 application 내부 어느 역할에서도 참조할 수 있다.
다만 기본 지향점은 `Service`에 Port 참조를 모으는 것이다.

- Service: aggregate command 처리에 필요한 조회와 저장
- Coordinator: 조율에 필요한 최소 호출만 허용
- Facade: 조회 조합에 필요한 최소 호출만 허용
- Validator: Port 참조 금지
- Mapper: Port 참조 금지

### 시그니처

- application이 이해하는 타입으로 입력과 출력을 정의한다.
- 외부 API 응답 DTO, JPA Entity, QueryDsl 타입을 노출하지 않는다.
- 실패를 표현해야 하면 Port 전용 Result, Status, ErrorCode를 사용한다.
- Port 전용 Result, Status, ErrorCode는 외부 자원 상태 표현에만 사용하고 Service 전용 DTO 대체물로 쓰지 않는다.

### 구현체

- 저장소 Port 구현체는 storage 단위에 둔다.
- 외부 API Port 구현체는 external 단위에 둔다.
- Mock 또는 fake 구현체는 동일 Port를 구현하고 프로필이나 테스트 설정에서 교체한다.

## 금지 규칙

- Port 시그니처에 JPA Entity, QueryDsl 타입, 외부 API DTO, 외부 SDK 타입을 노출하지 않는다.
- application 내부에서 Port 구현체나 infrastructure 클래스를 직접 참조하지 않는다.
- Validator와 Mapper가 Port를 참조하지 않는다.
- 여러 aggregate나 외부 기능을 하나의 비대한 Port로 합치지 않는다.
- Provider, HTTP, SQL 같은 구현 기술 중심 이름으로 Port 계약을 정의하지 않는다.
- Port 시그니처에 `ServiceCommand`, `StrategyDto` 같은 컴포넌트 전용 DTO를 노출하지 않는다.

## 예외와 경계

- 단일 조회가 UseCase 전체 선행 조건이면 Facade 또는 Coordinator에서 직접 Port를 참조할 수 있다.
- 같은 Port 호출이 여러 Service에서 반복되면 Port 계약을 더 작은 업무 기능 단위로 분리한다.
- Port가 비대해지면 aggregate 또는 외부 기능 단위로 분리한다.

## 완료 기준

- application은 infrastructure 구현체가 아니라 Port 인터페이스에 의존한다.
- Port 시그니처에 외부 DTO나 persistence Entity가 노출되지 않는다.
- Port 참조는 가능하면 Service에 모여 있다.
