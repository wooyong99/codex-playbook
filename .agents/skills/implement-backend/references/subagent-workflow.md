# Backend Subagent Workflow

## 목적

`implement-backend`가 호출하는 세 backend 서브에이전트의 입력, 출력, 반복 규칙을 한 곳에 둔다.

## 공통 입력

모든 서브에이전트 입력에는 아래를 포함한다.

- 확정 요구사항과 명시적 제외사항
- Source of Truth: `docs/backend/README.md`와 관련 `docs/backend/**` 문서, 각 선정 이유
- 현재 단계의 입력 파일, 출력 파일, 체크포인트 파일
- 이번 단계에서 반드시 지킬 출력 형식

서브에이전트는 사용자와 직접 대화하지 않는다. 질문이 필요하면 출력에 `needs_user_answer` 상태와 질문을 남기고 멈춘다.

## TDD Writer

호출 대상: `backend-technical-design-writer`

해야 할 일:

- 요구사항과 `docs/backend` 기준을 바탕으로 backend 기술설계문서(TDD)를 작성하거나 갱신한다.
- 책임 경계, 데이터 흐름, 트랜잭션/정합성, 실패 처리, 검증 계획을 구현 가능한 결정으로 남긴다.
- 구현하지 않는다.

출력:

```text
status: tdd_created | tdd_updated | blocked
tdd_path: <docs/backend/design/... 또는 output artifact 경로>
summary: <핵심 설계 결정>
questions: <사용자 질문, 없으면 없음>
```

## Implementation Engineer

호출 대상: `backend-implementation-engineer`

해야 할 일:

- TDD와 `docs/backend` 기준을 따라 backend 코드를 수정한다.
- 관련 테스트, lint, build 명령을 실행하고 결과를 남긴다.
- reviewer 판정은 하지 않는다.

수정 루프 입력에는 reviewer의 위반 목록만 추가한다. 구현자는 위반 해결 범위 밖으로 작업을 넓히지 않는다.

출력:

```text
status: implemented | needs_user_answer | failed
changed_files:
verification:
notes:
questions:
```

## Architecture Reviewer

호출 대상: `backend-architecture-reviewer`

해야 할 일:

- 변경이 TDD와 `docs/backend` 기준을 위반했는지 독립적으로 판정한다.
- 검토 기준은 입력의 Source of Truth와 TDD로 한정한다.
- 코드를 수정하지 않는다.

판정:

- `pass`: `blocker` 또는 `major` 위반 없음
- `fail`: `blocker` 또는 `major` 위반 있음

Backend Rule ID 형식:

- `BACKEND-APP-DTO-001`
- `BACKEND-DOMAIN-BOUNDARY-001`
- `BACKEND-PERSISTENCE-TRANSACTION-001`

위반 항목은 아래 필드를 포함한다.

- `rule_id`
- `severity`: `blocker`, `major`, `minor`, `info`
- `file`
- `line_range`
- `rule`
- `source_path`
- `reason`
- `suggested_fix`
- `UNREGISTERED`: Source of Truth에 명시 규칙이 없는데 의심만 있는 경우 사용

## 반복 규칙

1. reviewer가 `pass`를 반환하면 루프를 끝낸다.
2. reviewer가 `fail`을 반환하면 구현 서브에이전트에 위반 목록을 넘겨 수정시킨다.
3. 구현 → 리뷰를 최대 5회 반복한다.
4. 5회 후에도 `blocker` 또는 `major`가 남으면 메인 에이전트가 사용자에게 질문한다.
5. 메인 에이전트는 사용자의 명시 승인 없이 직접 backend 코드를 수정해 루프를 우회하지 않는다.
