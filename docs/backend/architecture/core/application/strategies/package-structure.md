# Package Structure 컨벤션

이 문서는 `application` 단위의 패키지 구조와 컴포넌트 배치 기준을 정리한다.

## 목적

- application 내부 코드를 도메인 개념과 역할 기준으로 일관되게 배치한다.
- UseCase 계약, 구현체, application DTO, Port, Mapper 같은 application 역할을 찾기 쉽게 만든다.
- `common`, `shared`, `util` 같은 모호한 패키지로 비즈니스 흐름이 숨지 않게 한다.

## 적용 범위

- `application` module/package 내부의 하위 패키지 구조
- 도메인별 UseCase, Facade, Coordinator, Service, Validator, Strategy, Port, Mapper 배치
- 신규 도메인 또는 신규 application 컴포넌트를 추가할 때의 위치 판단

`app/api`, `core/domain`, `internal/persistence`, `external/integration` 단위의 파일 구조는 각 단위의 전략 문서가 소유한다.

## 책임

- application 내부 패키지 분할의 우선순위를 정의한다.
- 도메인 패키지와 역할 하위 패키지를 언제 나눌지 정한다.
- application 전역 관심사와 도메인 전용 코드를 분리한다.

## 전체 구조

```text
application/
  ├── common/                     optional, application 전역 관심사만
  └── {domain}/
      ├── {Entity}CommandUseCase.kt
      ├── {Entity}QueryUseCase.kt
      ├── {Entity}CommandFacade.kt     optional
      ├── {Entity}QueryFacade.kt       optional
      ├── {Entity}CommandCoordinator.kt optional
      ├── {Entity}CommandService.kt    optional
      ├── dto/
      │   ├── {Action}{Entity}.kt
      │   └── internal/                optional, 예외 승인된 내부 개념 DTO만
      ├── validator/              optional
      ├── strategy/               optional
      ├── port/                   optional
      └── mapper/                 optional
```

UseCase 계약과 주요 구현체는 도메인 패키지 루트에 둔다. UseCase는 Command/Query 단위로 묶고, 세부 action은 메서드와 `dto/{Action}{Entity}.kt`로 표현한다.
Command/Result 같은 application 내부 DTO는 수가 빠르게 늘어나므로 `dto/` 하위 패키지에 둔다.
하위 컴포넌트 간 DTO는 기본적으로 만들지 않으며, 예외 기준은 [component-dto-convention](component-dto-convention.md)을 따른다.

## 세부 규칙

### 분할 우선순위

1. application 단위 안에서는 도메인 개념으로 먼저 나눈다.
2. 도메인 내부에서는 UseCase 계약과 주요 구현체를 먼저 드러낸다.
3. 같은 역할의 파일이 여러 개로 늘어나면 역할 하위 패키지를 둔다.
4. 도메인과 무관한 application 전역 관심사만 `common/`에 둔다.

### 도메인 패키지

- `{domain}`은 소문자 단수형을 기본값으로 한다.
- 한 도메인의 Command/Query UseCase 계약, application DTO, 구현체, Mapper는 같은 도메인 패키지 아래에서 찾을 수 있어야 한다.
- 다른 도메인 Port나 모델을 직접 참조해야 한다면 Port 경계를 먼저 검토한다.

### dto 패키지

- `dto/`는 application 내부 DTO만 담는다.
- `{Action}{Entity}.kt` 파일은 `dto/` 아래에 두고, 해당 operation의 `Command`와 `Result`를 함께 정의한다.
- `dto/internal/`은 여러 application 컴포넌트가 공유해야 하는 예외 승인 내부 개념 DTO만 담는다.
- `app/api`의 HTTP Request/Response DTO를 application `dto/`에 두지 않는다.

### 역할 하위 패키지

- `validator/`, `strategy/`, `port/`, `mapper/`는 해당 역할 파일이 늘어날 때만 만든다.
- UseCase 인터페이스는 외부 호출 계약이므로 `{Entity}CommandUseCase`, `{Entity}QueryUseCase`로 도메인 패키지 루트에 둔다.
- Facade와 Coordinator는 구현하는 UseCase의 Command/Query 축을 이름에 맞춘다.
- Service는 Command의 원자적 처리 단위이므로 기본적으로 `{Entity}CommandService`로 둔다.
- 구현체가 많아지면 역할별 하위 패키지를 검토한다.

### common 패키지

- `common/`은 application 단위 내부에서 모든 도메인이 공유하는 전역 관심사만 담는다.
- 특정 도메인에서 시작한 로직은 재사용 가능성이 생겼다는 이유만으로 곧바로 `common/`으로 올리지 않는다.
- 공통화가 필요하면 먼저 Port, Strategy, Validator 같은 역할 경계로 표현할 수 있는지 검토한다.

## 금지 규칙

- 도메인 패키지 없이 최상위에 `service/`, `port/`, `mapper/` 같은 역할 패키지만 나열하지 않는다.
- 단일 파일만 있는 역할을 위해 하위 패키지를 과도하게 만들지 않는다.
- `common`, `shared`, `util`, `helper` 이름으로 비즈니스 흐름을 숨기지 않는다.
- operation별 Command/Result 파일을 도메인 패키지 루트에 계속 쌓아두지 않는다.
- `ServiceCommand`, `ValidatorDto`, `StrategyDto` 같은 컴포넌트 전용 DTO 파일을 만들지 않는다.
- action마다 `{Action}{Entity}UseCase`, `{Action}{Entity}Facade`, `{Action}{Entity}Coordinator` 파일을 기본값으로 만들지 않는다.
- application `dto/`에 HTTP Request/Response DTO나 외부 API DTO를 섞지 않는다.
- 예외 승인 없는 내부 DTO를 `dto/internal/`, `common`, `shared`, `util`에 두지 않는다.
- 다른 도메인의 내부 구현체를 직접 참조하기 위해 패키지 경계를 우회하지 않는다.
- `app/api`, `internal/persistence`, `external/integration` 구현체나 DTO를 application 패키지 안으로 끌어오지 않는다.

## 예외와 경계

- 실제 프로젝트의 모듈명이 `core-application`, `usecase`처럼 다르면 실제 모듈명을 우선한다.
- 도메인보다 provider 또는 기술 단위 분리가 중요한 구현체는 application이 아니라 infrastructure 단위에 둔다.
- 파일 수가 적은 초기 단계에서는 도메인 패키지 루트 flat 구조를 우선한다.
- 특정 action이 별도 권한, 별도 actor, 독립적인 외부 계약을 가지면 action 단위 UseCase 또는 구현체 분리를 검토할 수 있다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 신규 application 파일이 도메인과 역할 기준에 맞는 패키지에 배치되어 있다.
- [ ] 외부 호출 계약인 Command/Query UseCase는 도메인 패키지 루트에 있고, application DTO는 `dto/` 아래에 있다.
- [ ] 하위 컴포넌트 간 DTO는 기본 금지이며, 예외 DTO만 `dto/internal/`에 제한적으로 존재한다.
- [ ] 역할 하위 패키지가 파일 수와 책임 분리를 기준으로 만들어져 있다.
- [ ] `common/`에 있는 코드는 특정 도메인 업무 흐름이 아니라 application 전역 관심사만 포함한다.
