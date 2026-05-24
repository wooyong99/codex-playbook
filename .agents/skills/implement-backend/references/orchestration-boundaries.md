# Backend Orchestration Boundaries

이 문서는 `implement-backend`의 [SKILL.md](../SKILL.md)에 있는 역할 요약을 보조하여, 메인 에이전트와 backend 역할 서브에이전트의 세부 경계와 예외를 정의한다.

실행 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유하고, 파일 저장·검증 규격은 [run-artifact-protocol.md](run-artifact-protocol.md)가 소유한다. 역할별 input/output/checkpoint 템플릿은 각 역할 계약 문서가 소유한다.

## 핵심 경계

`implement-backend`는 메인 에이전트가 전체 흐름을 조율하고, backend 역할 서브에이전트가 독립적인 전문 역할을 수행하는 구조다.

- 서브에이전트는 서로 호출하지 않는다.
- 서브에이전트는 전달받은 input artifact와 계약 문서 기준으로만 작업한다.
- 메인 에이전트는 이전 output을 읽고 다음 역할의 input으로 재구성한다.
- Backend Architecture Reviewer의 통과는 backend 아키텍처 기준 준수 통과를 뜻하며, 기능 정확성 전체를 보증하지 않는다.

## 서브에이전트 정의

서브에이전트 정의 파일은 역할, 판단 철학, 기본 금지사항을 제공한다.

- [backend-technical-design-writer.toml](../../../../.codex/agents/backend-technical-design-writer.toml)
- [backend-implementation-engineer.toml](../../../../.codex/agents/backend-implementation-engineer.toml)
- [backend-architecture-reviewer.toml](../../../../.codex/agents/backend-architecture-reviewer.toml)

## 메인 에이전트 책임

메인 에이전트는 backend 마일스톤의 오케스트레이터다.

- 구현 전에 [requirement-clarification-gate.md](requirement-clarification-gate.md)에 따라 요구사항 명확화 게이트를 수행한다.
- 구현 방식에 영향을 주는 유저 플로우, 정합성, 실패 처리, 운영 정책이 누락되면 사용자에게 질문한다.
- 업무 목표, 범위, 업무 규칙, 정책, 상태 변화, 운영 요구사항, 사용자 확인이 필요 없는 코드베이스 관례, 금지된 추론, 남은 미결정 사항을 분리한다.
- 실패 추적, 재처리, 감사 로그, 이벤트 유실 허용 여부, 중복 실행 방지 같은 운영 가능성을 architecture 요구사항으로 다룬다.
- backend 범위와 명시적 제외사항을 고정한다.
- 마일스톤별 Source of Truth 후보를 실제 요구사항에 맞게 선별한다.
- 각 호출 전에 input artifact를 작성한다.
- 서브에이전트 응답 신호와 output/checkpoint 파일을 검증한다.
- 이전 output artifact를 읽고 다음 역할의 input artifact로 재구성한다.
- reviewer 위반, 검증 실패, 체크포인트, 반복 한계 상황을 라우팅한다.
- 최종 결과를 사용자에게 보고한다.

메인 에이전트는 일반 경로에서 backend 구현 파일을 직접 수정하지 않는다. 자동 루프가 수렴하지 않거나 사용자가 명시적으로 요청한 경우에만 직접 개입을 선택지로 제시한다.

## 서브에이전트 책임

서브에이전트는 독립적인 역할 수행자다.

- 전달받은 input artifact와 계약 문서만 기준으로 작업한다.
- 확정 요구사항 컨텍스트에 없는 비즈니스, 운영, 실패 처리, 정합성, 재처리, 동시성 정책을 임의로 확정하지 않는다.
- 자기 역할의 output artifact를 계약 형식으로 저장한다.
- 정상 완료 경로에서도 checkpoint snapshot을 저장한다.
- 정상 완료 경로에서도 각 역할은 호출별 `[체크포인트 파일]`을 반드시 남긴다.
- 체크포인트가 필요하면 `CONTEXT_CHECKPOINT:` 신호와 checkpoint 파일을 남긴다.
- 다음 역할의 input을 직접 만들거나 다른 서브에이전트를 호출하지 않는다.

## 경계 원칙

- frontend 변경은 `implement-backend`에서 직접 구현하지 않는다.
- backend와 frontend가 함께 필요한 경우 backend API 계약, 도메인 상태, 저장, 외부 연동을 먼저 안정화한다.
- 계약 문서의 예시 문구를 프로젝트 사실처럼 복사하지 않는다.
- Source of Truth에 없는 기준, 개인 선호, 숨은 팀 관행은 reviewer 위반 근거가 될 수 없다.

## 이 문서가 소유하지 않는 것

- 마일스톤 분할 수치와 계획 기준: [milestone-planning.md](milestone-planning.md)
- backend 역할 호출 순서와 반복 종료 기준: [milestone-execution-workflow.md](milestone-execution-workflow.md)
- `.agents/runs/{run_id}` 파일 구조와 검증 절차: [run-artifact-protocol.md](run-artifact-protocol.md)
- 역할별 Markdown artifact 섹션, 결과 신호, 체크포인트 판단 기준: 각 `*-contract.md`
