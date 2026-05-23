# Frontend Implementation Engineer — Case Contract

`implement-frontend` 스킬이 `frontend-implementation-engineer` 서브에이전트와 주고받는 Case 기반 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/frontend-implementation-engineer.toml`)이 아닌 이 문서가 frontend 구현·수정 입력 Markdown 섹션, 출력 Markdown 섹션, 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿의 단일 출처다.

## 문서 역할

이 문서는 Frontend Implementation Engineer의 파일 기반 인터페이스만 정의한다.

- Frontend Implementation Engineer의 역할 철학은 `.codex/agents/frontend-implementation-engineer.toml`이 제공한다.
- Implementation Engineer 호출과 재호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 결정한다.
- 이 문서는 신규 구현 Case, 위반 수정 Case, Markdown input/output 섹션, 결과 신호, 체크포인트 기준만 소유한다.
- 메인 에이전트는 design/review output을 읽고 implementation input으로 재구성한다.

## 공통 원칙

- 메인 에이전트는 호출 전에 Markdown `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 모두 할당한다.
- 메인 에이전트는 계약 문서의 해당 Case에서 출력 규격과 체크포인트 규격을 가져와 `[입력 파일]`에 포함한다.
- 서브에이전트는 `[입력 파일]`의 출력 규격에 따라 `[출력 파일]`과 `[체크포인트 파일]`을 저장한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.
- 정상 완료 응답 본문에는 artifact 내용을 복사하지 않는다.

## Case 1. 신규 구현

### 목적

Design Writer의 결과와 Source of Truth를 기준으로 frontend 코드를 구현하고 build/test/browser 검증 결과를 남긴다.

### 호출 프롬프트

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-implementation-r00-input.v1.md
[계약 파일]: .agents/skills/implement-frontend/references/frontend-implementation-engineer-contract.md
[지시]: 입력 파일을 읽고 입력 파일의 출력 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

### 입력 파일 섹션

`[입력 파일]`은 Markdown으로 작성하며 아래 섹션을 포함한다.

```text
# Frontend Implementation Input
## Metadata
## 목표
## 명시적 제외사항
## Source of Truth
## 선행 산출물
## 구현 지시
## 출력 규격
## 체크포인트 규격
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-implementation-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-implementation-engineer
kind: implementation_input
iteration: 0
created_at: <ISO-8601 timestamp>
output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-implementation-r00-result.v1.md
checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/implementation-r00-v001.md
```

### 입력 규칙

- `[명시적 제외사항]`은 구현 범위에서 제외한다.
- 신규 구현은 `[입력 파일]`의 `선행 산출물`과 `Source of Truth` 섹션을 기준으로 수행한다.
- `[구현 지시]`에는 확정 요구사항 컨텍스트 경로를 포함할 수 있다.
- 확정 요구사항 컨텍스트가 있으면 `요구사항 결정`, `사용자 확인 필요 없음`, `금지된 추론`, `backend 계약/미확정 사항`, `검증 기준`, `남은 미결정 사항`을 구현 경계로 사용한다.
- Implementation Engineer는 확정 요구사항 컨텍스트에 없는 제품 UX, navigation flow, API shape, cache freshness, invalidation, optimistic update, destructive action, form validation 정책을 임의로 구현하지 않는다.
- `[출력 파일]`은 `[입력 파일]`의 `Metadata.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `Metadata.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `체크포인트 규격` 섹션을 기준으로 판단한다.

Source of Truth 후보:

- `docs/frontend/README.md`
- `docs/frontend/architecture/**`
- `docs/frontend/conventions/**`
- `docs/frontend/performance/**`
- `docs/frontend/ui-ux/**`
- `[입력 파일]`의 `선행 산출물`이 가리키는 design result의 TDD 경로

체크포인트 재호출 시 아래 필드가 추가된다.

```text
[체크포인트]: [입력 파일]의 `Metadata.checkpoint_file` 경로 참조.
완료된 작업은 건너뛰고 남은 작업부터 이어서 수행.
```

### 출력 규격

Implementation Engineer는 작업 완료 후 `[출력 파일]`에 아래 Markdown 섹션을 저장한다.

```text
# Frontend Implementation Result
## Metadata
## 상태
## 변경 요약
## 변경 파일
## 구현 결정
## 검증 결과
## 확인 필요 사항
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-implementation/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-implementation-engineer
kind: implementation_result
iteration: 0
created_at: <ISO-8601 timestamp>
```

필드 규칙:

- `schema_version`: 항상 `implement-frontend-implementation/v1`
- `role`: 항상 `frontend-implementation-engineer`
- `kind`: 항상 `implementation_result`
- `## 상태`: `completed`
- `## 변경 파일`: 절대 경로와 1~2줄 변경 요약을 포함한다.
- `## 검증 결과`: build/compile, tests, browser 또는 visual 검증 각각의 명령, exit code 또는 미실행 사유, `success | failure | not_run`, 요약을 포함한다.
- `## 확인 필요 사항`: 없으면 `없음`으로 쓴다.

