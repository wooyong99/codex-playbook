---
name: implement-backend
description: Use when 사용자가 $implement-backend를 명시적으로 호출하고 백엔드 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경, storage/external/app/application 계층 변경, DB/schema 변경, 또는 backend 아키텍처 기준에 영향을 주는 변경을 요청할 때.
---

# implement-backend

## 목적

백엔드 작업이 들어오면 요구사항을 먼저 확정하고, 기술설계문서(TDD) 작성 → 코드 구현 → 코드 리뷰를 각각 전용 서브에이전트에 위임해 `docs/backend` 기준을 지키며 구현한다.

이 스킬의 핵심은 직접 구현이 아니라 오케스트레이션이다. 메인 에이전트는 질문, 범위 고정, 서브에이전트 호출, 결과 검증, 반복 제어, 사용자 보고를 맡는다.

## 호출 방식

- 이 스킬은 자동 호출되지 않아야 한다. 적용 대상에 해당하는 backend 작업이어도 사용자가 `$implement-backend`를 명시적으로 호출한 경우에만 적용한다.
- `agents/openai.yaml`의 `policy.allow_implicit_invocation: false`를 유지해 Codex의 description 기반 implicit invocation을 막는다.
- 사용자가 이 스킬을 쓰지 말라고 명시하거나 단순 설명, 구조 검토, 일반 코드 리뷰만 요청한 경우에는 오케스트레이션을 수행하지 않는다.

## 적용 대상

- backend 코드, 서버 설정, DB/schema, migration 변경
- UseCase, domain, application, app, storage, external, internal adapter 변경
- backend API 계약, 운영 설정, 보안 정책, 트랜잭션 경계 변경
- `docs/backend/**` 기준을 따라야 하는 backend 리팩토링

비적용 범위:

- frontend 화면, route, component, client state/cache 구현
- backend 기준과 무관한 단순 설명, 구조 검토, 일반 코드 리뷰
- 사용자가 명시적으로 직접 구현만 요청한 작업

## 책임

- 요구사항 명확화: 구현 판단에 필요한 정책, 범위, 성공 기준이 부족하면 먼저 질문한다.
- Source of Truth 고정: `docs/backend/README.md`와 관련 `docs/backend/**` 문서를 읽고 role input에 경로와 선정 이유를 남긴다.
- 서브에이전트 호출: `backend-technical-design-writer`, `backend-implementation-engineer`, `backend-architecture-reviewer`를 순서대로 호출한다.
- 반복 제어: 구현과 리뷰를 최대 5회 반복하고, 해결되지 않으면 사용자에게 질문한다.
- 검증: 테스트, lint, build, run artifact 검증 결과를 확인한 뒤 완료를 보고한다.

메인 에이전트는 일반 경로에서 backend 코드를 직접 고치지 않는다. 서브에이전트 도구가 없거나 정책상 호출이 막히면 구현 전에 사용자에게 fallback 진행 여부를 확인한다.

## 참조 문서

핵심 작업 흐름은 이 문서가 소유하고, 긴 규격과 템플릿은 아래 reference가 소유한다.

- 요구사항 명확화 게이트: [references/requirement-clarification-gate.md](references/requirement-clarification-gate.md)
- 확정 요구사항 컨텍스트 템플릿: [references/requirement-context-template.md](references/requirement-context-template.md)
- 상세 책임 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- 마일스톤 계획: [references/milestone-planning.md](references/milestone-planning.md)
- 실행 흐름: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)
- run artifact 저장·검증·복구 규약: [references/run-artifact-protocol.md](references/run-artifact-protocol.md)
- 간소화된 run artifact 최소 형식: [references/run-artifacts.md](references/run-artifacts.md)
- 서브에이전트 호출 흐름: [references/subagent-workflow.md](references/subagent-workflow.md)
- Backend Design Writer 계약: [references/backend-technical-design-writer-contract.md](references/backend-technical-design-writer-contract.md)
- Backend Implementation Engineer 계약: [references/backend-implementation-engineer-contract.md](references/backend-implementation-engineer-contract.md)
- Backend Architecture Reviewer 계약: [references/backend-architecture-reviewer-contract.md](references/backend-architecture-reviewer-contract.md)

