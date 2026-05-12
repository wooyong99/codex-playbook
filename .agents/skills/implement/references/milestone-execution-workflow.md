# Milestone Execution Workflow

이 문서는 `implement` 스킬 패밀리의 마일스톤별 실행 루프를 소유한다. 역할별 프롬프트 필드와 출력 스키마는 각 계약 문서가 단일 출처이며, 파일 검증 절차는 [handoff-checkpoint-protocol.md](handoff-checkpoint-protocol.md)를 따른다.

## 전체 흐름

각 마일스톤은 아래 순서로 실행한다.

1. D를 호출해 TDD를 작성하거나 스킵 근거를 받는다.
2. 마일스톤 영역에 맞는 A를 호출해 구현 결과를 받는다.
3. 변경 영역에 맞는 B와 필요한 supplemental reviewer를 호출해 변경 파일의 문서 준수 여부를 검토한다.
4. 위반이 있으면 해당 영역의 A에게 수정 작업을 맡기고 reviewer를 다시 호출한다.
5. 호출된 모든 B와 필수 supplemental reviewer가 `pass`를 반환하면 다음 마일스톤으로 넘어간다.
6. A-B 루프가 제한 횟수를 넘으면 사용자에게 escalation 선택지를 제시한다.

## Step 1. 마일스톤 시작

- 현재 마일스톤을 진행 중으로 표시한다.
- 해당 마일스톤의 목표, 범위, 명시적 제외사항, 검증 기준을 다시 확인한다.
- 이번 마일스톤의 handoff와 checkpoint 경로를 할당한다.

## Step 2. Agent D 위임

마일스톤 영역에 맞는 D와 계약 문서를 먼저 고른다.

- 백엔드 마일스톤은 `backend-technical-design-writer`를 호출하고, 프롬프트는 [backend-technical-design-writer-contract.md](backend-technical-design-writer-contract.md)의 Input 형식으로 구성한다.
- 프론트엔드 마일스톤은 `frontend-technical-design-writer`를 호출하고, 프롬프트는 [frontend-technical-design-writer-contract.md](frontend-technical-design-writer-contract.md)의 Input 형식으로 구성한다.
- 백엔드와 프론트엔드가 모두 필요한 요청은 마일스톤을 가능한 한 영역별로 분리한다.
- 단일 마일스톤 안에서 분리할 수 없으면 backend D와 frontend D를 별도 `[결과 파일]`, `[체크포인트 파일]`로 각각 호출하고, 영역별 D 결과 파일을 A 단계로 넘긴다.

필수 입력:

- 마일스톤 제목과 요구사항
- 명시적 제외사항
- 실제 저장소 기준 프로젝트 컨텍스트
- `[결과 파일]`
- `[체크포인트 파일]`

응답 처리:

- `CONTEXT_CHECKPOINT:`이면 [handoff-checkpoint-protocol.md](handoff-checkpoint-protocol.md)의 체크포인트 공통 처리로 재호출한다.
- `TDD_CREATED:`이면 D 결과 파일을 검증하고 `payload.tdd_path`와 D 결과 파일 경로를 보관한다.
- `TDD_SKIPPED:`이면 D 결과 파일을 검증하고 `payload.skip_reason`과 D 결과 파일 경로를 보관한다.

아래 조건 중 하나라도 만족하면 `TDD_SKIPPED`를 그대로 수용하지 않고 D를 한 번 더 재호출해 스킵 근거를 재확인한다.

- 마일스톤이 2개 이상 레이어에 걸친다.
- 새로운 도메인 개념, 이벤트, 예외 전략, 트랜잭션 경계, 동시성 제어가 포함된다.
- 사용자가 복잡한 변경, 대규모 리팩토링, 엔터프라이즈급 같은 표현으로 설계 리스크를 명시했다.

재확인 후에도 D가 `TDD_SKIPPED`를 유지하면 그 이유를 사용자 업데이트에 짧게 노출한 뒤 A 단계로 진행한다.

## Step 3. Agent A 라우팅 및 위임

프롬프트는 [implementation-engineer-contract.md](implementation-engineer-contract.md)의 Input Case A 형식으로 구성한다. A에게는 설계 요약 원문을 복사하지 않고 D 결과 파일 경로를 전달한다.

호출 대상:

- 백엔드 코드, backend 문서, DB/schema, 서버 설정 변경은 `backend-implementation-engineer`를 호출한다.
- 프론트엔드 코드, frontend 문서, UI/상태/API client/cache/rendering 변경은 `frontend-implementation-engineer`를 호출한다.
- 백엔드와 프론트엔드가 모두 필요한 요청은 마일스톤을 가능한 한 영역별로 분리한다.
- 단일 마일스톤 안에서 분리할 수 없으면 backend A와 frontend A를 별도 `[결과 파일]`, `[체크포인트 파일]`로 각각 호출하고, `payload.changed_files`와 `payload.verification`을 합쳐 검토 단계로 넘긴다.

응답 처리:

- `CONTEXT_CHECKPOINT:`이면 체크포인트 공통 처리로 같은 A 인스턴스를 재호출한다.
- `IMPLEMENTATION_COMPLETED:`이면 A 결과 파일을 검증하고 `payload.changed_files`, `payload.design_decisions`, `payload.verification`을 필요한 범위에서 읽는다.
- `verification.compile.exit_code`, `verification.tests.exit_code`가 누락됐거나 실패면 마일스톤을 성공으로 간주하지 않는다.
- 검증 실패는 A 재호출 또는 사용자 보고로 처리하고 B 검토로 넘기지 않는다.