### 정상 완료 포맷

먼저 `[출력 파일]`에 implementation artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
IMPLEMENTATION_COMPLETED: {[출력 파일] 절대 경로}
```

정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 변경·검증 결론으로 수렴할 수 있는 최소 근거를 남긴다.

## Case 2. 위반 수정

### 목적

Architecture Reviewer가 확정한 위반만 수정하고, 위반과 무관한 코드는 변경하지 않는다.

### 호출 프롬프트

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-implementation-r{iter}-input.v1.md
[계약 파일]: .agents/skills/implement-frontend/references/frontend-implementation-engineer-contract.md
[지시]: 입력 파일을 읽고 입력 파일의 출력 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

### 입력 파일 섹션

`[입력 파일]`은 Markdown으로 작성하며 아래 섹션을 포함한다.

```text
# Frontend Fix Input
## Metadata
## 목표
## 수정 대상 위반
## Source of Truth
## 선행 산출물
## 수정 지시
## 출력 규격
## 체크포인트 규격
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-fix-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-implementation-engineer
kind: fix_input
iteration: <implementation-review 루프 iter>
created_at: <ISO-8601 timestamp>
output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-implementation-r{iter}-fix-result.v1.md
checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/implementation-r{iter}-v001.md
```

### 입력 규칙

- 위반 수정은 `[입력 파일]`의 `수정 대상 위반`과 `선행 산출물`이 가리키는 review output만 기준으로 수행한다.
- `수정 대상 위반`에는 reviewer output 파일 경로와 수정 대상 violation 식별자만 둔다.
- 위반 본문 원문을 복사하지 않고 reviewer output 파일 경로를 참조한다.
- `[수정 지시]`에는 확정 요구사항 컨텍스트 경로를 포함할 수 있다.
- 확정 요구사항 컨텍스트에 없는 UX/API/cache/navigation 정책을 위반 수정 과정에서 새로 만들지 않는다.
- `[출력 파일]`은 `[입력 파일]`의 `Metadata.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `Metadata.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `체크포인트 규격` 섹션을 기준으로 판단한다.

### 출력 규격

Implementation Engineer는 수정 완료 후 `[출력 파일]`에 아래 Markdown 섹션을 저장한다.

```text
# Frontend Fix Result
## Metadata
## 상태
## 수정 요약
## 변경 파일
## 적용한 위반
## 적용 실패
## 검증 결과
## 확인 필요 사항
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-implementation/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-implementation-engineer
kind: fix_result
iteration: <implementation-review 루프 iter>
created_at: <ISO-8601 timestamp>
```

필드 규칙:

- `schema_version`: 항상 `implement-frontend-implementation/v1`
- `role`: 항상 `frontend-implementation-engineer`
- `kind`: 항상 `fix_result`
- `## 상태`: `fixed | partial | failed`
- `## 변경 파일`: 절대 경로와 이번 수정으로 바뀐 내용을 포함한다.
- `## 적용 실패`: 실패 항목이 없으면 `없음`으로 쓴다.
- `## 검증 결과`: build/compile, tests, browser 또는 visual 검증 각각의 명령, exit code 또는 미실행 사유, `success | failure | not_run`, 요약을 포함한다.
- `## 확인 필요 사항`: 없으면 `없음`으로 쓴다.

### 정상 완료 포맷

먼저 `[출력 파일]`에 fix artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
FIX_APPLIED: {[출력 파일] 절대 경로}
```

정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 변경·검증 결론으로 수렴할 수 있는 최소 근거를 남긴다.

## 공통 체크포인트 규격

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `IMPLEMENTATION_COMPLETED:` 또는 `FIX_APPLIED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 구현 배치가 끝나고 다른 frontend 책임 영역으로 넘어간다.
- 변경 집합 또는 테스트 기대값이 서로 맞물려 보존이 필요하다.
- 위반 수정 흐름이 다른 위반 묶음으로 넘어간다.
- 빌드/테스트 실패가 수정 방향 전환을 요구한다.
- 요구사항 또는 명시적 제외사항 경계가 불명확해진다.

체크포인트가 필요한 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`IMPLEMENTATION_COMPLETED`, `FIX_APPLIED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Frontend Implementation Engineer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | changed_file_batch | implementation_batch_done | violation_batch_done | verification_failure | read_batch_done | requirement_boundary | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
- `## 완료된 작업`
- `## 진행중 작업`
- `## 남은 작업`
- `## 발견한 버그`
- `## 주의사항`
- `## 실패 패턴`
- `## 최근 결정`
- `## 검증 상태`
- `## 관련 파일`
- `## 진행 상태`
