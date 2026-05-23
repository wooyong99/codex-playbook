# Frontend Milestone Execution Workflow

이 문서는 `implement-frontend` 스킬의 frontend 마일스톤 실행 흐름을 정의한다.

핵심 책임 경계는 [../SKILL.md](../SKILL.md)가 소유하고, 상세 경계는 [orchestration-boundaries.md](orchestration-boundaries.md)가 소유한다. 역할별 input/output schema는 각 frontend 계약 문서가 소유한다. 파일 검증과 체크포인트 복구 절차는 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.

## 실행 모델

각 frontend 마일스톤은 design/implementation/review 역할을 파일 기반으로 연결한다.

```text
Main agent
  -> Requirement clarification gate
  -> Clarified frontend requirement context
  -> Milestone planning
  -> Frontend Design Writer input
  -> design output
  -> Frontend Implementation Engineer input
  -> implementation output
  -> Frontend Architecture Reviewer input
  -> architecture review output
  -> pass or implementation fix input
```

메인 에이전트는 각 단계 사이에서 이전 output을 검증하고 다음 input을 만든다. 이 변환은 단순 포맷 변환이 아니라 현재 마일스톤 상태, Source of Truth, 제외사항, 확정 요구사항 컨텍스트, 검증 결과, reviewer 위반, backend API 계약 불확실성을 반영하는 오케스트레이션 책임이다.

## 단계 개요

0. 요구사항 명확화 게이트: 구현 방식에 영향을 주는 frontend 정책을 확정하거나 사용자에게 질문한다.
1. 마일스톤 시작: 범위, 제외사항, 검증 기준, 확정 요구사항 컨텍스트, run artifact 경로를 확정한다.
2. Frontend Design Writer 위임: frontend TDD를 작성하거나 스킵 근거를 받는다.
3. Frontend Implementation Engineer 위임: frontend 구현 또는 수정을 수행한다.
4. Frontend Architecture Reviewer 위임: frontend 아키텍처 기준 준수 여부를 검토한다.
5. 위반 수정: 같은 Frontend Implementation Engineer 인스턴스에 수정 작업을 맡긴다.
6. 반복 종료: Frontend Architecture Reviewer가 통과하면 완료하고, 반복 한계를 넘으면 escalation한다.

## 공통 운영 규칙