## Step 4. Agent B 라우팅 및 Reviewer 위임

백엔드 변경 파일이 있으면 `backend-architecture-reviewer`를 호출하고, 프롬프트는 [backend-architecture-reviewer-contract.md](backend-architecture-reviewer-contract.md)의 Input 형식으로 구성한다. 프론트엔드 변경 파일이 있으면 `frontend-architecture-reviewer`를 호출하고, 프롬프트는 [frontend-architecture-reviewer-contract.md](frontend-architecture-reviewer-contract.md)의 Input 형식으로 구성한다. B에게는 A 구현 결과 파일, D 설계 결과 파일, B의 `[결과 파일]`, `[체크포인트 파일]`을 전달한다.

변경 파일이 문서 또는 보안 민감 영역을 포함하면 [review routing](../../../../docs/review/README.md)에 따라 supplemental reviewer를 추가로 적용한다. supplemental reviewer 결과도 Rule ID, severity, source_path를 포함해야 하며, `blocker` 또는 `major` 위반은 B 위반과 동일하게 수정 루프로 보낸다.

응답 처리:

- `CONTEXT_CHECKPOINT:`이면 체크포인트 공통 처리로 새 B 인스턴스를 재호출한다. 완료된 파일의 위반 결과는 체크포인트 파일의 `완료된 결과` 섹션에서 복원한다.
- `REVIEW_COMPLETED:`이면 B 결과 파일을 검증하고 `status`와 `payload.violations`를 읽는다.
- 호출된 모든 B와 필수 supplemental reviewer의 `status: pass`가 확인되면 마일스톤을 완료한다.
- `status: violations`이면 위반 수정 단계로 진행한다.

B 결과는 사용자에게 짧게 요약한다. 위반이 있으면 파일명과 위반 규칙 요약만 한 줄씩 노출한다.

## Step 5. 위반 수정

위반 수정은 같은 마일스톤의 해당 영역 A 인스턴스를 이어서 사용한다. 프롬프트는 [implementation-engineer-contract.md](implementation-engineer-contract.md)의 Input Case B 형식으로 구성하고, 위반 항목 원문은 프롬프트에 복사하지 않는다. reviewer 결과 파일 경로만 전달한다.

- `backend-architecture-reviewer`가 보고한 backend 위반은 `backend-implementation-engineer`가 수정한다.
- `frontend-architecture-reviewer`가 보고한 frontend 위반은 `frontend-implementation-engineer`가 수정한다.
- 문서 전용 위반은 메인 에이전트가 직접 수정하지 않고 사용자에게 별도 문서 작업으로 보고하거나, 문서 작업이 명시된 경우에만 문서 전담 흐름으로 처리한다.

응답 처리:

- `CONTEXT_CHECKPOINT:`이면 체크포인트 공통 처리로 같은 A 인스턴스를 재호출한다.
- `FIX_APPLIED:`이면 A 수정 결과 파일을 검증하고 `payload.changed_files`, `payload.applied`, `payload.failed`, `payload.verification`을 읽는다.
- 새로 수정된 파일이 있으면 마일스톤 변경 파일 집합에 합친다.
- compile 또는 tests 검증이 누락·실패하면 재검토로 진행하지 않는다.
- `verification.tests.result`가 `not_run`이면 이유를 사용자에게 노출하고, 허용 가능한 빠른 수정인지 확인된 경우에만 재검토로 진행한다.

수정 후에는 해당 reviewer를 새 인스턴스로 다시 호출한다.

## Step 6. 반복 종료

- 호출된 모든 B와 필수 supplemental reviewer가 `status: pass`를 반환하면 마일스톤을 완료한다.
- B가 `status: violations`를 반환하면 위반 수정 단계로 돌아간다.
- A-B 반복은 최대 5회까지만 자동 수행한다.
- 5회를 넘으면 escalation 단계로 넘어간다.

## Escalation

자동 수렴에 실패하면 마지막 검토 결과를 3~5줄로 요약하고 사용자 선택을 기다린다.

선택지:

- 현재 상태로 커밋하고 수동 검토
- 메인 에이전트가 직접 개입하여 수정
- 요구사항을 재정의하고 해당 마일스톤 재시작
- 해당 마일스톤을 스킵하고 다음으로 진행
- 전체 중단

메인 에이전트 직접 수정은 사용자가 그 선택지를 고른 경우에만 허용한다. 직접 수정 시에는 마지막 A 결과 파일, 마지막 B 결과 파일, 관련 체크포인트 파일을 읽고 충돌 여부를 먼저 정리한다. 이후 수정 범위와 성공 기준을 3줄 이내로 다시 고정하고, 수정 뒤 빌드와 테스트 결과를 사용자에게 보고한다. 가능하면 새 B 인스턴스로 최종 문서 준수 재검토를 한 번 더 수행한다.

## 전체 완료 보고

모든 마일스톤이 완료되면 아래 항목을 요약한다.

- 완료 마일스톤 수와 전체 마일스톤 수
- 총 A-B 라운드 수와 마일스톤별 라운드 수
- 변경 파일 수와 주요 변경 요약
- 실행한 컴파일·테스트 명령과 결과
- 남은 불확실성 또는 사용자 확인이 필요한 항목
- 커밋 그룹핑 또는 커밋 작성 제안
