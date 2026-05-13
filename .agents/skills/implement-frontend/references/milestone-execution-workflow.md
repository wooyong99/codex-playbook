# Frontend Milestone Execution Workflow

이 문서는 `implement-frontend` 스킬의 frontend 마일스톤 실행 흐름을 정의한다.

책임 경계는 [orchestration-boundaries.md](orchestration-boundaries.md)가 소유하고, 역할별 input/output schema는 각 frontend 계약 문서가 소유한다. 파일 검증과 체크포인트 복구 절차는 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.

## 실행 모델

각 frontend 마일스톤은 D/A/B 역할을 파일 기반으로 연결한다.

```text
Main agent
  -> D input
  -> D output
  -> A input
  -> A output
  -> B input
  -> B output
  -> pass or A fix input
```

메인 에이전트는 각 단계 사이에서 이전 output을 검증하고 다음 input을 만든다. 이 변환은 단순 포맷 변환이 아니라 현재 마일스톤 상태, Source of Truth, 제외사항, 검증 결과, reviewer 위반, backend API 계약 불확실성을 반영하는 오케스트레이션 책임이다.

## 단계 개요

1. 마일스톤 시작: 범위, 제외사항, 검증 기준, run artifact 경로를 확정한다.
2. Agent D 위임: frontend TDD를 작성하거나 스킵 근거를 받는다.
3. Agent A 위임: frontend 구현 또는 수정을 수행한다.
4. Agent B 위임: frontend 아키텍처 기준 준수 여부를 검토한다.
5. 위반 수정: 같은 A 인스턴스에 수정 작업을 맡긴다.
6. 반복 종료: 모든 필수 reviewer가 통과하면 완료하고, 반복 한계를 넘으면 escalation한다.

## 공통 운영 규칙

