# Backend Milestone Planning

이 문서는 `implement-backend` 스킬의 backend 요구사항 분석과 마일스톤 분할 기준을 소유한다. 실행 중 D/A/B 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유한다.

## 요구사항 분석

- 사용자 입력을 backend 관점의 한 문장 목표로 고정한다.
- API, UseCase, domain, storage, external integration, DB/schema, backend policy 중 무엇이 바뀌는지 분리한다.
- 명시적 제외사항을 요구사항과 분리해 기록한다.
- 트랜잭션 경계, 정합성 요구, 외부 연동 실패 처리, 검증 명령이 불명확하면 구현 전에 확인한다.
- frontend 표시 방식이나 UI 상태는 backend 마일스톤 범위로 끌어오지 않는다.

## 마일스톤 분할 기준

backend 마일스톤은 하나의 도메인 책임과 하나의 검증 가능한 서버 동작을 기준으로 나눈다. 목표는 한 D/A/B 루프가 과도하게 커지기 전에 끝나는 단위로 작업을 제한하는 것이다.

마일스톤 기본 단위:

- 사용자 또는 내부 시스템 관점의 backend 결과 1개
- 주 도메인 1개, 보조 도메인 최대 1개
- 주요 트랜잭션 경계 1개
- API, UseCase, Flow 최대 3개
- DB/schema 변경 묶음 1개
- 외부 연동 또는 batch/scheduler 책임 1개
- 예상 변경 파일 3~8개 권장
- compile/test 명령 묶음 1개로 성공과 실패 판단 가능

무조건 분할을 검토하는 조건:

- 독립 backend 결과가 2개 이상이다.
- Aggregate 2개 이상 또는 모듈 4개 이상을 동시에 건드린다.
- 예상 변경 파일이 12개를 넘는다.
- DB 마이그레이션이 2개 이상이거나 서로 다른 Aggregate의 스키마를 바꾼다.
- 인증/권한, 외부 연동, 비동기 이벤트/outbox, batch/scheduler 변경이 핵심 기능 변경과 섞여 있다.
- 한 번의 backend B 검토 대상이 10개 파일을 넘는다.

분할이 어렵다면 하나의 큰 마일스톤으로 강행하지 않고 `M{n}-backend-a`, `M{n}-backend-b` 같은 하위 마일스톤으로 나눈다. 데이터 정합성 때문에 원자성이 필요한 경우에만 큰 마일스톤을 허용한다.

## 규모별 기준

- 단일 CRUD 또는 단일 UseCase 추가는 보통 1개 backend 마일스톤으로 둔다.
- API 계약과 persistence가 함께 바뀌는 기능은 보통 설계, 구현, 검증이 한 루프에서 끝나는지 먼저 판단한다.
- 여러 도메인에 걸친 기능은 보통 2~4개 backend 마일스톤으로 나눈다.
- 신규 서브시스템, 대규모 리팩토링, batch/outbox 도입은 5개 이상 마일스톤을 허용하되 사용자에게 진행 여부를 먼저 확인한다.

## 마일스톤 메타데이터

각 backend 마일스톤에는 아래 항목을 붙인다.

- `목표`: backend 관점 결과 1개
- `범위`: 포함할 도메인, 계층, 모듈, DB/schema, 외부 연동
- `명시적 제외사항`: 사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"
- `예상 변경 파일 수`: 3~8개 권장
- `검증 기준`: 실행할 compile/test 명령
- `frontend handoff`: frontend가 소비해야 할 API 계약 또는 미해결 사항. 없으면 "없음"

## 실행 준비

- 마일스톤 계획을 사용자에게 짧게 보고한다.
- 마일스톤이 5개 이상이면 진행 여부를 확인한다.
- 진행이 확정되면 `run_id`를 생성하고 `.agents/runs/{run_id}/handoffs`, `.agents/runs/{run_id}/checkpoints` 하위 경로를 준비한다.
- run id와 경로 구성 규칙은 [handoff-checkpoint-protocol.md](handoff-checkpoint-protocol.md)를 따른다.
