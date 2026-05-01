# Transaction And Consistency Policy

## 적용 범위

- application 단위의 트랜잭션 경계
- 도메인 상태 변경과 저장 순서
- 이벤트 기반 최종 일관성
- 외부 I/O와 데이터 정합성 경계

## 핵심 원칙

- 트랜잭션은 데이터 일관성이 필요한 최소 의미 단위로 설정한다.
- Command 흐름은 읽기/쓰기 트랜잭션, Query 흐름은 읽기 전용 트랜잭션을 기본으로 한다.
- 외부 API 호출, 파일 I/O, 장기 계산은 트랜잭션 밖에서 수행한다.
- 모든 변경이 즉시 반영되어야 하거나 금전적 가치와 직결되면 강한 일관성을 선택한다.
- 약간의 지연이 허용되고 도메인 간 느슨한 결합이 중요하면 이벤트 기반 최종 일관성을 선택한다.
- 커밋 후 부수 효과는 `AFTER_COMMIT` 이벤트 처리처럼 메인 트랜잭션과 분리한다.

## 금지 규칙

- 트랜잭션 안에서 외부 시스템 호출을 수행하지 않는다.
- 실패 시 함께 롤백되어야 하는 변경을 여러 독립 트랜잭션으로 흩어 놓지 않는다.
- 커밋 전 이벤트 핸들러에서 외부 부수 효과를 실행하지 않는다.
- 최종 일관성이 허용되지 않는 재고/잔액 차감 같은 흐름을 비동기 보정만으로 처리하지 않는다.

## 안티패턴

- Facade가 필요 이상으로 많은 서비스를 하나의 긴 트랜잭션에 묶는다.
- Query 흐름에 쓰기 트랜잭션을 기본 적용해 DB 부하를 키운다.
- 이벤트 핸들러 실패 시 재시도·보상 전략 없이 메인 흐름과 분리한다.
- 트랜잭션 경계를 클래스명 관성으로만 정하고 비즈니스 의미 단위와 맞추지 않는다.

## 코드 근거

- `application` UseCase/Flow - 트랜잭션 시작점과 의미 단위
- `application` EventHandler - 커밋 후 부수 효과 처리
- `storage` Adapter/Repository - 저장과 조회 경계
- `external` Adapter - 트랜잭션 밖에서 실행해야 하는 외부 I/O

## 관련 아키텍처 문서

- [architecture/application](../architecture/application/application-guidelines.md) - UseCase, Flow, EventHandler 경계
- [architecture/storage](../architecture/storage/storage-guidelines.md) - 저장소 경계
- [architecture/external](../architecture/external/external-guidelines.md) - 외부 I/O 경계