- D와 B는 매번 새 인스턴스로 호출한다.
- A는 마일스톤 첫 구현에서 새 인스턴스로 시작하고, 같은 마일스톤의 위반 수정과 체크포인트 재개에서는 동일 인스턴스를 이어서 사용한다.
- 마일스톤이 바뀌면 A도 새 인스턴스로 시작한다.
- D/A/B 호출마다 해당 계약 문서의 `Input > 역할별 체크포인트 기준`을 `[체크포인트 판단 기준]`으로 input artifact의 `checkpoint.criteria`에 전달한다.
- D/A/B 호출 전에 `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 모두 할당한다.
- Source of Truth 후보 중 이번 변경과 직접 관련된 문서만 input artifact에 넣는다.
- 정상 산출물과 체크포인트 파일은 모두 검증한 뒤 다음 단계로 진행한다.

## Step 1. 마일스톤 시작

고수준 확인:

- 현재 frontend 마일스톤을 진행 중으로 표시한다.
- 목표, 범위, 명시적 제외사항, build/test 또는 브라우저 검증 기준을 다시 확인한다.
- 이번 마일스톤의 input, output, checkpoint 경로를 할당한다.
- frontend Source of Truth 후보에서 이번 변경과 직접 관련된 문서만 선별한다.
- backend API 계약이 불확실하면 A 구현 전에 계약 불확실성으로 보고하거나 backend 마일스톤 선행을 요청한다.

세부 파일 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.

## Step 2. Agent D 위임

목적:

- frontend 설계가 필요한 경우 TDD를 작성한다.
- TDD가 불필요하면 스킵 근거를 output artifact로 남긴다.

처리:

- 호출 전 [frontend-technical-design-writer-contract.md](frontend-technical-design-writer-contract.md)의 Input 형식으로 D input artifact를 저장한다.
- 호출 프롬프트에는 `[입력 파일]` 경로와 계약 파일 경로만 전달한다.
- `TDD_CREATED:`이면 D output을 검증하고 `payload.tdd_path`와 D output 경로를 보관한다.
- `TDD_SKIPPED:`이면 D output을 검증하고 `payload.skip_reason`과 D output 경로를 보관한다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 재호출한다.

`TDD_SKIPPED` 재확인 조건:

- 마일스톤이 route/page, feature/entity, state/API/cache 중 2개 이상 책임 영역에 걸친다.
- 새로운 상태 소유권, query key/cache 전략, error boundary, routing 구조가 포함된다.
- responsive layout, 접근성, 렌더링 성능, 브라우저 검증 리스크가 포함된다.
- 사용자가 복잡한 변경, 대규모 리팩토링, 엔터프라이즈급 같은 표현으로 설계 리스크를 명시했다.

## Step 3. Agent A 위임

목적:

- D 결과와 Source of Truth를 기준으로 frontend 코드를 구현한다.
- build/test/browser 검증 결과를 output artifact에 남긴다.

처리:

- 호출 전 [frontend-implementation-engineer-contract.md](frontend-implementation-engineer-contract.md)의 Input Case A 형식으로 A input artifact를 저장한다.
- A input artifact에는 D output 경로를 기록하고, 설계 요약 원문은 복사하지 않는다.
- `IMPLEMENTATION_COMPLETED:`이면 A output을 검증한다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 같은 A 인스턴스를 재호출한다.
- `verification.compile.exit_code`, `verification.tests.exit_code`가 누락됐거나 실패면 마일스톤을 성공으로 간주하지 않는다.
- 브라우저 검증이 필요한데 실행되지 않았으면 이유를 사용자에게 노출하고, B 검토 전에 허용 가능한지 판단한다.
- 검증 실패는 A 재호출 또는 사용자 보고로 처리하고 B 검토로 넘기지 않는다.

## Step 4. Agent B 및 Supplemental Reviewer 위임

목적:

- A가 변경한 frontend 파일이 입력된 Source of Truth와 TDD 결정에 맞는지 검토한다.
- 문서 구조 또는 보안 민감 변경은 supplemental reviewer로 보강한다.

처리:

- frontend 변경 파일이 있으면 [frontend-architecture-reviewer-contract.md](frontend-architecture-reviewer-contract.md)의 Input 형식으로 B input artifact를 저장한다.
- B input artifact에는 A output 경로, D output 경로, 이번 검토의 Source of Truth, output/checkpoint 경로, 체크포인트 기준을 기록한다.
- 기준 문서와 TDD 결정은 B input artifact로 전달하며 agent TOML이 정적으로 소유하지 않는다.
- `REVIEW_COMPLETED:`이면 B output을 검증하고 `status`와 `payload.violations`를 읽는다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 새 B 인스턴스를 재호출한다.
- 호출된 모든 reviewer의 `status: pass`가 확인되면 마일스톤을 완료한다.
- `status: violations`이면 위반 수정 단계로 진행한다.

Supplemental reviewer 적용:

- 변경 파일이 문서 또는 보안 민감 영역을 포함하면 [review routing](../../../../docs/review/README.md)에 따라 supplemental reviewer를 추가한다.
- supplemental reviewer 결과도 Rule ID, severity, source_path를 포함해야 한다.
- `blocker` 또는 `major` 위반은 B 위반과 동일하게 수정 루프로 보낸다.

## Step 5. 위반 수정

목적:

- reviewer가 확정한 위반만 수정한다.
- 위반과 무관한 코드는 변경하지 않는다.

처리:

- 같은 마일스톤의 frontend A 인스턴스를 이어서 사용한다.
- [frontend-implementation-engineer-contract.md](frontend-implementation-engineer-contract.md)의 Input Case B 형식으로 A fix input artifact를 저장한다.
- A fix input artifact에는 reviewer output 파일 경로만 기록하고 위반 본문을 복사하지 않는다.
- `FIX_APPLIED:`이면 A fix output을 검증한다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 같은 A 인스턴스를 재호출한다.
- 새로 수정된 파일이 있으면 마일스톤 변경 파일 집합에 합친다.
- build 또는 tests 검증이 누락·실패하면 재검토로 진행하지 않는다.
- 수정 후에는 해당 reviewer를 새 인스턴스로 다시 호출한다.

## Step 6. 반복 종료

- 호출된 모든 reviewer가 `status: pass`를 반환하면 frontend 마일스톤을 완료한다.
- B 또는 supplemental reviewer가 `status: violations`를 반환하면 위반 수정 단계로 돌아간다.
- A-B 반복은 최대 5회까지만 자동 수행한다.
- 5회를 넘으면 escalation 단계로 넘어간다.

## Escalation

자동 수렴에 실패하면 마지막 검토 결과를 3~5줄로 요약하고 사용자 선택을 기다린다.

선택지:

- 현재 상태로 커밋하고 수동 검토
- 메인 에이전트가 직접 개입하여 수정
- 요구사항을 재정의하고 해당 frontend 마일스톤 재시작
- 해당 frontend 마일스톤을 스킵하고 다음으로 진행
- 전체 중단

## 완료 보고

frontend 마일스톤 완료 시 아래 항목을 요약한다.

- D/A/B input/output 파일 경로
- frontend 변경 파일 수와 주요 변경 요약
- 실행한 build/test 또는 브라우저 검증 결과
- frontend architecture review 통과 여부
- backend 마일스톤으로 넘겨야 할 API 계약 또는 미해결 사항
