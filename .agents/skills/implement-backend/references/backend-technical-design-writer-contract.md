# Backend Design Writer — Case Contract

`implement-backend` 스킬이 `backend-technical-design-writer` 서브에이전트와 주고받는 Case 기반 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/backend-technical-design-writer.toml`)이 아닌 이 문서가 design input/output/checkpoint 템플릿, 결과 신호, 체크포인트 판단 기준의 단일 출처다.

## 문서 역할

이 문서는 Backend Design Writer의 파일 기반 인터페이스만 정의한다.

- Backend Design Writer의 역할 철학은 `.codex/agents/backend-technical-design-writer.toml`이 제공한다.
- Design Writer 호출 여부와 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 결정한다.
- 이 문서는 design request Case, Markdown input/output/checkpoint 템플릿, 결과 신호, 체크포인트 기준만 소유한다.
- 메인 에이전트는 design output을 읽고 다음 implementation input으로 재구성한다.

## 공통 원칙

- 메인 에이전트는 호출 전에 Markdown `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 모두 할당한다.
- 메인 에이전트는 계약 문서의 해당 Case에서 출력 규격과 체크포인트 규격을 가져와 `[입력 파일]`에 포함한다.
- 서브에이전트는 `[입력 파일]`의 출력 규격에 따라 `[출력 파일]`과 `[체크포인트 파일]`을 저장한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.
- 정상 완료 응답 본문에는 artifact 내용을 복사하지 않는다.

## Case 1. Backend Design Request

### 목적

backend 마일스톤에 기술설계문서가 필요한지 판단하고, 필요하면 TDD를 작성하며, 불필요하면 스킵 근거를 남긴다.

### 호출 프롬프트

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-design-r00-input.v1.md
[계약 파일]: .agents/skills/implement-backend/references/backend-technical-design-writer-contract.md
[지시]: 입력 파일을 읽고 입력 파일의 출력 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

### Input Template

`[입력 파일]`은 Markdown으로 작성하며 아래 섹션을 포함한다. 이 input template은 이 계약 문서가 소유한다.

```text
# Backend Design Input
## Metadata
## 목표
## 명시적 제외사항
## 프로젝트 컨텍스트
## Source of Truth
## 설계 입력
## 출력 규격
## 체크포인트 규격
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-backend-design-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-technical-design-writer
kind: design_input
iteration: 0
created_at: <ISO-8601 timestamp>
output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-design-r00-result.v1.md
checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/design-r00-v001.md
```

### 입력 규칙

