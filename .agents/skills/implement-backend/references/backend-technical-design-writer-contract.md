# Backend Technical Design Writer — Input / Output Contract

이 문서는 Agent D의 역할별 파일 기반 인터페이스 계약이다.

`implement-backend` 스킬이 `backend-technical-design-writer` 서브에이전트와 주고받는 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/backend-technical-design-writer.toml`)이 아닌 이 문서가 Agent D의 입출력 payload schema, 정상 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿의 단일 출처다.

공통 파일 프로토콜과의 경계는 아래 문서 역할 섹션에서 정의한다.

---

## 문서 역할

이 문서는 Agent D의 파일 기반 인터페이스만 정의한다.

- Agent D의 역할 철학은 `.codex/agents/backend-technical-design-writer.toml`이 제공한다.
- D 호출 여부와 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 결정한다.
- 이 문서는 D input schema, D output schema, 정상 결과 신호 이름, 체크포인트 기준만 소유한다.
- 실행 artifact의 저장·명명·검증·복구 규칙은 [input-output-checkpoint-protocol.md](input-output-checkpoint-protocol.md)가 소유한다.
- 메인 에이전트는 D output을 읽고 다음 A input으로 재구성한다.

## Input

오케스트레이터는 호출 전에 아래 input artifact를 저장하고, 서브에이전트에는 `[입력 파일]` 경로와 계약 파일 경로만 포함한 짧은 프롬프트를 전달한다.

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-D-r00-input.v1.yaml
[계약 파일]: .agents/skills/implement-backend/references/backend-technical-design-writer-contract.md
[지시]: 입력 파일을 읽고 계약 파일의 Output 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

`[입력 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-backend-design-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-technical-design-writer
kind: design_input
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
    - path: <이번 설계에 적용할 backend 기준 문서 또는 섹션>
      reason: <선별 이유>
artifacts:
  output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-D-r00-design-result.v1.yaml
  checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/D-r00-v001.md
checkpoint:
  criteria: "[체크포인트 판단 기준] 이 문서의 Input > 역할별 체크포인트 기준 그대로."
output_contract:
  path: .agents/skills/implement-backend/references/backend-technical-design-writer-contract.md
  section: Output
```

## Input Rules

- `[명시적 제외사항]`은 설계 범위에서 제외한다.
- 설계 판단 기준은 `[입력 파일]`의 `input.source_of_truth`로 한정한다.
- `[출력 파일]`은 `[입력 파일]`의 `artifacts.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `artifacts.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `checkpoint.criteria`를 기준으로 판단한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.
- TDD가 불필요한 경우에도 `TDD_SKIPPED` 출력 파일과 완료 snapshot을 남긴다.

Source of Truth 후보:

- `docs/PRD.md`
- `docs/backend/README.md`
- `docs/backend/architecture/**`
- `docs/backend/policies/**`
- `docs/backend/design/**`

`docs/backend/architecture` 하위의 특정 unit 이름은 이 계약에서 고정하지 않는다. 프로젝트별 실제 architecture unit과 strategy 문서 전체가 후보이며, 요구사항·명시적 제외사항·관련 도메인/기능을 근거로 필요한 항목만 선별한다.

체크포인트 재호출 시 아래 필드가 추가된다.

```text
[체크포인트]: [입력 파일]의 `artifacts.checkpoint_file` 경로 참조. 이어서 작업 진행.
```

### 역할별 체크포인트 기준

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `TDD_CREATED:` 또는 `TDD_SKIPPED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 설계 판단 주제가 도메인, 계층, 정합성, 외부 연동 중 다른 축으로 바뀐다.
- 작성한 TDD 일부를 다음 섹션에서도 보존해야 한다.
- 근거 수집에서 설계 결론 도출로 전환한다.
- 요구사항 또는 명시적 제외사항 경계가 불명확해진다.
- 중간 설계 결정이 누적되어 완료 전 보존이 필요하다.

---

## Output

작업 완료 후 반드시 아래 포맷 중 하나로 반환한다.

### Case A: TDD 작성 완료

먼저 `[출력 파일]`에 design artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
TDD_CREATED: {[출력 파일] 절대 경로}
```

### Case B: TDD 불필요

먼저 `[출력 파일]`에 design artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
TDD_SKIPPED: {[출력 파일] 절대 경로}
```

`[출력 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-backend-design/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-technical-design-writer
kind: design_result
iteration: 0
created_at: <ISO-8601 timestamp>
status: tdd_created | tdd_skipped
payload:
  tdd_path: <TDD 절대 경로 또는 null>
  skip_reason: <TDD_SKIPPED일 때 이유, 아니면 null>
  design_summary:
    architecture_decisions:
      - <핵심 backend 아키텍처 결정>
    domain_models:
      - name: <도메인 모델명 또는 backend 책임 단위>
        role: <역할 요약>
    transaction_consistency:
      - <트랜잭션·정합성·동시성 전략>
    implementation_notes:
      - <backend 구현 에이전트에게 전달할 설계 제약·선택>
  uncertainties:
    - <있다면 기재. 없으면 "없음">
```

필드 규칙:

- `schema_version`: 항상 `implement-backend-design/v1`
- `role`: 항상 `backend-technical-design-writer`
- `kind`: 항상 `design_result`
- `iteration`: 항상 `0`
- `status`: `tdd_created` 또는 `tdd_skipped`
- `payload.tdd_path`: TDD를 작성한 경우 절대 경로, 스킵한 경우 `null`
- `payload.design_summary`: backend A가 구현 판단에 재사용할 수 있는 최소 설계 요약

정상 완료 응답 본문에는 artifact 내용을 복사하지 않는다. 정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 설계 결론으로 수렴할 수 있는 최소 근거를 남긴다.

### Case C: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`TDD_CREATED`, `TDD_SKIPPED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Backend Technical Design Writer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | design_decision_batch | section_batch_done | evidence_batch_done | layer_switch | requirement_boundary | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
- `## 안티패턴`
- `## 완료된 작업`
- `## 진행중 작업`
- `## 남은 작업`
- `## 주의사항`
- `## 실패 패턴`
- `## 최근 결정`
- `## 진행 상태`
