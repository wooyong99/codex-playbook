---
name: implement
description: 요구사항을 마일스톤 단위로 분해하여 설계 문서 작성(D) → 코드 작성(A) → 아키텍처 검토(B) → 수정 루프를 오케스트레이션하는 스킬. 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경 등 코드 작업이 필요한 모든 상황에서 사용한다. "구현해줘", "만들어줘", "추가해줘", "리팩토링", "implement", "/implement" 같은 요청에 이 스킬을 사용한다.
---

# implement — 코드 작성 및 검토 오케스트레이션

## 역할

- 사용자의 구현·리팩토링 요구사항을 마일스톤 단위로 분해한다.
- 각 마일스톤을 기술설계(D), 코드 작성(A), 아키텍처 검토(B), 위반 수정 루프로 실행한다.
- 메인 에이전트는 요구사항 분석, 마일스톤 분할, 서브에이전트 호출, handoff 검증, 반복 종료 판단, 사용자 보고를 담당한다.
- D/A/B 사이의 통신은 메인 에이전트가 관리하며, 정상 산출물은 handoff artifact와 체크포인트 파일로 전달한다.
- 세부 입출력 포맷과 체크포인트 규격은 역할별 계약 문서가 단일 출처다.

## 기본 범위

- 포함: 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경, 구현에 필요한 TDD 작성, 아키텍처 규칙 검토
- 제외: 요구사항만 정리하는 PRD 작업, 구현이 없는 문서 정리, 아키텍처 검토만 단독 수행하는 작업
- 예외: 자동 A-B 루프가 수렴하지 않아 사용자가 직접 개입을 선택한 경우에만 메인 에이전트가 직접 수정할 수 있다.

## 참조 문서

- 역할 경계와 서브에이전트 운영 원칙: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- 요구사항 분석과 마일스톤 분할 기준: [references/milestone-planning.md](references/milestone-planning.md)
- handoff artifact와 체크포인트 처리 규약: [references/handoff-checkpoint-protocol.md](references/handoff-checkpoint-protocol.md)
- 마일스톤별 D/A/B 실행 루프: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)
- D 계약: [references/technical-design-writer-contract.md](references/technical-design-writer-contract.md)
- A 계약: [references/implementation-engineer-contract.md](references/implementation-engineer-contract.md)
- B 계약: [references/backend-architecture-reviewer-contract.md](references/backend-architecture-reviewer-contract.md)

## 프로세스

### 1. 요구사항을 분석한다

- 사용자 요청을 한 문장으로 재진술해 목표를 고정한다.
- 애매하거나 중요한 정보가 누락되면 구현 전에 사용자에게 확인한다.
- 요구사항, 명시적 제외사항, 성공 기준을 구분한다.
- 세부 기준은 [milestone-planning.md](references/milestone-planning.md)를 따른다.

### 2. 마일스톤을 분할한다

- 사용자 관점의 독립 결과, 도메인 경계, 트랜잭션 경계, 검토 범위를 기준으로 나눈다.
- 각 마일스톤에는 목표, 범위, 명시적 제외사항, 예상 변경 규모, 검증 기준을 둔다.
- 큰 작업은 사용자 확인 후 진행한다.
- 분할 기준은 [milestone-planning.md](references/milestone-planning.md)를 따른다.

### 3. 실행 준비를 한다

- run id를 만들고 `.agents/runs/{run_id}` 아래 handoff와 checkpoint 경로를 할당한다.
- 각 서브에이전트 호출 전 `[결과 파일]`과 `[체크포인트 파일]` 절대 경로를 정한다.
- 역할별 프롬프트는 해당 계약 문서의 Input 형식을 따른다.
- 파일명과 검증 규칙은 [handoff-checkpoint-protocol.md](references/handoff-checkpoint-protocol.md)를 따른다.

### 4. 마일스톤별 D/A/B 루프를 실행한다

- D는 마일스톤 TDD를 작성하거나 스킵 근거를 남긴다.
- A는 D 결과 파일을 읽고 구현 또는 수정 결과를 handoff artifact로 남긴다.
- B는 A 결과 파일의 변경 파일만 문서 규칙과 대조해 검토한다.
- 위반이 있으면 같은 마일스톤의 A 인스턴스에 수정 작업을 맡기고 B를 새 인스턴스로 다시 호출한다.
- 상세 루프는 [milestone-execution-workflow.md](references/milestone-execution-workflow.md)를 따른다.

### 5. 체크포인트와 실패를 처리한다

- `CONTEXT_CHECKPOINT:` 응답은 완료로 처리하지 않고 체크포인트 복구 절차로만 처리한다.
- 정상 결과도 `[결과 파일]`과 `[체크포인트 파일]`을 모두 검증한 뒤 다음 단계로 넘긴다.
- A-B 루프가 제한 횟수 안에 수렴하지 않으면 사용자에게 선택지를 제시한다.
- 공통 처리 규약은 [handoff-checkpoint-protocol.md](references/handoff-checkpoint-protocol.md)와 [milestone-execution-workflow.md](references/milestone-execution-workflow.md)를 따른다.

### 6. 완료 보고를 한다

- 완료된 마일스톤 수, A-B 라운드 수, 변경 파일, 검증 결과를 요약한다.
- 마지막 handoff artifact 경로와 남은 불확실성을 보고한다.
- 필요한 경우 커밋 그룹핑 또는 커밋 작성을 다음 단계로 제안한다.

## 완료 산출물

- 마일스톤별 D/A/B 결과 파일 경로
- 변경 파일 목록과 검증 결과 요약
- 아키텍처 검토 통과 여부와 남은 위반
- 자동 수렴 실패 또는 사용자 확인이 필요한 항목
