# Frontend Orchestration Boundaries

이 문서는 `implement-frontend`에서 메인 에이전트와 frontend 역할 서브에이전트가 무엇을 책임지고 무엇을 책임지지 않는지 정의한다.

실행 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 파일 규격은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)와 역할별 계약 문서가 소유한다.

## 핵심 모델

`implement-frontend`는 메인 에이전트가 전체 흐름을 조율하고, 서브에이전트가 독립적인 전문 역할을 수행하는 구조다.

- 메인 에이전트는 요구사항을 분해하고 Frontend Design Writer, Frontend Implementation Engineer, Frontend Architecture Reviewer를 호출한다.
- 메인 에이전트는 이전 output을 읽고 다음 역할의 input으로 재구성한다.
- 서브에이전트는 서로 호출하지 않는다.
- 서브에이전트는 전달받은 input과 계약 문서 기준으로만 작업한다.
- Frontend Architecture Reviewer의 통과는 frontend 아키텍처 기준 준수 통과를 뜻하며, 기능 정확성·접근성·성능 전체를 보증하지 않는다.

## 참여 주체

| 주체 | 핵심 책임 | 책임이 아닌 것 |
|------|-----------|----------------|
| 메인 에이전트 | 요구사항 분석, 마일스톤 분할, Source of Truth 선별, input 작성, output 검증, 다음 단계 라우팅, 사용자 보고 | 서브에이전트의 전문 판단 대체 |
| Frontend Design Writer `frontend-technical-design-writer` | frontend 설계 판단, TDD 작성 또는 스킵 근거 작성 | 구현, 리뷰, 다음 input 작성 |
| Frontend Implementation Engineer `frontend-implementation-engineer` | frontend 코드 작성·수정, build/test/browser 검증 실행, 구현 output 작성 | architecture review 판정 |
| Frontend Architecture Reviewer `frontend-architecture-reviewer` | 입력된 Source of Truth와 TDD 결정 기준으로 frontend 변경 파일 검토 | 기능 QA, 시각 QA, backend 검토 |

서브에이전트 정의 파일은 역할, 판단 철학, 기본 금지사항을 제공한다.

- [frontend-technical-design-writer.toml](../../../../.codex/agents/frontend-technical-design-writer.toml)
- [frontend-implementation-engineer.toml](../../../../.codex/agents/frontend-implementation-engineer.toml)
- [frontend-architecture-reviewer.toml](../../../../.codex/agents/frontend-architecture-reviewer.toml)

## 메인 에이전트 책임

메인 에이전트는 frontend 마일스톤의 오케스트레이터다.

- frontend 범위와 명시적 제외사항을 고정한다.
- 마일스톤별 Source of Truth 후보를 실제 요구사항에 맞게 선별한다.
- 각 호출 전에 input artifact를 작성한다.
- 서브에이전트 응답 신호와 output/checkpoint 파일을 검증한다.
- 이전 output artifact를 읽고 다음 역할의 input artifact로 재구성한다.
- reviewer 위반, 검증 실패, 체크포인트, 반복 한계 상황을 라우팅한다.
- backend API 계약이 불확실하면 구현 전에 계약 불확실성으로 보고하거나 backend 마일스톤을 선행시킨다.
- 최종 결과를 사용자에게 보고한다.

메인 에이전트는 일반 경로에서 frontend 구현 파일을 직접 수정하지 않는다. 자동 루프가 수렴하지 않거나 사용자가 명시적으로 요청한 경우에만 직접 개입을 선택지로 제시한다.

## 서브에이전트 책임

서브에이전트는 독립적인 역할 수행자다.

- 전달받은 input artifact와 계약 문서만 기준으로 작업한다.
- 자기 역할의 output artifact를 계약 형식으로 저장한다.
- 정상 완료 경로에서도 checkpoint snapshot을 저장한다.
- 정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다.
- 체크포인트가 필요하면 `CONTEXT_CHECKPOINT:` 신호와 checkpoint 파일을 남긴다.
- 다음 역할의 input을 직접 만들거나 다른 서브에이전트를 호출하지 않는다.

## 경계 원칙

- backend 변경은 `implement-frontend`에서 직접 구현하지 않는다.
- backend API 계약이 필요한 경우 계약, 불확실성, 선행 backend 마일스톤 필요 여부를 명시한다.
- frontend와 backend가 함께 필요한 경우 backend API 계약이 안정된 뒤 frontend 상태/API/cache/UI 구현을 진행한다.
- 계약 문서의 예시 문구를 프로젝트 사실처럼 복사하지 않는다.
- Source of Truth에 없는 기준, 개인 선호, 숨은 팀 관행은 reviewer 위반 근거가 될 수 없다.

## 이 문서가 소유하지 않는 것

- 마일스톤 분할 수치와 계획 기준: [milestone-planning.md](milestone-planning.md)
- frontend 역할 호출 순서와 반복 종료 기준: [milestone-execution-workflow.md](milestone-execution-workflow.md)
- `.agents/runs/{run_id}` 파일 구조와 검증 절차: [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)
- 역할별 Markdown artifact 섹션, 결과 신호, 체크포인트 판단 기준: 각 `*-contract.md`
