# Persistence Guidelines

이 문서는 `backend/internal/persistence` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `backend/internal/persistence` - application Port 구현, JPA Entity 매핑, QueryDsl 구성, 저장소 adapter를 담당한다.

## 책임

- application 계층이 선언한 저장소 Port를 구현한다.
- 인프라 모델과 도메인 모델을 분리하고 반환 전 도메인 객체로 변환한다.
- 단순 CRUD와 복잡 쿼리를 역할별 컴포넌트로 나눈다.
- Entity 변경과 DDL 변경을 같은 변경 단위로 관리한다.
- DB adapter가 아직 없더라도 runtime 저장소 구현이 필요하면 이 모듈이 임시 in-memory adapter를 소유한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, database
- used by: Spring runtime, `core/application` Port
- 금지되는 방향: Entity 외부 노출, Domain 내부 변환 로직, 단순 저장소와 복잡 쿼리 혼재

## 핵심 원칙

- persistence 단위는 저장 기술을 캡슐화하고 application에는 Port 계약만 드러낸다.
- 저장소 구현체의 기술이 JPA, JDBC, in-memory, fake runtime 구현 중 무엇이든 application 밖에서 Port를 구현한다.
- DB 스키마 변경이 domain 모델로 전파되지 않도록 Entity와 Domain을 분리한다.
- 조회 복잡도는 JpaRepository와 QueryDslRepository를 분리해 관리한다.
- DDL은 Entity 변경과 함께 갱신해 스키마 불일치를 막는다.

## 관련 정책

- [transaction-and-consistency](../../../policies/transaction-and-consistency.md) - 트랜잭션 경계와 정합성
- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - 쿼리 성능, 락, 캐시

## 금지 규칙

- Entity, Row, Record 같은 인프라 모델을 application이나 domain 계층으로 반환하지 않는다.
- 인프라 모델에 비즈니스 로직을 넣지 않는다.
- 저장소 Port 구현체를 `core/application` production source에 두지 않는다.
- 런타임에서 사용하는 in-memory 저장소를 application 테스트 대역처럼 취급해 application 내부에 배치하지 않는다.
- Domain 클래스나 Entity 클래스 내부에 양방향 변환 로직을 넣지 않는다.
- 단순 Repository에 복잡한 동적 쿼리와 Projection 조합을 계속 누적하지 않는다.
- DDL 변경 없이 Entity만 수정하지 않는다.
- QueryDsl/JPA 세부 구현을 application Port 시그니처로 노출하지 않는다.

## 주요 컴포넌트

- Port 구현체: `{Entity}Adapter`
- 단순 저장소: `{Entity}JpaRepository`
- 복잡 쿼리 저장소: `{Entity}QueryDslRepository`
- 변환 컴포넌트: `{Entity}Extension`
- 인프라 모델: `{Entity}Entity`
- DDL 파일: `sql/{domain}/{table}.sql`

## 전략 문서

- [Strategies](./strategies/README.md)

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] application은 저장 기술이 아니라 Port 인터페이스에 의존한다.
- [ ] 저장소 Port의 runtime 구현체가 `backend/internal/persistence` 아래에 배치되어 있다.
- [ ] 아직 JPA/DDL이 없는 임시 저장소라도 production에서 사용되면 persistence adapter로 분류되어 있다.
- [ ] persistence 반환 타입에 JPA Entity나 QueryDsl 타입이 노출되지 않는다.
- [ ] Entity 변경과 DDL 변경이 같은 PR, 커밋, 또는 설계 문서에 함께 포함되어 있다.