- Frontend Design Writer와 Frontend Architecture Reviewer는 매번 새 인스턴스로 호출한다.
- Frontend Implementation Engineer는 마일스톤 첫 구현에서 새 인스턴스로 시작하고, 같은 마일스톤의 위반 수정과 체크포인트 재개에서는 동일 인스턴스를 이어서 사용한다.
- 마일스톤이 바뀌면 Frontend Implementation Engineer도 새 인스턴스로 시작한다.
- 각 역할 호출마다 해당 계약 문서의 Case에 있는 `체크포인트 규격`을 입력 파일에 포함한다.
- 각 역할 호출 전에 `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 모두 할당한다.
- Source of Truth 후보 중 이번 변경과 직접 관련된 문서만 input artifact에 넣는다.
- 확정 요구사항 컨텍스트가 있으면 design/implementation/review input artifact에 경로로 연결한다.
- 정상 산출물과 체크포인트 파일은 모두 검증한 뒤 다음 단계로 진행한다.

## Step 0. 요구사항 명확화 게이트

목적:

- 추상적인 frontend 요청을 구현 가능한 요구사항으로 좁힌다.
- UX, API, 상태, cache, rendering, 검증 정책을 AI가 임의로 추론하지 못하게 한다.
- Frontend Design Writer가 미확정 UX/API/cache/navigation 정책을 설계 결정으로 확정하지 않도록 입력 경계를 만든다.

처리:

- [requirement-clarification-gate.md](requirement-clarification-gate.md)에 따라 사용자 흐름, 진입 경로/라우팅, 화면 상태, interaction lifecycle, API 계약, state ownership, cache/invalidation, form/submit 정책, UX 실패 처리, responsive/a11y, design source, 렌더링 성능, 브라우저 검증 기준을 확인한다.
- 구현 방식에 영향을 주는 정보가 누락되면 design/implementation/review artifact를 만들기 전에 중단하고 사용자에게 질문한다.
- 질문은 사용자 흐름과 대상 화면, API 계약과 backend dependency, 상태 소유권과 interaction state, cache/invalidation 순서로 우선한다.
- 단순 UI copy 수정 또는 국소 component 스타일 조정처럼 결정 영향도가 낮으면 확정된 기본값과 코드베이스 관례 기반 가정을 기록하고 진행할 수 있다.
- 게이트를 통과하면 `요구사항 결정`, `사용자 확인 필요 없음`, `금지된 추론`, `backend 계약/미확정 사항`, `검증 기준`, `남은 미결정 사항`을 확정 요구사항 컨텍스트로 남긴다.

## Step 1. 마일스톤 시작

고수준 확인:

- 현재 frontend 마일스톤을 진행 중으로 표시한다.
- 목표, 범위, 명시적 제외사항, 확정 요구사항 컨텍스트, build/test 또는 브라우저 검증 기준을 다시 확인한다.
- 이번 마일스톤의 input, output, checkpoint 경로를 할당한다.
- frontend Source of Truth 후보에서 이번 변경과 직접 관련된 문서만 선별한다.
- backend API 계약이 불확실하면 Frontend Implementation Engineer 구현 전에 계약 불확실성으로 보고하거나 backend 마일스톤 선행을 요청한다.

세부 파일 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)를 따른다.

## Step 2. Frontend Design Writer 위임

목적:

- frontend 설계가 필요한 경우 TDD를 작성한다.
- TDD가 불필요하면 스킵 근거를 output artifact로 남긴다.

처리:

- 호출 전 [frontend-technical-design-writer-contract.md](frontend-technical-design-writer-contract.md)의 Case 1 형식으로 design input artifact를 저장한다.
- design input artifact에는 확정 요구사항 컨텍스트 경로를 포함한다.
- 호출 프롬프트에는 `[입력 파일]` 경로와 계약 파일 경로만 전달한다.
- `TDD_CREATED:`이면 design output을 검증하고 TDD 경로와 design output 경로를 보관한다.
- `TDD_SKIPPED:`이면 design output을 검증하고 스킵 근거와 design output 경로를 보관한다.
- `TDD_BLOCKED:`이면 design output을 검증하고 `설계 불가 사유`를 읽은 뒤 구현으로 진행하지 않고 Step 0으로 돌아가 사용자 질문을 만든다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 재호출한다.

`TDD_SKIPPED` 재확인 조건:

- 마일스톤이 route/page, feature/entity, state/API/cache 중 2개 이상 책임 영역에 걸친다.
- 새로운 상태 소유권, query key/cache 전략, error boundary, routing 구조가 포함된다.
- responsive layout, 접근성, 렌더링 성능, 브라우저 검증 리스크가 포함된다.
- 사용자가 복잡한 변경, 대규모 리팩토링, 엔터프라이즈급 같은 표현으로 설계 리스크를 명시했다.

## Step 3. Frontend Implementation Engineer 위임

목적:

- design output과 Source of Truth를 기준으로 frontend 코드를 구현한다.
- build/test/browser 검증 결과를 output artifact에 남긴다.

처리:

- 호출 전 [frontend-implementation-engineer-contract.md](frontend-implementation-engineer-contract.md)의 Case 1 형식으로 implementation input artifact를 저장한다.
- implementation input artifact에는 design output 경로를 기록하고, 설계 요약 원문은 복사하지 않는다.
- implementation input artifact에는 확정 요구사항 컨텍스트 경로를 포함한다.
- `IMPLEMENTATION_COMPLETED:`이면 implementation output을 검증한다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 같은 Frontend Implementation Engineer 인스턴스를 재호출한다.
- `검증 결과` 섹션의 build/compile 또는 tests 결과가 누락됐거나 실패면 마일스톤을 성공으로 간주하지 않는다.
- 브라우저 검증이 필요한데 실행되지 않았으면 이유를 사용자에게 노출하고, architecture review 전에 허용 가능한지 판단한다.
- 검증 실패는 Frontend Implementation Engineer 재호출 또는 사용자 보고로 처리하고 architecture review로 넘기지 않는다.

## Step 4. Frontend Architecture Reviewer 위임

목적:

- A가 변경한 frontend 파일이 입력된 Source of Truth와 TDD 결정에 맞는지 검토한다.

처리:

- frontend 변경 파일이 있으면 [frontend-architecture-reviewer-contract.md](frontend-architecture-reviewer-contract.md)의 Case 1 형식으로 architecture review input artifact를 저장한다.
- architecture review input artifact에는 implementation output 경로, design output 경로, 이번 검토의 Source of Truth, output/checkpoint 경로, 체크포인트 규격을 기록한다.
- architecture review input artifact에는 확정 요구사항 컨텍스트 경로를 포함한다.
- 기준 문서와 TDD 결정은 architecture review input artifact로 전달하며 agent TOML이 정적으로 소유하지 않는다.
- `REVIEW_COMPLETED:`이면 architecture review output을 검증하고 판정과 위반 목록을 읽는다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 새 Frontend Architecture Reviewer 인스턴스를 재호출한다.
- `pass` 판정이 확인되면 마일스톤을 완료한다.
- `violations` 판정이면 위반 수정 단계로 진행한다.

## Step 5. 위반 수정

목적:

- reviewer가 확정한 위반만 수정한다.
- 위반과 무관한 코드는 변경하지 않는다.

처리:

- 같은 마일스톤의 Frontend Implementation Engineer 인스턴스를 이어서 사용한다.
- [frontend-implementation-engineer-contract.md](frontend-implementation-engineer-contract.md)의 Case 2 형식으로 fix input artifact를 저장한다.
- fix input artifact에는 reviewer output 파일 경로만 기록하고 위반 본문을 복사하지 않는다.
- `FIX_APPLIED:`이면 fix output을 검증한다.
- `CONTEXT_CHECKPOINT:`이면 체크포인트 복구 절차로 같은 Frontend Implementation Engineer 인스턴스를 재호출한다.
- 새로 수정된 파일이 있으면 마일스톤 변경 파일 집합에 합친다.
- build 또는 tests 검증이 누락·실패하면 재검토로 진행하지 않는다.
- 수정 후에는 Frontend Architecture Reviewer를 새 인스턴스로 다시 호출한다.

## Step 6. 반복 종료

- Frontend Architecture Reviewer가 `pass`를 반환하면 frontend 마일스톤을 완료한다.
- Frontend Architecture Reviewer가 `violations`를 반환하면 위반 수정 단계로 돌아간다.
- implementation-review 반복은 최대 5회까지만 자동 수행한다.
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

- design/implementation/review input/output 파일 경로
- frontend 변경 파일 수와 주요 변경 요약
- 실행한 build/test 또는 브라우저 검증 결과
- frontend architecture review 통과 여부
- backend 마일스톤으로 넘겨야 할 API 계약 또는 미해결 사항
