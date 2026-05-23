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

Port 구현체 규칙은 [persistence adapter convention](../../../internal/persistence/strategies/storage-adapter-convention.md), [external integration adapter convention](../../../external/integration/strategies/adapter-convention.md)이 소유한다.
하위 컴포넌트 간 DTO 생성 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 책임

- application이 필요한 작업을 구현 기술이 아닌 업무 언어로 정의한다.
- domain 객체 또는 application 내부 DTO를 입출력으로 사용한다.
- JPA Entity, HTTP DTO, 외부 SDK 타입을 application 경계 밖으로 밀어낸다.

## 전체 흐름

```text
Service / Coordinator / Facade
  -> Port interface
    -> internal/persistence | external/integration adapter
```

## 세부 규칙

### 네이밍

application outbound Port 인터페이스는 이름 끝에 반드시 `Port`를 붙인다.

| Port 종류 | 패턴 | 예시 |
|-----------|------|------|
| 저장소 Port | `{Aggregate}RepositoryPort` | `OrderRepositoryPort` |
| 외부 시스템 Port | `{ProviderOrDomain}{Capability}Port` | `PaymentApprovalPort` |
| 내부 인프라 Port | `{DomainOrCapability}Port` | `SessionTokenPort` |

- `port/` 패키지에 있는 production 인터페이스는 예외 없이 `*Port`로 끝난다.
- 저장소 역할을 추상화할 때 `Store`, `Repository`, `Gateway`, `Provider`만으로 끝나는 이름을 쓰지 않는다.
- 외부 API, 파일, 메시징, 캐시, 토큰, 암호화, 시간, ID 생성처럼 구현 교체 가능한 outbound 경계도 `*Port`로 표현한다.
- 구현체 클래스에는 `Port` suffix를 붙이지 않는다. 구현체는 기술과 역할이 드러나는 `Adapter`, `Repository`, `Client`, `Generator` 등의 이름을 사용한다.
- 기존 코드에 `*Port` suffix가 없는 outbound 인터페이스가 있으면 legacy로 간주하고, 신규 코드나 수정 범위에서는 같은 패턴을 확산하지 않는다.

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

- 저장소 Port 구현체는 `internal/persistence` 단위에 둔다.
- 외부 API Port 구현체는 `external/integration` 단위에 둔다.
- 캐시, 메시징, 파일, 보안, object storage 같은 내부 인프라 Port 구현체는 해당 `internal/*` 단위에 둔다.
- in-memory 구현체도 production runtime에서 bean으로 등록되면 infrastructure adapter로 취급하고 application 밖에 둔다.
- Mock 또는 fake 구현체는 동일 Port를 구현하되 테스트 source나 테스트 설정에서만 교체한다.

## 금지 규칙

- Port 시그니처에 JPA Entity, QueryDsl 타입, 외부 API DTO, 외부 SDK 타입을 노출하지 않는다.
- application outbound Port 인터페이스를 `*Port` suffix 없이 선언하지 않는다.
- `Store`, `Generator`, `Hasher`, `Client`, `Provider`, `Gateway` 같은 구현 또는 역할 이름만으로 Port 계약명을 끝내지 않는다.
- application 내부에서 Port 구현체나 infrastructure 클래스를 직접 참조하지 않는다.
- application production source 아래에 `adapter`, `inmemory`, `jpa`, `http`, `client`, `repository` 같은 구현체 패키지를 만들지 않는다.
- 임시 저장소, 개발용 저장소, in-memory 저장소라는 이유로 Port 구현체를 application 내부에 예외 배치하지 않는다.
- Validator와 Mapper가 Port를 참조하지 않는다.
- 여러 aggregate나 외부 기능을 하나의 비대한 Port로 합치지 않는다.
- Provider, HTTP, SQL 같은 구현 기술 중심 이름으로 Port 계약을 정의하지 않는다.
- Port 시그니처에 `ServiceCommand`, `StrategyDto` 같은 컴포넌트 전용 DTO를 노출하지 않는다.

## 예외와 경계

- 단일 조회가 UseCase 전체 선행 조건이면 Facade 또는 Coordinator에서 직접 Port를 참조할 수 있다.
- 같은 Port 호출이 여러 Service에서 반복되면 Port 계약을 더 작은 업무 기능 단위로 분리한다.
- Port가 비대해지면 aggregate 또는 외부 기능 단위로 분리한다.
- 이미 존재하는 non-`*Port` outbound 인터페이스를 수정 범위에서 만지면 새 이름으로 마이그레이션하거나, 마이그레이션 불가 사유와 후속 작업을 남긴다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 신규 또는 수정된 application outbound 인터페이스 이름이 모두 `*Port`로 끝난다.
- [ ] `port/` 패키지 production 파일에 `Store`, `Generator`, `Hasher`, `Client`, `Provider`, `Gateway`로 끝나는 인터페이스가 새로 추가되지 않았다.
- [ ] application은 infrastructure 구현체가 아니라 Port 인터페이스에 의존한다.
- [ ] Port 구현체의 production package가 `core.application`이 아니라 `internal/*` 또는 `external/*` 하위 adapter 위치에 있다.
- [ ] in-memory 구현체가 production에서 사용된다면 application 테스트 대역이 아니라 infrastructure adapter로 분류되어 있다.
- [ ] Port 시그니처에 외부 DTO나 persistence Entity가 노출되지 않는다.
- [ ] Port 참조는 가능하면 Service에 모여 있다.
