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

[프로젝트 컨텍스트]:
  - {실제 저장소 문서에서 추출한 스택/모듈 구조}
  - {실제 저장소 문서에서 추출한 의존 방향/레이어 규칙}
  - 관련 레이어: {app/application/domain/storage 중 해당}
  - 관련 도메인: {도메인명}

[기술설계문서]: {TDD 절대 경로 — design-writer가 TDD_SKIPPED를 반환한 경우 이 항목 생략}. 코드 작성 전 반드시 읽고 설계 의도에 따라 구현.

[체크포인트 파일]: .agents/checkpoints/code-writer-{run_id}-M{n}.md

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

[체크포인트 파일]: .agents/checkpoints/code-writer-{run_id}-M{n}.md

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

컨텍스트 윈도우가 65% 이상 소모된 경우, 출력 **첫 줄**에 아래 신호를 출력한 뒤 완료된 작업에 대한 정상 출력 포맷을 이어서 작성한다:

```
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

체크포인트는 이 계약에서 **유일하게 보장되는 복구 메커니즘** 이다. `compact` 또는 `/compact` 명령은 런타임이 실제 제공될 때만 선택적으로 사용할 수 있으며, 사용하지 못한 경우에도 체크포인트 저장과 위 신호 반환은 반드시 수행한다.
