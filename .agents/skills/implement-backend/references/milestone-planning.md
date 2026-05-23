# Backend Milestone Planning

이 문서는 `implement-backend`가 backend 요구사항을 어떤 마일스톤 단위로 나누는지 정의한다.

실행 중 design/implementation/review 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 파일 저장 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)가 소유한다.

## 계획 모델

backend 마일스톤은 하나의 검증 가능한 서버 동작을 끝까지 닫는 단위다.

마일스톤 계획은 [requirement-clarification-gate.md](requirement-clarification-gate.md)의 요구사항 명확화 게이트를 통과한 뒤에만 수행한다.

좋은 backend 마일스톤은 아래 조건을 만족한다.

- 사용자 또는 내부 시스템 관점의 backend 결과가 하나다.
- 주 도메인 책임이 하나다.
- 주요 트랜잭션 또는 정합성 경계가 하나다.
- compile/test 명령 한 묶음으로 성공 여부를 판단할 수 있다.
- design/implementation/review 루프가 과도하게 커지기 전에 끝난다.

## 계획 산출물

각 backend 마일스톤에는 아래 메타데이터를 붙인다.

- `목표`: backend 관점 결과 1개
- `범위`: 포함할 도메인, 계층, 모듈, DB/schema, 외부 연동
- `명시적 제외사항`: 사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"
- `검증 기준`: 실행할 compile/test 명령
- `frontend 전달 계약`: frontend가 소비해야 할 API 계약 또는 미해결 사항. 없으면 "없음"
- `예상 변경 파일 수`: 가능하면 3~8개

## 요구사항 분석

마일스톤을 나누기 전에 사용자 입력을 backend 관점의 한 문장 목표로 고정한다.

먼저 확인할 항목:

- 유저 플로우가 구현 구조를 결정할 만큼 명확한가
- 정합성 요구가 transaction boundary, 이벤트 처리, 저장 모델에 영향을 주는가
- 실패 처리 정책이 retry, rollback, compensation, dead letter, 수동 복구 중 무엇을 요구하는가
- 운영 정책이 실패 추적, 관리자 재처리, 감사 로그, 멱등성, 모니터링을 요구하는가

분리해서 확인할 항목:

- API, UseCase, domain, storage, external integration, DB/schema, backend policy 중 무엇이 바뀌는가
- 명시적 제외사항은 무엇인가
- 트랜잭션 경계와 정합성 요구가 있는가
- 외부 연동 실패 처리 또는 재시도 정책이 필요한가
- 운영자가 실패 건을 추적하거나 재처리해야 하는가
- 이벤트 유실 허용 여부와 중복 실행 방지 정책이 확정됐는가
- 검증 명령이 무엇인가
- frontend 표시 방식이나 UI 상태가 backend 범위로 잘못 들어와 있지 않은가

모호한 요청은 구현 전에 우선순위 질문으로 좁힌다.

- "상품 등록 기능": 상품과 옵션 저장 흐름, 임시 저장/승인/노출 상태, 실패 추적과 재처리 필요 여부를 먼저 확인한다.
- "조회 API": 관리자 목록인지 사용자 피드인지, 데이터 규모와 정렬 기준, offset/cursor/search index/cache 필요 여부를 먼저 확인한다.
- "구조 개선": 대상 계층, 성공 기준, 공개 계약/DB/도메인 동작 변경 허용 여부, 운영 리스크를 먼저 확인한다.

## 마일스톤 분할 기준

기본 권장 단위:

- 주 도메인 1개, 보조 도메인 최대 1개
- 주요 트랜잭션 경계 1개
- API, UseCase, Flow 최대 3개
- DB/schema 변경 묶음 1개
- 외부 연동 또는 batch/scheduler 책임 1개
- 예상 변경 파일 3~8개 권장
- compile/test 명령 묶음 1개

분할을 반드시 검토하는 조건:

- 독립 backend 결과가 2개 이상이다.
- Aggregate 2개 이상 또는 모듈 4개 이상을 동시에 건드린다.
- 예상 변경 파일이 12개를 넘는다.
- DB 마이그레이션이 2개 이상이거나 서로 다른 Aggregate의 스키마를 바꾼다.
- 인증/권한, 외부 연동, 비동기 이벤트/outbox, batch/scheduler 변경이 핵심 기능 변경과 섞여 있다.
- 관리자 재처리, 감사 로그, 멱등성, 실패 상태 모델, outbox/queue/CDC 같은 운영 가능성 요구가 핵심 기능 변경과 섞여 있다.
- 한 번의 backend architecture review 대상이 10개 파일을 넘는다.

분할이 어렵다면 하나의 큰 마일스톤으로 강행하지 않고 `M{n}-backend-a`, `M{n}-backend-b` 같은 하위 마일스톤으로 나눈다. 데이터 정합성 때문에 원자성이 필요한 경우에만 큰 마일스톤을 허용한다.

## 규모별 기준

- 단일 CRUD 또는 단일 UseCase 추가는 보통 1개 backend 마일스톤으로 둔다.
- API 계약과 persistence가 함께 바뀌는 기능은 설계, 구현, 검증이 한 루프에서 끝나는지 먼저 판단한다.
- 여러 도메인에 걸친 기능은 보통 2~4개 backend 마일스톤으로 나눈다.
- 신규 서브시스템, 대규모 리팩토링, batch/outbox 도입은 5개 이상 마일스톤을 허용하되 사용자에게 진행 여부를 먼저 확인한다.

## 실행 준비

- 마일스톤 계획을 사용자에게 짧게 보고한다.
- 마일스톤이 5개 이상이면 진행 여부를 확인한다.
- 진행이 확정되면 `run_id`를 생성하고 backend 마일스톤의 run artifact 경로를 준비한다.
- run artifact의 디렉토리 구조와 파일명 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.
