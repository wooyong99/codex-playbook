# Architecture Reviewer — Input / Output Contract

`implement` 스킬이 `architecture-reviewer` 서브에이전트와 주고받는 인터페이스 규격.  
에이전트 파일(`architecture-reviewer.md`)이 아닌 이 문서가 입출력 포맷의 단일 출처다.

---

## Input

오케스트레이터가 아래 형식으로 프롬프트를 구성해 전달한다.

```
[마일스톤]: {마일스톤 제목}

[구현 결과 파일]: {A가 반환한 implementation_result 또는 fix_result handoff artifact 절대 경로}

[설계 결과 파일]: {D가 반환한 design_result handoff artifact 절대 경로. 없으면 생략}

[결과 파일]: .agents/runs/{run_id}/handoffs/M{n}/{seq}-B-r{iter}-review-result.v1.yaml

[체크포인트 파일]: .agents/runs/{run_id}/checkpoints/M{n}/B-r{iter}-v001.md

[출력 규격]: 이 문서(.agents/skills/implement/references/architecture-reviewer-contract.md) — Output 섹션 그대로.
```

B는 `[구현 결과 파일]`을 먼저 읽고 `payload.changed_files`를 검토 대상 파일로 삼는다. `payload.design_decisions`가 있으면 추가 컨텍스트로만 사용한다. `[설계 결과 파일]`이 전달되고 그 안의 `payload.tdd_path`가 `null`이 아니면, 검토 범위는 `docs/backend/architecture/*`, `docs/backend/policies/*` 뿐 아니라 **해당 마일스톤 TDD의 명시 결정 사항 준수 여부** 까지 포함한다. 단, TDD에 없는 개인적 선호나 대안 제안은 여전히 금지한다.

[결과 파일]은 오케스트레이터가 할당한 handoff artifact 경로다. 실제 호출 값은 절대 경로여야 한다. B는 정상 완료 시 해당 파일에 검토 결과 payload를 먼저 저장한 뒤, 첫 줄에 결과 신호와 파일 경로만 반환한다. 임의 파일명 생성, 다른 경로 반환, 기존 결과 파일 덮어쓰기는 금지한다. 단, 같은 호출의 저장 실패 복구 재시도에서 동일 경로를 다시 쓰는 것은 허용한다.

체크포인트 재호출 시 아래 필드가 추가된다:

```
[체크포인트]: [체크포인트 파일] 경로 참조.
완료된 파일은 건너뛰고 남은 파일부터 이어서 검토.
```

---

## Output

### Case A: 검토 완료

먼저 `[결과 파일]`에 아래 handoff artifact를 저장한다. 저장이 끝난 뒤 출력 **첫 줄**에 결과 파일 경로만 반환한다:

```
REVIEW_COMPLETED: {[결과 파일] 절대 경로}
```

### Handoff Artifact

`[결과 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-handoff/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: architecture-reviewer
kind: review_result
iteration: <A-B 루프 iter>
created_at: <ISO-8601 timestamp>
status: pass | violations
payload:
  reviewed_files:
    - <검토한 파일 절대 경로>
  violations:
    - file: <절대 경로>
      rule: <문서명>:<규칙 또는 체크리스트 항목>
      line_range: <start-end>
      reason: <1줄 근거 + 참조 문서 경로>
  referenced_artifacts:
    code_result: <[구현 결과 파일] 절대 경로>
    design_result: <[설계 결과 파일] 절대 경로 또는 null>
    tdd_path: <TDD 절대 경로 또는 null>
```

### 필드 규칙

- `schema_version`: 항상 `implement-handoff/v1`
- `run_id`: 오케스트레이터가 생성한 run id
- `milestone`: `M1`, `M2` 형식
- `sequence`: 오케스트레이터가 파일명에 부여한 3자리 순번의 정수값
- `role`: 항상 `architecture-reviewer`
- `kind`: 항상 `review_result`
- `iteration`: 현재 A-B 루프 iter
- `created_at`: ISO-8601 타임스탬프
- `status`: 위반이 없으면 `pass`, 1건 이상 있으면 `violations`
- `payload.reviewed_files`: 실제 검토한 파일의 절대 경로 목록
- `payload.violations`: 위반이 없으면 빈 배열 `[]`
- `payload.violations[].file`: 절대 경로 (상대 경로 금지)
- `payload.referenced_artifacts.code_result`: 이번 검토 입력으로 사용한 `[구현 결과 파일]` 절대 경로
- `rule`: 형식 `<문서명>:<항목>`
  - 예: `app-layer-guidelines.md:Controller 체크리스트 "@Valid가 Request DTO에 적용됐는가"`
  - 예: `logging.md:LogExtension 확장 함수 사용 규정`
- `line_range`: 시작-끝 라인 (예: `45-52`)
- `reason`: 1줄 근거 + 참조 문서 경로 (예: `reason: Request DTO에 toCommand() 로직 포함. app-layer-guidelines.md Coding Rules 2번.`)

