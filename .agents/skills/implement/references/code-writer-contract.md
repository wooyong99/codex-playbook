# Code Writer — Input / Output Contract

`implement` 스킬이 `code-writer` 서브에이전트와 주고받는 인터페이스 규격.  
에이전트 파일(`code-writer.md`)이 아닌 이 문서가 입출력 포맷의 단일 출처다.

---

## Input

### Case A — 신규 구현

오케스트레이터가 아래 형식으로 프롬프트를 구성해 전달한다.

```
[마일스톤]: {마일스톤 제목}
[요구사항]:
{구체적 범위·목표}

[명시적 제외사항]:
{사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"}

[프로젝트 컨텍스트]:
  - {실제 저장소 문서에서 추출한 스택/모듈 구조}
  - {실제 저장소 문서에서 추출한 의존 방향/레이어 규칙}
  - 관련 레이어: {app/application/domain/storage 중 해당}
  - 관련 도메인: {도메인명}

[설계 결과 파일]: {D가 반환한 design_result handoff artifact 절대 경로}. 먼저 이 파일을 읽고, `payload.tdd_path`가 있으면 해당 TDD를 읽은 뒤 설계 의도에 따라 구현.

[결과 파일]: .agents/runs/{run_id}/handoffs/M{n}/{seq}-A-r00-implementation-result.v1.yaml

[체크포인트 파일]: .agents/runs/{run_id}/checkpoints/M{n}/A-r00-v001.md

[출력 규격]: 이 문서(.agents/skills/implement/references/code-writer-contract.md) — Output > Case A 그대로.
```

[설계 결과 파일]과 `[결과 파일]`은 오케스트레이터가 할당한 handoff artifact 경로다. 실제 호출 값은 절대 경로여야 한다. A는 정상 완료 시 `[결과 파일]`에 결과 payload를 먼저 저장한 뒤, 첫 줄에 결과 신호와 파일 경로만 반환한다. 임의 파일명 생성, 다른 경로 반환, 기존 결과 파일 덮어쓰기는 금지한다. 단, 같은 호출의 저장 실패 복구 재시도에서 동일 경로를 다시 쓰는 것은 허용한다.

### Case B — 위반 수정

```
[수정 작업]: 이전 작업에 대한 아키텍처 검토에서 아래 위반이 발견됐습니다.
검토 결과 파일의 `payload.violations` 각 항목의 file·line_range를 직접 읽고, rule·reason을 근거로 수정하세요.

[검토 결과 파일]: {B가 반환한 review_result handoff artifact 절대 경로}

[규칙]:
  - 위반 항목 외 코드는 변경하지 말 것.
  - 모든 수정 후 컴파일 성공 확인.

[결과 파일]: .agents/runs/{run_id}/handoffs/M{n}/{seq}-A-r{iter}-fix-result.v1.yaml

[체크포인트 파일]: .agents/runs/{run_id}/checkpoints/M{n}/A-r{iter}-v001.md

[출력 규격]: 이 문서(.agents/skills/implement/references/code-writer-contract.md) — Output > Case B 그대로.
```

A는 `[검토 결과 파일]`을 먼저 읽고, `status: violations` 인 경우에만 수정 작업을 수행한다. `status: pass` 이거나 `payload.violations`가 비어 있으면 수정하지 말고 `status: failed`, 빈 배열 payload, `verification.*.result: not_run` 으로 결과 파일에 근거를 기록한다.

체크포인트 재호출 시 Case A·Case B 프롬프트에 아래 필드가 추가된다:

```
[체크포인트]: [체크포인트 파일] 경로 참조.
완료된 작업은 건너뛰고 남은 작업부터 이어서 수행.
```

---

## Output

작업 완료 후 반드시 아래 포맷 중 하나로 반환한다. 불필요한 서술 없이 간결하게.

### Case A: 신규 구현

먼저 `[결과 파일]`에 아래 handoff artifact를 저장한다. 저장이 끝난 뒤 출력 **첫 줄**에 결과 파일 경로만 반환한다:

