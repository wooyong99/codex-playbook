# Design Writer — Input / Output Contract

`implement` 스킬이 `design-writer` 서브에이전트와 주고받는 인터페이스 규격.  
에이전트 정의 파일(`.codex/agents/design-writer.toml`)이 아닌 이 문서가 입출력 포맷, 체크포인트 판단 기준, 체크포인트 파일 템플릿의 단일 출처다.

---

## Input

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

[결과 파일]: .agents/runs/{run_id}/handoffs/M{n}/{seq}-D-r00-design-result.v1.yaml

[체크포인트 파일]: .agents/runs/{run_id}/checkpoints/M{n}/D-r00-v001.md

[출력 규격]: 이 문서(.agents/skills/implement/references/design-writer-contract.md) — Output 섹션 그대로.
```

[결과 파일]은 오케스트레이터가 할당한 handoff artifact 경로다. 실제 호출 값은 절대 경로여야 한다. D는 정상 완료 시 해당 파일에 결과 payload를 먼저 저장한 뒤, 첫 줄에 결과 신호와 파일 경로만 반환한다. 임의 파일명 생성, 다른 경로 반환, 기존 결과 파일 덮어쓰기는 금지한다. 단, 같은 호출의 저장 실패 복구 재시도에서 동일 경로를 다시 쓰는 것은 허용한다.

체크포인트 재호출 시 프롬프트에 아래 필드가 추가된다:

```
[체크포인트]: [체크포인트 파일] 경로 참조. 이어서 작업 진행.
```

---

## Output

작업 완료 후 반드시 아래 포맷 중 하나로 반환한다.

### Case A: TDD 작성 완료

먼저 `[결과 파일]`에 아래 handoff artifact를 저장한다. 저장이 끝난 뒤 출력 **첫 줄**에 결과 파일 경로만 반환한다:

```
TDD_CREATED: {[결과 파일] 절대 경로}
```

### Case B: TDD 불필요

먼저 `[결과 파일]`에 아래 handoff artifact를 저장한다. 저장이 끝난 뒤 출력 **첫 줄**에 결과 파일 경로만 반환한다:

```
TDD_SKIPPED: {[결과 파일] 절대 경로}
```

### Handoff Artifact

`[결과 파일]`은 YAML로 작성한다.

```yaml
schema_version: implement-handoff/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: design-writer
kind: design_result
iteration: 0
created_at: <ISO-8601 timestamp>
status: tdd_created | tdd_skipped
payload:
  tdd_path: <TDD 절대 경로 또는 null>
  skip_reason: <TDD_SKIPPED일 때 이유, 아니면 null>
  design_summary:
    architecture_decisions:
      - <핵심 아키텍처 결정>
    domain_models:
      - name: <모델명>
        role: <역할 요약>
    transaction_consistency:
      - <트랜잭션·정합성 전략>
    implementation_notes:
      - <code-writer에게 전달할 설계 제약·선택>
  uncertainties:
    - <있다면 기재. 없으면 "없음">