정상 완료 응답 본문에는 handoff artifact 내용을 복사하지 않는다. 오케스트레이터와 다음 에이전트는 첫 줄의 파일 경로를 통해 필요한 내용을 읽는다.

### Case B: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 **첫 줄**에 아래 신호를 출력한다:

```
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`REVIEW_COMPLETED`)을 섞지 말고 최소 진행 상태만 작성한다. 검토 완료된 파일의 pass/위반 항목에 해당하는 중간 결과는 응답 본문이 아니라 체크포인트 파일의 `완료된 결과` 섹션에 저장한다.

체크포인트는 이 계약에서 **유일하게 보장되는 복구 메커니즘** 이다. 체크포인트 저장과 위 신호 반환은 반드시 수행한다.

체크포인트 파일은 아래 섹션을 포함한다:

```markdown
# Architecture Reviewer Checkpoint

## 체크포인트 사유
{review_file_batch | layer_batch_done | violation_batch_done | rule_read_batch_done | requirement_boundary | 기타}

## 현재 목표
{이번 호출에서 검토해야 할 파일 목록 및 목표}

## 완료된 작업
{검토 완료된 파일 목록}

## 진행중 작업
{현재 검토 중이던 파일}

## 남은 작업
{아직 검토하지 않은 파일 목록}

## 발견한 버그
{없음 - 아키텍처 규칙 위반만 보고}

## 주의사항
{검토 중 발견한 특이사항}

## 실패 패턴
{반복 위반 유형, 모호했던 규칙 적용, 다음 검토에서 재확인할 패턴. 없으면 "없음"}

## 최근 결정
{검토 기준 적용 시 내린 주요 판단}

## 완료된 결과
{검토 완료된 파일별 pass 또는 위반 항목 원문}

## 관련 파일
{검토 대상 파일 절대 경로 목록}

## 진행 상태
{읽은 규칙/파일 섹션 수, 검토 완료 파일 수, 확정 위반 수, 완료한 레이어}
```

### 절대 출력하지 말 것

- 인사말·결론 문구 (예: "아래는 위반 목록입니다", "검토 완료")
- Markdown 헤더·본문
- 정상 완료 시 handoff artifact 내용 원문
- REVIEW_COMPLETED, CONTEXT_CHECKPOINT 외의 어떤 텍스트. 단, 컨텍스트 체크포인트에서 `CONTEXT_CHECKPOINT:` 첫 줄 뒤에 붙는 최소 진행 상태는 예외다.

---

## 출력 예시

### 예시 1 — 위반 없음

```
REVIEW_COMPLETED: /path/to/.agents/runs/20260501-120000-12345/handoffs/M1/003-B-r01-review-result.v1.yaml
```

결과 파일:

```yaml
schema_version: implement-handoff/v1
run_id: 20260501-120000-12345
milestone: M1
sequence: 3
role: architecture-reviewer
kind: review_result
iteration: 1
created_at: 2026-05-01T12:00:00+09:00
status: pass
payload:
  reviewed_files:
    - /path/to/backend/app/backoffice/src/main/kotlin/com/example/backoffice/product/ProductController.kt
  violations: []
  referenced_artifacts:
    code_result: /path/to/.agents/runs/20260501-120000-12345/handoffs/M1/002-A-r00-implementation-result.v1.yaml
    design_result: /path/to/.agents/runs/20260501-120000-12345/handoffs/M1/001-D-r00-design-result.v1.yaml
    tdd_path: /path/to/docs/backend/design/tdd-product.md
```

### 예시 2 — 위반 2건

```
REVIEW_COMPLETED: /path/to/.agents/runs/20260501-120000-12345/handoffs/M1/003-B-r01-review-result.v1.yaml
```

결과 파일의 `payload.violations`:

```yaml
- file: /path/to/backend/app/backoffice/src/main/kotlin/com/example/backoffice/product/ProductController.kt
  rule: app-layer-guidelines.md:Controller 체크리스트 "@Valid가 Request DTO에 적용됐는가"
  line_range: 52-56
  reason: Request DTO에 @Valid 누락. docs/backend/architecture/app/app-layer-guidelines.md Post-Work Verification - Controller 섹션.
- file: /path/to/backend/core/application/src/main/kotlin/com/example/application/product/CreateProductUseCase.kt
  rule: logging.md:LogExtension 확장 함수 사용 규정
  line_range: 14-15
  reason: raw LoggerFactory 사용 + [SCOPE] 태그 누락. docs/backend/policies/logging.md Kotlin 사용 예시 및 안티 패턴.
```

---

## Self-check (출력 전 확인)

- [ ] 모든 지적이 **문서에 명시된 규칙**에 근거하는가? (추측·선호 배제)
- [ ] 출력이 `REVIEW_COMPLETED:` 또는 컨텍스트 체크포인트의 `CONTEXT_CHECKPOINT:` 포맷 외의 텍스트를 포함하지 않는가?
- [ ] 기능 정확성·버그 관련 지적을 포함하지 않았는가?
- [ ] 설계 대안·선호 기반 제안을 포함하지 않았는가?
