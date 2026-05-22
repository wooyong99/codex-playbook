# Application Guidelines

이 문서는 `backend/core/application` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `backend/core/application` - 유스케이스 실행, 업무 흐름 조율, 트랜잭션 경계, Port 계약 정의를 담당한다.

## 책임

- 외부 요청을 받아 Domain 객체와 Port를 조합해 유스케이스를 완성한다.
- Domain 로직이 인프라 구현 세부사항에 오염되지 않도록 경계를 유지한다.
- 데이터 일관성 단위를 결정하고 트랜잭션 범위를 의미 단위로 제한한다.
- UseCase, Facade, Coordinator, Service, Validator, Strategy, Port, Mapper 같은 역할을 프로젝트 복잡도에 맞게 배치한다.

## 의존 경계

- depends on: `core/domain`, outbound Port interface
- used by: `app/api`, `app/batch`, `app/worker`, infrastructure adapter
- 금지되는 방향: 인프라 구현체 직접 참조, application 진입점 간 직접 호출, 트랜잭션 내 외부 I/O

## 핵심 원칙

- 비즈니스 규칙은 Domain에 위임하고 application은 조합과 경계 설정에 집중한다.
- 인프라 구현체가 아니라 application이 정의한 추상화 인터페이스를 통해 외부 자원에 접근한다.
- 입력 형식 검증, 데이터 조회, 비즈니스 규칙 검증, 도메인 행위 실행, 저장 및 결과 반환의 책임 단계를 섞지 않는다.

## 관련 정책

- [transaction-and-consistency](../../../policies/transaction-and-consistency.md) - 트랜잭션 경계와 정합성
- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - 동시성 제어와 성능
- [logging](../../../policies/logging.md) - 상태 변경과 실패 로깅

## 금지 규칙

- Application 계층에 도메인 불변식이나 상태 판단을 직접 구현하지 않는다.
- 추상화 인터페이스 없이 DB, 외부 API, 메시징 구현체를 직접 참조하지 않는다.
- 트랜잭션 안에서 외부 API 호출, 파일 I/O, 장기 계산을 수행하지 않는다.
- Validator가 데이터를 직접 조회하거나 형식 검증과 존재 여부 검증을 섞지 않는다.
- UseCase가 다른 UseCase를 직접 호출해 진입점끼리 결합하지 않는다.
- Facade, Coordinator, Service, Validator, Strategy 역할을 이름만 분리하고 같은 책임을 중복 구현하지 않는다.
- 트랜잭션 경계를 불필요하게 넓혀 DB 커넥션 점유 시간을 늘리지 않는다.

## 주요 컴포넌트

- External contract: UseCase
- Complexity Hiding: Facade
- Transaction Coordinator: Coordinator
- Aggregate Command Processor: Service
- Rule Checker: Validator
- Strategy: Strategy
- Assembler: Mapper
- Outbound contract: Port interface

## 전략 문서

- [Strategies](./strategies/README.md)

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] application 진입점은 도메인 행위와 Port 계약을 조합하되 인프라 구현체를 직접 참조하지 않는다.
- [ ] 트랜잭션 경계, 외부 I/O 경계, 데이터 일관성 단위가 설계 문서, 테스트, 또는 코드 구조에서 확인된다.
- [ ] UseCase, Facade, Coordinator, Service, Validator, Strategy, Port, Mapper 역할 중 필요한 것만 선택되어 책임이 중복되지 않는다.
