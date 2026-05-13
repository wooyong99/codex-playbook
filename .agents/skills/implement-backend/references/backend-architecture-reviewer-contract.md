# Backend Architecture Reviewer — Input / Output Contract

`implement-backend` 스킬이 `backend-architecture-reviewer` 서브에이전트와 주고받는 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/backend-architecture-reviewer.toml`)이 아닌 이 문서가 입출력 포맷, 체크포인트 판단 기준, 체크포인트 파일 템플릿의 단일 출처다.

---

## 문서 역할

이 문서는 Agent B의 파일 기반 인터페이스만 정의한다.

- Agent B의 역할 철학은 `.codex/agents/backend-architecture-reviewer.toml`이 제공한다.
- B 호출과 재검토 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 결정한다.
- 이 문서는 B input schema, B output schema, 결과 신호, 체크포인트 기준만 소유한다.
- 메인 에이전트는 A output과 D output을 읽고 B input으로 재구성한다.

## Input

오케스트레이터는 호출 전에 아래 input artifact를 저장하고, 서브에이전트에는 `[입력 파일]` 경로와 계약 파일 경로만 포함한 짧은 프롬프트를 전달한다.

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-B-r{iter}-input.v1.yaml
[계약 파일]: .agents/skills/implement-backend/references/backend-architecture-reviewer-contract.md
[지시]: 입력 파일을 읽고 계약 파일의 Output 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

`[입력 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-backend-review-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-architecture-reviewer
kind: review_input
iteration: <A-B 루프 iter>
created_at: <ISO-8601 timestamp>
input:
  milestone_title: <마일스톤 제목>
  implementation_result_file: <A가 반환한 implementation_result 또는 fix_result output artifact 절대 경로>
  design_result_file: <D가 반환한 design_result output artifact 절대 경로 또는 null>
  source_of_truth:
    - path: <이번 검토에 적용할 backend 기준 문서 또는 섹션>
      reason: <선별 이유>
artifacts:
  output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-B-r{iter}-review-result.v1.yaml
  checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/B-r{iter}-v001.md
checkpoint:
  criteria: "[체크포인트 판단 기준] 이 문서의 Input > 역할별 체크포인트 기준 그대로."
output_contract:
  path: .agents/skills/implement-backend/references/backend-architecture-reviewer-contract.md
  section: Output
```

## Input Rules

- `[입력 파일]`의 `input.implementation_result_file`이 가리키는 `payload.changed_files`만 검토 대상으로 삼는다.
- `payload.design_decisions`, `[입력 파일]`의 `input.design_result_file`, `payload.tdd_path`는 입력된 경우에만 보조 컨텍스트로 사용한다.
- 검토 기준은 `[입력 파일]`의 `input.source_of_truth`로 한정한다.
- 입력되지 않은 문서 경로, 숨은 팀 관행, 개인적 선호, 설계 대안은 violation 근거로 삼지 않는다.
- `[출력 파일]`은 `[입력 파일]`의 `artifacts.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `artifacts.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `checkpoint.criteria`를 기준으로 판단한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.

Source of Truth 후보:

- `docs/backend/README.md`
- `docs/backend/architecture/**`
- `docs/backend/policies/**`
- `[입력 파일]`의 `input.design_result_file`이 가리키는 `payload.tdd_path`의 마일스톤 TDD

`docs/backend/architecture` 하위의 특정 unit 이름은 이 계약에서 고정하지 않는다. 프로젝트별 실제 architecture unit과 strategy 문서 전체가 후보이며, 변경 파일 경로·A 결과 요약·D 결과의 설계 결정을 근거로 필요한 항목만 선별한다.

체크포인트 재호출 시 아래 필드가 추가된다.

```text
[체크포인트]: [입력 파일]의 `artifacts.checkpoint_file` 경로 참조.
완료된 파일은 건너뛰고 남은 파일부터 이어서 검토.
```

### 역할별 체크포인트 기준

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `REVIEW_COMPLETED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 검토 파일군 또는 규칙 관점이 바뀐다.
- 위반 근거가 누적되어 보존이 필요하다.
- 규칙 문서 탐색에서 파일 검토로 전환한다.
- 검토 대상 경계가 불명확해진다.
- 완료된 파일별 pass 또는 violation 결과를 다음 검토에서 다시 참조해야 한다.

---

## Output

### Case A: 검토 완료

먼저 `[출력 파일]`에 review artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
REVIEW_COMPLETED: {[출력 파일] 절대 경로}
```

`[출력 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-backend-review/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-architecture-reviewer
kind: review_result
iteration: <A-B 루프 iter>
created_at: <ISO-8601 timestamp>
status: pass | violations
payload:
  reviewed_files:
    - <검토한 파일 절대 경로>
  violations:
    - rule_id: <규칙 ID. 없으면 UNREGISTERED>
      severity: blocker | major | minor | info
      file: <절대 경로>
      rule: <문서명>:<규칙 또는 체크리스트 항목>
      source_path: <규칙 원문 문서의 저장소 상대 경로>
      line_range: <start-end>
      reason: <1줄 근거 + 참조 문서 경로>
  referenced_artifacts:
    code_result: <input.implementation_result_file 절대 경로>
    design_result: <input.design_result_file 절대 경로 또는 null>
    tdd_path: <TDD 절대 경로 또는 null>
```

필드 규칙:

- `schema_version`: 항상 `implement-backend-review/v1`
- `role`: 항상 `backend-architecture-reviewer`
- `kind`: 항상 `review_result`
- `status`: 위반이 없으면 `pass`, 1건 이상 있으면 `violations`
- `payload.reviewed_files`: 실제 검토한 파일의 절대 경로 목록
- `payload.violations`: 위반이 없으면 빈 배열 `[]`
- `payload.violations[].rule_id`: [Rule ID and metadata](../../../../docs/rules/README.md) 형식을 따른다. 아직 등록되지 않은 규칙은 `UNREGISTERED`로 둔다.
- `payload.violations[].severity`: `blocker`, `major`, `minor`, `info` 중 하나
- `payload.violations[].file`: 절대 경로
- `payload.violations[].source_path`: 규칙 원문 문서의 저장소 상대 경로

정상 완료 응답 본문에는 output artifact 내용을 복사하지 않는다. 정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 검토 결론으로 수렴할 수 있는 최소 근거를 남긴다.

### Case B: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`REVIEW_COMPLETED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Backend Architecture Reviewer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | review_file_batch | layer_batch_done | violation_batch_done | rule_read_batch_done | requirement_boundary | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
- `## 안티패턴`
- `## 완료된 작업`
- `## 진행중 작업`
- `## 남은 작업`
- `## 발견한 버그`: 아키텍처 규칙 위반만 보고한다.
- `## 주의사항`
- `## 실패 패턴`
- `## 최근 결정`
- `## 완료된 결과`: 검토 완료 파일별 `pass` 또는 violation 항목
- `## 관련 파일`
- `## 진행 상태`: 읽은 규칙/파일 섹션 수, 검토 완료 파일 수, 확정 위반 수

## Output Guard

- 정상 완료는 `REVIEW_COMPLETED:`만 출력한다.
- 체크포인트는 `CONTEXT_CHECKPOINT:`만 출력한다.
- 기능 정확성·버그 관련 지적을 포함하지 않는다.
- Source of Truth에 없는 기준이나 선호 기반 제안을 포함하지 않는다.
