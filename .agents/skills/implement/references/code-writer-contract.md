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

[기술설계문서]: {TDD 절대 경로 — design-writer가 TDD_SKIPPED를 반환한 경우 이 항목 생략}. 코드 작성 전 반드시 읽고 설계 의도에 따라 구현.

[체크포인트 파일]: .agents/checkpoints/{run_id}/code-writer-M{n}.md

[출력 규격]: 이 문서(.agents/skills/implement/references/code-writer-contract.md) — Output > Case A 그대로.
```

### Case B — 위반 수정

```
[수정 작업]: 이전 작업에 대한 아키텍처 검토에서 아래 위반이 발견됐습니다.
각 위반 항목의 file·line_range를 직접 읽고, rule·reason을 근거로 수정하세요.

{B가 반환한 위반 YAML 원문}

[규칙]:
  - 위반 항목 외 코드는 변경하지 말 것.
  - 모든 수정 후 컴파일 성공 확인.

[체크포인트 파일]: .agents/checkpoints/{run_id}/code-writer-M{n}.md

[출력 규격]: 이 문서(.agents/skills/implement/references/code-writer-contract.md) — Output > Case B 그대로.
```

체크포인트 재호출 시 Case A·Case B 프롬프트에 아래 필드가 추가된다:

```
[체크포인트]: [체크포인트 파일] 경로 참조.
완료된 작업은 건너뛰고 남은 작업부터 이어서 수행.
```

---

## Output

작업 완료 후 반드시 아래 포맷 중 하나로 반환한다. 불필요한 서술 없이 간결하게.

### Case A: 신규 구현

````text
IMPLEMENTATION_COMPLETED
```yaml
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
````

설명 문장은 추가하지 않는다. 메인 오케스트레이터가 이 YAML을 그대로 파싱해 다음 단계 입력으로 재사용한다.

### Case B: 위반 수정

````text
FIX_APPLIED
```yaml
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
````

`failed` 가 없으면 빈 배열 `[]` 로 반환한다.

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
