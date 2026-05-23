# Frontend Architecture Reviewer — Case Contract

`implement-frontend` 스킬이 `frontend-architecture-reviewer` 서브에이전트와 주고받는 Case 기반 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/frontend-architecture-reviewer.toml`)이 아닌 이 문서가 검토 입력 Markdown 섹션, 출력 Markdown 섹션, 결과 신호, 체크포인트 판단 기준, 체크포인트 파일 템플릿의 단일 출처다.

## 문서 역할

이 문서는 Frontend Architecture Reviewer의 파일 기반 인터페이스만 정의한다.

- Frontend Architecture Reviewer의 역할 철학은 `.codex/agents/frontend-architecture-reviewer.toml`이 제공한다.
- Architecture Reviewer 호출과 재검토 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 결정한다.
- 이 문서는 architecture review Case, Markdown input/output 섹션, 결과 신호, 체크포인트 기준만 소유한다.
- 메인 에이전트는 implementation output과 design output을 읽고 review input으로 재구성한다.

## 공통 원칙

- 메인 에이전트는 호출 전에 Markdown `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 모두 할당한다.
- 메인 에이전트는 계약 문서의 해당 Case에서 출력 규격과 체크포인트 규격을 가져와 `[입력 파일]`에 포함한다.
- 서브에이전트는 `[입력 파일]`의 출력 규격에 따라 `[출력 파일]`과 `[체크포인트 파일]`을 저장한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.
- 정상 완료 응답 본문에는 artifact 내용을 복사하지 않는다.

## Case 1. Architecture Review

### 목적

Implementation Engineer가 변경한 frontend 파일이 입력된 Source of Truth와 TDD 결정에 맞는지 검토한다.

### 호출 프롬프트

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-architecture-review-r{iter}-input.v1.md
[계약 파일]: .agents/skills/implement-frontend/references/frontend-architecture-reviewer-contract.md
[지시]: 입력 파일을 읽고 입력 파일의 출력 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

### 입력 파일 섹션

`[입력 파일]`은 Markdown으로 작성하며 아래 섹션을 포함한다.

```text
# Frontend Architecture Review Input
## Metadata
## 목표
## 검토 대상
## Source of Truth
## 선행 산출물
## 검토 지시
## 출력 규격
## 체크포인트 규격
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-review-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-architecture-reviewer
kind: review_input
iteration: <implementation-review 루프 iter>
created_at: <ISO-8601 timestamp>
output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-architecture-review-r{iter}-result.v1.md
checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/architecture-review-r{iter}-v001.md
```

### 입력 규칙

- `[입력 파일]`의 `검토 대상` 섹션에 있는 변경 파일만 검토 대상으로 삼는다.
- implementation output의 변경 요약, design output, TDD 경로는 입력된 경우에만 보조 컨텍스트로 사용한다.
- `[검토 지시]`에는 확정 요구사항 컨텍스트 경로를 포함할 수 있다.
- 확정 요구사항 컨텍스트가 있으면 `요구사항 결정`, `사용자 확인 필요 없음`, `금지된 추론`, `backend 계약/미확정 사항`, `검증 기준`, `남은 미결정 사항`을 검토 경계로 사용한다.
- 검토 기준은 `[입력 파일]`의 `Source of Truth` 섹션으로 한정한다.
- 입력되지 않은 문서 경로, 숨은 팀 관행, 개인적 선호, 설계 대안, 미확정 제품 UX/API/cache/navigation 정책은 violation 근거로 삼지 않는다.
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
완료된 파일은 건너뛰고 남은 파일부터 이어서 검토.
```

### 출력 규격

Architecture Reviewer는 검토 완료 후 `[출력 파일]`에 아래 Markdown 섹션을 저장한다.

```text
# Frontend Architecture Review Result
## Metadata
## 판정
## 검토 대상
## 위반 사항
## 참조 산출물
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-review/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-architecture-reviewer
kind: review_result
iteration: <implementation-review 루프 iter>
created_at: <ISO-8601 timestamp>
```

필드 규칙:

- `schema_version`: 항상 `implement-frontend-review/v1`
- `role`: 항상 `frontend-architecture-reviewer`
- `kind`: 항상 `review_result`
- `## 판정`: 위반이 없으면 `pass`, 1건 이상 있으면 `violations`
- `## 검토 대상`: 실제 검토한 파일의 절대 경로 목록
- `## 위반 사항`: 위반이 없으면 `없음`
- 위반 항목은 `rule_id`, `severity`, `file`, `rule`, `source_path`, `line_range`, `reason`을 포함한다.
- `rule_id`: [Rule ID and metadata](../../../../docs/rules/README.md) 형식을 따른다. 아직 등록되지 않은 규칙은 `UNREGISTERED`로 둔다.
- `severity`: `blocker`, `major`, `minor`, `info` 중 하나
- `file`: 절대 경로
- `source_path`: 규칙 원문 문서의 저장소 상대 경로

### 정상 완료 포맷

먼저 `[출력 파일]`에 review artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
REVIEW_COMPLETED: {[출력 파일] 절대 경로}
```

정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 검토 결론으로 수렴할 수 있는 최소 근거를 남긴다.

### 체크포인트 규격

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `REVIEW_COMPLETED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 검토 파일군 또는 규칙 관점이 바뀐다.
- 위반 근거가 누적되어 보존이 필요하다.
- 규칙 문서 탐색에서 파일 검토로 전환한다.
- 검토 대상 경계가 불명확해진다.
- 완료된 파일별 pass 또는 violation 결과를 다음 검토에서 다시 참조해야 한다.

체크포인트가 필요한 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`REVIEW_COMPLETED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Frontend Architecture Reviewer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | review_file_batch | layer_batch_done | violation_batch_done | rule_read_batch_done | requirement_boundary | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
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