- `[명시적 제외사항]`은 설계 범위에서 제외한다.
- `[설계 입력]`에는 확정 요구사항 컨텍스트 경로를 포함할 수 있다.
- 확정 요구사항 컨텍스트가 있으면 업무 목표, 범위, 업무 규칙, 정책, 상태 변화, 정합성, 운영 요구사항, 금지된 추론, 남은 미결정 사항을 설계 경계로 사용한다.
- Design Writer는 확정 요구사항 컨텍스트에 없는 비즈니스, 운영, 실패 처리, 정합성, 재처리, 동시성 정책을 임의로 확정하지 않는다.
- 설계 판단 기준은 `[입력 파일]`의 `Source of Truth` 섹션으로 한정한다.
- `docs/backend` Source of Truth가 비어 있거나 generic 문서이거나 실제 코드와 불일치하면 설계를 임의로 보강하지 않고 `TDD_BLOCKED`로 차단 사유를 남긴다.
- `[출력 파일]`은 `[입력 파일]`의 `Metadata.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `Metadata.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `체크포인트 규격` 섹션을 기준으로 판단한다.
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
[체크포인트]: [입력 파일]의 `Metadata.checkpoint_file` 경로 참조. 이어서 작업 진행.
```

### Output Template / 출력 규격

`TDD_CREATED` 상태의 `[출력 파일]`은 [../../write-backend-tech-design-doc/references/backend-tdd-template.md](../../write-backend-tech-design-doc/references/backend-tdd-template.md)의 전체 구조와 동일한 Backend TDD 문서로 저장한다.

````markdown
# {기능명} Backend TDD

## Metadata

```yaml
schema_version: implement-backend-design/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-technical-design-writer
kind: design_result
iteration: 0
created_at: <ISO-8601 timestamp>
```

> 작성일: YYYY-MM-DD
> 상태: Draft | Reviewing | Approved | Superseded
> 대상 모듈: {대상 backend 모듈}

## 1. 설계 배경 및 목적

### 1.1 배경
{기능이 필요한 이유, 해결하려는 비즈니스 문제, 현재 시스템 제약}

### 1.2 설계 목표
1. **{목표}**: {달성 기준과 이유}

### 1.3 설계 비목표
- {이번 설계에서 제외하는 항목과 이유}

### 1.4 기술적 제약사항
- **아키텍처 제약**: {확인된 backend architecture 제약}
- **인프라 제약**: {확인된 infra 제약}
- **비기능 요구사항**: {성능, 가용성, 정합성 요구 수준}

## 2. 현행 시스템 분석

### 2.1 관련 도메인 구조
```text
{EntityA} (1) -> (N) {EntityB}  [{entityAId}로 참조]
```

### 2.2 현재 처리 흐름
```text
Controller -> UseCase -> Domain Service -> Port -> Adapter
```

### 2.3 현행 스키마 분석
| 테이블 | 주요 필드 | 현재 역할 | 변경 필요성 |
|--------|-----------|-----------|-------------|
| `{table}` | `{columns}` | {role} | {reason} |

## 3. 아키텍처 설계

### 3.1 계층별 책임 분배
| 계층 | 구성 요소 | 책임 | 설계 근거 |
|------|-----------|------|-----------|
| App | `{Component}` | {responsibility} | {reason} |
| Application | `{Component}` | {responsibility} | {reason} |
| Domain | `{Component}` | {responsibility} | {reason} |
| Storage/External | `{Component}` | {responsibility} | {reason} |

### 3.2 처리 흐름
{요청에서 응답까지의 command/query 흐름}

### 3.3 설계 대안 분석
| 대안 | 장점 | 단점 | 채택 여부 | 사유 |
|------|------|------|-----------|------|
| {alternative} | {pros} | {cons} | 채택/기각 | {reason} |

## 4. 도메인 모델 설계

### 4.1 애그리거트 경계
{aggregate 단위와 경계 결정 이유}

### 4.2 도메인 모델 상세
#### `{DomainClass}`
- 역할: {business responsibility}
- 불변식: {invariants}
- 주요 행위: {methods and meaning}
- 상태 전이: {state transition}

### 4.3 데이터 스키마 설계
```sql
-- 필요한 경우 실제 프로젝트 DDL 관리 방식에 맞춰 작성
```

### 4.4 데이터 변환 흐름
{Domain <-> Entity <-> DTO 변환 경로와 책임}

## 5. 트랜잭션 설계

### 5.1 트랜잭션 경계
| 연산 | 시작점 | 범위 | 격리 수준 | 사유 |
|------|--------|------|-----------|------|
| {operation} | {boundary} | {scope} | {isolation} | {reason} |

### 5.2 정합성 보장 전략
{강한 일관성 또는 최종 일관성 선택 이유}

### 5.3 이벤트 처리
| 이벤트 | 발행 시점 | 구독자 | 처리 방식 | 실패 대응 |
|--------|-----------|--------|-----------|-----------|
| {event} | {timing} | {handler} | {sync/async} | {recovery} |

## 6. 예외 및 실패 처리

### 6.1 예외 분류
| 예외 유형 | ErrorCode | 발생 조건 | Error Type | 사용자 메시지 |
|-----------|-----------|-----------|------------|---------------|
| {type} | `{ErrorCode}` | {condition} | {error type} | {message} |

### 6.2 실패 시나리오 및 복구 전략
| 시나리오 | 발생 가능성 | 영향 범위 | 복구 전략 |
|----------|-------------|-----------|-----------|
| {scenario} | 높음/중간/낮음 | {impact} | {recovery} |

### 6.3 멱등성 보장
{중복 요청과 재처리 부작용을 막는 방법}

## 7. 동시성 및 성능

### 7.1 동시성 제어
| 경합 지점 | 제어 방식 | 구현 방법 | 사유 |
|-----------|-----------|-----------|------|
| {resource} | {strategy} | {implementation} | {reason} |

### 7.2 성능 고려사항
| 항목 | 우려 사항 | 대응 전략 | 측정 기준 |
|------|-----------|-----------|-----------|
| {item} | {risk} | {strategy} | {metric} |

### 7.3 확장 가능성
{열어둔 확장 포인트와 의도적으로 제한한 지점}

## 8. 변경 파일 목록
| 파일 | 모듈 | 변경 유형 | 설명 |
|------|------|-----------|------|
| `{path}` | {module} | 생성/수정/삭제 | {description} |

## 9. 검증 계획
| 시나리오 | 유형 | 검증 내용 | 예상 결과 |
|----------|------|-----------|-----------|
| {scenario} | unit/integration/e2e/manual | {verification} | {expected} |

## 10. 리스크와 미결정 사항
- {risk or open question}

## 11. 완료 체크리스트
- [ ] 설계 배경과 목표가 현재 backend 구조와 요구사항에 연결된다.
- [ ] 계층별 책임, 도메인 모델, 트랜잭션 경계, 실패 처리 판단에 근거가 있다.
- [ ] 동시성, 성능, 확장 가능성의 의도적 제약과 열어둔 지점이 구분된다.
- [ ] 검증 계획이 변경 파일과 주요 시나리오를 빠짐없이 다룬다.
- [ ] 새 TDD 추가·삭제·이름 변경이 `docs/backend/design/README.md`에 반영되었다.
````

TDD가 불필요하거나 설계가 차단된 경우에는 `[출력 파일]`에 아래 fallback 결과를 저장한다.

```text
# Backend Design Result
## Metadata
## 상태
## 설계 불가 사유
## 스킵 근거
## 참조 근거
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-backend-design/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: backend-technical-design-writer
kind: design_result
iteration: 0
created_at: <ISO-8601 timestamp>
```

fallback 필드 규칙:

- `schema_version`: 항상 `implement-backend-design/v1`
- `role`: 항상 `backend-technical-design-writer`
- `kind`: 항상 `design_result`
- `iteration`: 항상 `0`
- `## 상태`: `tdd_skipped` 또는 `design_blocked`
- `## 설계 불가 사유`: `design_blocked`일 때 구현 전에 사용자 확인이 필요한 누락 정책을 포함한다. 스킵 가능한 경우 `없음`으로 쓴다.
- `## 스킵 근거`: `tdd_skipped`일 때 TDD 없이 구현 가능한 이유를 쓴다. 차단된 경우 `없음`으로 쓴다.
- `## 참조 근거`: 사용한 Source of Truth 문서 경로와 핵심 근거를 적는다.

