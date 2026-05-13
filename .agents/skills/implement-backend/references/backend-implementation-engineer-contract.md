# Backend Implementation Engineer — Input / Output Contract

`implement-backend` 스킬이 `backend-implementation-engineer` 서브에이전트와 주고받는 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/backend-implementation-engineer.toml`)이 아닌 이 문서가 backend 구현 입출력 포맷, 체크포인트 판단 기준, 체크포인트 파일 템플릿의 단일 출처다.

---

## Input

### Case A — 신규 구현

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-A-r00-input.v1.yaml
[계약 파일]: .agents/skills/implement-backend/references/backend-implementation-engineer-contract.md
[지시]: 입력 파일을 읽고 계약 파일의 Output > Case A 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

`[입력 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-backend-implementation-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-implementation-engineer
kind: implementation_input
iteration: 0
created_at: <ISO-8601 timestamp>
input:
  milestone_title: <마일스톤 제목>
  requirements: <구체적 범위·목표>
  explicit_exclusions: <사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음">
  project_context:
    area: backend
    stack_or_modules:
      - <실제 저장소 문서에서 확인한 backend 스택/모듈/의존 방향>
    related_docs:
      - <docs/backend 하위에서 실제로 필요한 문서>
    related_domain_or_feature: <도메인명 또는 backend 기능명>
  source_of_truth:
    - path: <이번 구현에 적용할 backend 기준 문서 또는 섹션>
      reason: <선별 이유>
  design_result_file: <D가 반환한 design_result output artifact 절대 경로>
artifacts:
  output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-A-r00-implementation-result.v1.yaml
  checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/A-r00-v001.md
checkpoint:
  criteria: "[체크포인트 판단 기준] 이 문서의 Input > 역할별 체크포인트 기준 그대로."
output_contract:
  path: .agents/skills/implement-backend/references/backend-implementation-engineer-contract.md
  section: Output > Case A
```

### Case B — 위반 수정

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-A-r{iter}-input.v1.yaml
[계약 파일]: .agents/skills/implement-backend/references/backend-implementation-engineer-contract.md
[지시]: 입력 파일을 읽고 계약 파일의 Output > Case B 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

`[입력 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-backend-fix-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-implementation-engineer
kind: fix_input
iteration: <A-B 루프 iter>
created_at: <ISO-8601 timestamp>
input:
  task: 이전 backend architecture review에서 위반이 발견됐습니다.
  review_result_file: <B가 반환한 review_result output artifact 절대 경로>
  rules:
    - 위반 항목 외 코드는 변경하지 말 것.
    - 모든 수정 후 컴파일 성공 확인.
artifacts:
  output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-A-r{iter}-fix-result.v1.yaml
  checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/A-r{iter}-v001.md
checkpoint:
  criteria: "[체크포인트 판단 기준] 이 문서의 Input > 역할별 체크포인트 기준 그대로."
output_contract:
  path: .agents/skills/implement-backend/references/backend-implementation-engineer-contract.md
  section: Output > Case B
```

## Input Rules

- `[명시적 제외사항]`은 구현 범위에서 제외한다.
- 신규 구현은 `[입력 파일]`의 `input.design_result_file`과 `input.source_of_truth`를 기준으로 수행한다.
- 위반 수정은 `[입력 파일]`의 `input.review_result_file`이 가리키는 `payload.violations`와 그 안의 `source_path`, `rule`, `reason`만 기준으로 수행한다.
- `[출력 파일]`은 `[입력 파일]`의 `artifacts.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `artifacts.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `checkpoint.criteria`를 기준으로 판단한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.

Source of Truth 후보:

- `docs/backend/README.md`
- `docs/backend/architecture/**`
- `docs/backend/policies/**`
- `[입력 파일]`의 `input.design_result_file`이 가리키는 `payload.tdd_path`의 마일스톤 TDD

체크포인트 재호출 시 아래 필드가 추가된다.

```text
[체크포인트]: [입력 파일]의 `artifacts.checkpoint_file` 경로 참조.
완료된 작업은 건너뛰고 남은 작업부터 이어서 수행.
```

### 역할별 체크포인트 기준

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `IMPLEMENTATION_COMPLETED:` 또는 `FIX_APPLIED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 구현 배치가 끝나고 다른 backend 책임 영역으로 넘어간다.
- 변경 집합 또는 테스트 기대값이 서로 맞물려 보존이 필요하다.
- 위반 수정 흐름이 다른 위반 묶음으로 넘어간다.
- 컴파일/테스트 실패가 수정 방향 전환을 요구한다.
- 요구사항 또는 명시적 제외사항 경계가 불명확해진다.

---

## Output

### Case A: 신규 구현

먼저 `[출력 파일]`에 implementation artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
IMPLEMENTATION_COMPLETED: {[출력 파일] 절대 경로}
```

```yaml
schema_version: implement-backend-implementation/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-implementation-engineer
kind: implementation_result
iteration: 0
created_at: <ISO-8601 timestamp>
status: completed
payload:
  changed_files:
    - path: <절대 경로>
      summary: <1~2줄 설명>
  design_decisions:
    - <구현 중 확정한 결정>
  verification:
    compile:
      command: <실행 명령어>
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <요약>
    tests:
      command: <실행 명령어>
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <요약>
  uncertainties:
    - <있다면 기재. 없으면 "없음">
```

### Case B: 위반 수정

먼저 `[출력 파일]`에 fix artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
FIX_APPLIED: {[출력 파일] 절대 경로}
```

```yaml
schema_version: implement-backend-implementation/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-implementation-engineer
kind: fix_result
iteration: <A-B 루프 iter>
created_at: <ISO-8601 timestamp>
status: fixed | partial | failed
payload:
  changed_files:
    - path: <절대 경로>
      summary: <이번 수정으로 바뀐 내용>
  applied:
    - file: <절대 경로>
      rule: <문서명:항목>
      result: applied
  failed:
    - file: <절대 경로>
      rule: <문서명:항목>
      reason: <실패 이유>
  verification:
    compile:
      command: <실행 명령어>
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <요약>
    tests:
      command: <실행 명령어 또는 "not_run">
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <요약>
```

필드 규칙:

- `schema_version`: 항상 `implement-backend-implementation/v1`
- `role`: 항상 `backend-implementation-engineer`
- `kind`: `implementation_result` 또는 `fix_result`
- `status`: 신규 구현은 `completed`, 위반 수정은 `fixed | partial | failed`
- 모든 `path`와 `file`: 절대 경로
- `payload.failed`: 실패 항목이 없으면 빈 배열 `[]`

정상 완료 응답 본문에는 artifact 내용을 복사하지 않는다. 정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 변경·검증 결론으로 수렴할 수 있는 최소 근거를 남긴다.

### Case C: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`IMPLEMENTATION_COMPLETED`, `FIX_APPLIED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Backend Implementation Engineer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | changed_file_batch | implementation_batch_done | violation_batch_done | verification_failure | read_batch_done | requirement_boundary | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
- `## 안티패턴`
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
