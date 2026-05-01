# Storage Guidelines

이 문서는 `storage` 단위의 실제 코드 위치, 책임, 의존 경계, 구현 전략을 정리한다.

## 코드 위치

- `storage` infrastructure module/package - application Port 구현, Entity 매핑, 쿼리 구현, DDL 관리를 담당한다.

## 책임

- application 계층이 선언한 저장소 Port를 구현한다.
- 인프라 모델과 도메인 모델을 분리하고 반환 전 도메인 객체로 변환한다.
- 단순 CRUD와 복잡 쿼리를 역할별 컴포넌트로 나눈다.
- 인프라 모델 변경 시 DDL 변경을 함께 관리한다.

## 의존 경계

- depends on: `application`, `domain`, database
- used by: `application`
- 금지되는 방향: Entity 외부 노출, Domain 내부 변환 로직, 단순 저장소와 복잡 쿼리 혼재

## 핵심 원칙

- storage 단위는 저장 기술을 캡슐화하고 application에는 Port 계약만 드러낸다.
- DB 스키마 변경이 domain 모델로 전파되지 않도록 인프라 모델과 도메인 모델을 분리한다.
- 조회 복잡도는 단순 저장소와 복잡 쿼리 저장소를 분리해 관리한다.

## 관련 정책

- [transaction-and-consistency](../../policies/transaction-and-consistency.md) - 트랜잭션 경계와 정합성
- [concurrency-and-performance](../../policies/concurrency-and-performance.md) - 쿼리 성능, 락, 캐시

## 금지 규칙

- Entity, Row, Record 같은 인프라 모델을 application이나 domain 계층으로 반환하지 않는다.
- 인프라 모델에 비즈니스 로직을 넣지 않는다.
- Domain 클래스나 Entity 클래스 내부에 양방향 변환 로직을 넣지 않는다.
- 단순 Repository에 복잡한 동적 쿼리와 Projection 조합을 계속 누적하지 않는다.

## 안티패턴

- DDL 변경 없이 Entity만 수정한다.
- QueryDsl/JPA 세부 구현이 application Port 시그니처로 드러난다.
- 변환 책임이 Adapter, Entity, Domain에 흩어져 변경 지점이 늘어난다.

## 주요 컴포넌트

- Port 구현체: `{Entity}Adapter`
- 단순 저장소: `{Entity}JpaRepository`
- 복잡 쿼리 저장소: `{Entity}QueryDslRepository`
- 변환 컴포넌트: `{Entity}Extension`
- 인프라 모델: `{Entity}Entity`

## 전략 문서

- [Strategies](./strategies/README.md)

## Playbook compatibility

- 이 단위는 기존 playbook의 `storage` 개념 계층과 동일하다.
- 실제 프로젝트에서 storage가 `persistence`, `repository`, `database` 등으로 나뉘면 실제 모듈명을 우선한다.