### 정상 완료 포맷

먼저 `[출력 파일]`에 design artifact를 저장하고, `[체크포인트 파일]`에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 출력 파일 경로만 반환한다.

```text
TDD_CREATED: {[출력 파일] 절대 경로}
```

TDD가 불필요하면 같은 저장 순서를 지킨 뒤 아래 신호를 반환한다.

```text
TDD_SKIPPED: {[출력 파일] 절대 경로}
```

확정 요구사항 컨텍스트가 부족해 설계를 진행할 수 없으면 같은 저장 순서를 지킨 뒤 아래 신호를 반환한다.

```text
TDD_BLOCKED: {[출력 파일] 절대 경로}
```

`TDD_BLOCKED`는 구현으로 진행 가능한 완료가 아니다. 메인 에이전트는 출력 파일의 `설계 불가 사유`를 읽고 사용자 질문으로 되돌아간다.

정상 완료 checkpoint의 `체크포인트 사유`는 `normal_completion`으로 기록하고, 완료 snapshot에는 재호출해도 같은 설계 결론으로 수렴할 수 있는 최소 근거를 남긴다.

### Checkpoint Template / 체크포인트 규격

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `TDD_CREATED:`, `TDD_SKIPPED:`, `TDD_BLOCKED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 설계 판단 주제가 도메인, 계층, 정합성, 외부 연동 중 다른 축으로 바뀐다.
- 작성한 TDD 일부를 다음 섹션에서도 보존해야 한다.
- 근거 수집에서 설계 결론 도출로 전환한다.
- 요구사항 또는 명시적 제외사항 경계가 불명확해진다.
- 중간 설계 결정이 누적되어 완료 전 보존이 필요하다.

체크포인트가 필요한 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`TDD_CREATED`, `TDD_SKIPPED`, `TDD_BLOCKED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다. 이 checkpoint template은 이 계약 문서가 소유한다.

- `# Backend Technical Design Writer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | design_decision_batch | section_batch_done | evidence_batch_done | layer_switch | requirement_boundary | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
- `## 완료된 작업`
- `## 진행중 작업`
- `## 남은 작업`
- `## 주의사항`
- `## 실패 패턴`
- `## 최근 결정`
- `## 진행 상태`