```

### 필드 규칙

- `schema_version`: 항상 `implement-handoff/v1`
- `run_id`: 오케스트레이터가 생성한 run id
- `milestone`: `M1`, `M2` 형식
- `sequence`: 오케스트레이터가 파일명에 부여한 3자리 순번의 정수값
- `role`: 항상 `design-writer`
- `kind`: 항상 `design_result`
- `iteration`: 설계 단계는 항상 `0`
- `created_at`: ISO-8601 타임스탬프
- `status`: `tdd_created` 또는 `tdd_skipped`
- `payload.tdd_path`: TDD를 작성한 경우 절대 경로, 스킵한 경우 `null`
- `payload.design_summary`: A가 파일을 읽어 구현 판단에 재사용할 수 있는 최소 설계 요약

정상 완료 응답 본문에는 handoff artifact 내용을 복사하지 않는다. 오케스트레이터와 다음 에이전트는 첫 줄의 파일 경로를 통해 필요한 내용을 읽는다.

### 역할별 체크포인트 기준

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `TDD_CREATED:` 또는 `TDD_SKIPPED:`를 반환할 수 있으면 체크포인트하지 말고 정상 완료한다.

아래 항목 중 하나라도 `조건`과 `관측 신호`를 함께 만족하면 선제적으로 체크포인트한다. `관측 신호`가 애매하지만 `fallback`에 걸리면 체크포인트한다:

- 조건: 설계 판단 흐름이 한 덩어리 끝났고 다음 판단 덩어리로 넘어가야 한다.
  관측 신호: 같은 판단에서 도출된 결정들이 서로 의존하고, 다음 작업이 다른 도메인·레이어·정합성 주제로 바뀐다.
  fallback: 설계 결정 3개 이상을 정리했고 TDD 작성이 아직 끝나지 않았다.
- 조건: 작성한 TDD 일부가 다음 호출에서도 그대로 유지되어야 한다.
  관측 신호: 이미 작성한 섹션의 결정·용어·제약을 이후 섹션에서 반복 참조해야 한다.
  fallback: TDD 주요 섹션 3개 이상을 작성했고 남은 섹션이 있다.
- 조건: 근거 수집에서 설계 결론 도출로 전환해야 한다.
  관측 신호: 읽은 문서들이 같은 결론을 지지하거나 충돌 지점을 만들었고, 그 상태를 잃으면 같은 근거를 다시 읽어야 한다.
  fallback: 신규 근거 파일 또는 문서 섹션 8개 이상을 읽었고 아직 결론 전이다.
- 조건: 요구사항 경계가 흔들려서 이후 판단이 범위를 넓힐 위험이 있다.
  관측 신호: 명시적 제외사항, 사용자가 말한 범위, 저장소 규칙 사이에 충돌 또는 미해결 선택지가 생겼다.
  fallback: 요구사항 또는 명시적 제외사항을 넘어서는 설계 판단이 필요해졌고 남은 작업이 있다.
- 조건: 기억해야 할 중간 요약이 누적되어 정상 응답 전까지 안정적으로 들고 가기 어렵다.
  관측 신호: 최근 결정, 실패 패턴, 주의사항을 다음 섹션에서 모두 참조해야 한다.
  fallback: 아직 결론 전인데 중간 요약을 두 번 이상 누적해야 한다.

### Case C: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 **첫 줄**에 아래 신호를 출력한다:

```
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`TDD_CREATED`, `TDD_SKIPPED`)을 섞지 말고 최소 진행 상태만 작성한다.

체크포인트는 이 계약에서 **유일하게 보장되는 복구 메커니즘** 이다. 체크포인트 저장과 위 신호 반환은 반드시 수행한다.

체크포인트 파일은 아래 섹션을 포함한다:

```markdown
# Design Writer Checkpoint

## 체크포인트 사유
{design_decision_batch | section_batch_done | evidence_batch_done | layer_switch | requirement_boundary | 기타}

## 현재 목표
{이번 호출에서 작성해야 할 TDD의 목표}

## 핵심 규칙
{반드시 지켜야 할 규칙: 계약 문서의 출력 신호·파일 경로·스키마 준수, 설계 결정과 근거 보존, 명시적 제외사항 준수}

## 금지 규칙
{절대 하면 안 되는 행동: 임의 결과/체크포인트 경로 생성, 정상 완료 신호와 체크포인트 신호 혼합, 근거 없이 확정한 설계 결정 변경}

## 안티패턴
{자주 실수하는 나쁜 사례: 결정 근거 없이 요약만 남김, 남은 섹션을 모호하게 작성, 스킵 판단 근거 부족. 없으면 "없음"}

## 완료된 작업
{작성 완료된 섹션 목록}

## 진행중 작업
{현재 작성 중이던 섹션}

## 남은 작업
{아직 작성하지 않은 섹션 목록}

## 주의사항
{다음 작업자가 알아야 할 제약·특이사항}

## 실패 패턴
{반복된 설계 혼선, 미해결 리스크, 다음 호출에서 피해야 할 접근. 없으면 "없음"}

## 최근 결정
{이번 호출에서 내린 주요 설계 결정}

## 진행 상태
{읽은 근거 섹션 수, 작성한 주요 섹션 수, 누적 설계 결정 수}
```