```text
IMPLEMENTATION_COMPLETED: {[결과 파일] 절대 경로}
```

`[결과 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-handoff/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: code-writer
kind: implementation_result
iteration: 0
created_at: <ISO-8601 timestamp>
status: completed
payload:
  changed_files:
    - path: <절대 경로 1>
      summary: <1~2줄 설명>
    - path: <절대 경로 2>
      summary: <1~2줄 설명>
  design_decisions:
    - <결정 1>
    - <결정 2>
  verification:
    compile:
      command: <실행 명령어>
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <실패 시 에러 또는 성공 요약>
    tests:
      command: <실행 명령어>
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <통과 수/총 수 또는 실패 테스트명>
  uncertainties:
    - <있다면 기재. 없으면 "없음">
```

### Case B: 위반 수정

먼저 `[결과 파일]`에 아래 handoff artifact를 저장한다. 저장이 끝난 뒤 출력 **첫 줄**에 결과 파일 경로만 반환한다:

```text
FIX_APPLIED: {[결과 파일] 절대 경로}
```

`[결과 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-handoff/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: code-writer
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
      details: <실패 시 에러 또는 성공 요약>
    tests:
      command: <실행 명령어 또는 "not_run">
      exit_code: <0 또는 비0>
      result: success | failure | not_run
      details: <이유 또는 요약>
```

`payload.failed` 가 없으면 빈 배열 `[]` 로 저장한다.

### 공통 필드 규칙

- `schema_version`: 항상 `implement-handoff/v1`
- `run_id`: 오케스트레이터가 생성한 run id
- `milestone`: `M1`, `M2` 형식
- `sequence`: 오케스트레이터가 파일명에 부여한 3자리 순번의 정수값
- `role`: 항상 `code-writer`
- `kind`: `implementation_result` 또는 `fix_result`
- `iteration`: 신규 구현은 `0`, 위반 수정은 현재 A-B 루프 iter
- `created_at`: ISO-8601 타임스탬프
- 모든 `path`와 `file`: 절대 경로

정상 완료 응답 본문에는 handoff artifact 내용을 복사하지 않는다. 오케스트레이터와 다음 에이전트는 첫 줄의 파일 경로를 통해 필요한 내용을 읽는다.

### Case C: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 **첫 줄**에 아래 신호를 출력한다:

```
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`IMPLEMENTATION_COMPLETED`, `FIX_APPLIED`)을 섞지 말고 최소 진행 상태만 작성한다.

체크포인트는 이 계약에서 **유일하게 보장되는 복구 메커니즘** 이다. 체크포인트 저장과 위 신호 반환은 반드시 수행한다.

체크포인트 파일은 아래 섹션을 포함한다:

```markdown
# Code Writer Checkpoint

## 체크포인트 사유
{changed_file_batch | implementation_batch_done | violation_batch_done | verification_failure | read_batch_done | requirement_boundary | 기타}

## 현재 목표
{이번 호출에서 달성해야 할 목표}

## 완료된 작업
{처리 완료된 파일·작업 목록}

## 진행중 작업
{현재 처리 중이던 파일·작업}

## 남은 작업
{아직 처리하지 않은 파일·작업 목록}

## 발견한 버그
{작업 중 발견한 이슈. 없으면 "없음"}

## 주의사항
{다음 작업자가 알아야 할 제약·특이사항}

## 실패 패턴
{반복된 컴파일/테스트 실패, 되돌린 접근, 실패한 수정 전략. 없으면 "없음"}

## 최근 결정
{이번 호출에서 내린 주요 설계 결정}

## 검증 상태
{아직 실행하지 못한 검증 명령과 이유}

## 관련 파일
{이번 작업과 관련된 핵심 파일 절대 경로 목록}

## 진행 상태
{읽은 파일/섹션 수, 변경 파일 수, 처리한 위반 수, 완료한 구현 배치}
```