## 작업 흐름

1. 요구사항 명확화
   - 목표, 범위, 제외사항, 성공 기준, 외부 계약, DB/schema 영향, 보안/운영 정책을 확인한다.
   - 합리적 추론으로 정하면 위험한 정책이 있으면 구현을 시작하지 않고 질문한다.

2. Source of Truth 선정
   - 항상 `docs/backend/README.md`를 포함한다.
   - 작업 성격에 맞춰 `docs/backend/architecture/**`, `docs/backend/policies/**`, `docs/backend/api-specs/**`, `docs/backend/design/**` 중 관련 문서를 고른다.
   - 문서가 없거나 실제 코드와 맞지 않으면 먼저 사용자에게 문서 정리 필요성을 알리거나 `reverse-engineer-backend-docs` 사용을 제안한다.

3. run artifact 준비
   - `.agents/runs/{run_id}` 아래에 요구사항, role input/output, checkpoint 파일을 만든다.
   - 자세한 최소 형식은 [references/run-artifacts.md](references/run-artifacts.md)를 따른다.

4. TDD 작성 서브에이전트 호출
   - `backend-technical-design-writer`를 호출한다.
   - 입력에는 확정 요구사항, 제외사항, Source of Truth, TDD 저장 경로, 출력 파일, 체크포인트 파일을 포함한다.
   - 결과는 구현자가 따를 수 있는 backend TDD 또는 TDD 생략 불가/차단 사유여야 한다.

5. 코드 구현 서브에이전트 호출
   - `backend-implementation-engineer`를 호출한다.
   - 입력에는 TDD 결과, Source of Truth, 변경 범위, 검증 명령을 포함한다.
   - 구현자는 `docs/backend` 하위 문서와 TDD를 기준으로 코드를 수정하고 검증 결과를 남긴다.

6. 코드 리뷰 서브에이전트 호출
   - `backend-architecture-reviewer`를 호출한다.
   - 입력에는 구현 결과, 변경 파일, TDD, Source of Truth를 포함한다.
   - reviewer는 `docs/backend` 하위 문서와 TDD 기준 위반만 판정한다.

7. 최대 5회 수정 루프
   - reviewer가 `blocker` 또는 `major` 위반을 보고하면 같은 구현 서브에이전트에 수정 입력을 보낸다.
   - 수정 후 reviewer를 다시 호출한다.
   - 구현과 리뷰 반복은 최대 5회다.
   - 5회 후에도 위반이 남으면 직접 고치지 말고 위반 요약, 시도한 수정, 남은 결정 사항을 사용자에게 질문한다.

8. 완료 보고
   - 변경 파일, TDD 경로, 테스트/lint/build 결과, reviewer 판정, 남은 위험 또는 사용자 결정 사항을 짧게 보고한다.

## 서브에이전트 규칙

- 세부 호출 프롬프트와 출력 형식은 [references/subagent-workflow.md](references/subagent-workflow.md)를 따른다.
- 서브에이전트는 서로 직접 호출하지 않는다.
- 서브에이전트는 전달받은 input artifact와 `docs/backend` Source of Truth만 신뢰한다.
- reviewer는 취향, 일반론, 입력에 없는 규칙을 violation으로 만들지 않는다.
- 구현자는 reviewer의 `blocker`/`major` 위반을 해결하는 범위로만 수정한다.

## 검증

스킬 또는 관련 artifact 구조를 바꾼 뒤 실행한다.

```bash
python3 .agents/skills/write-skill-artifact/scripts/check_skill_artifact.py .agents/skills/implement-backend/SKILL.md
python3 .agents/scripts/validate-context-checkpoints.py
python3 .agents/scripts/check-playbook.py
```

백엔드 작업 자체를 완료할 때는 해당 작업의 Gradle test, ktlint, bootJar 등 실제 검증 명령을 fresh run으로 수행한다.
