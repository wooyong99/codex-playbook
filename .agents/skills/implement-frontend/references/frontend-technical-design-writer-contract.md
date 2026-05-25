# Frontend Design Writer — Case Contract

`implement-frontend` 스킬이 `frontend-technical-design-writer` 서브에이전트와 주고받는 Case 기반 인터페이스 규격.
에이전트 정의 파일(`.codex/agents/frontend-technical-design-writer.toml`)이 아닌 이 문서가 design input/output/checkpoint 템플릿, 결과 신호, 체크포인트 판단 기준의 단일 출처다.

## 문서 역할

이 문서는 Frontend Design Writer의 파일 기반 인터페이스만 정의한다.

- Frontend Design Writer의 역할 철학은 `.codex/agents/frontend-technical-design-writer.toml`이 제공한다.
- Design Writer 호출 여부와 호출 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 결정한다.
- 이 문서는 design request Case, Markdown input/output/checkpoint 템플릿, 결과 신호, 체크포인트 기준만 소유한다.
- 메인 에이전트는 design output을 읽고 다음 implementation input으로 재구성한다.

## 공통 원칙

- 메인 에이전트는 호출 전에 Markdown `[입력 파일]`, `[출력 파일]`, `[체크포인트 파일]` 경로를 모두 할당한다.
- 메인 에이전트는 계약 문서의 해당 Case에서 출력 규격과 체크포인트 규격을 가져와 `[입력 파일]`에 포함한다.
- 서브에이전트는 `[입력 파일]`의 출력 규격에 따라 `[출력 파일]`과 `[체크포인트 파일]`을 저장한다.
- 정상 완료 전에도 `[체크포인트 파일]`을 반드시 저장한다.
- 정상 완료 응답 본문에는 artifact 내용을 복사하지 않는다.

## Case 1. Frontend Design Request

### 목적

frontend 마일스톤에 기술설계문서가 필요한지 판단하고, 필요하면 TDD를 작성하며, 불필요하면 스킵 근거를 남긴다.
확정 frontend 요구사항 컨텍스트가 부족해 설계가 불가능하면 설계 불가 사유를 남기고 구현으로 진행하지 않게 한다.

### 호출 프롬프트

```text
[입력 파일]: .agents/runs/{run_id}/inputs/M{n}/{seq}-design-r00-input.v1.md
[계약 파일]: .agents/skills/implement-frontend/references/frontend-technical-design-writer-contract.md
[지시]: 입력 파일을 읽고 입력 파일의 출력 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

### Input Template

`[입력 파일]`은 Markdown으로 작성하며 아래 섹션을 포함한다. 이 input template은 이 계약 문서가 소유한다.

```text
# Frontend Design Input
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
schema_version: implement-frontend-design-input/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-technical-design-writer
kind: design_input
iteration: 0
created_at: <ISO-8601 timestamp>
output_file: .agents/runs/{run_id}/outputs/M{n}/{seq}-design-r00-result.v1.md
checkpoint_file: .agents/runs/{run_id}/checkpoints/M{n}/design-r00-v001.md
```

### 입력 규칙

- `[명시적 제외사항]`은 설계 범위에서 제외한다.
- `[설계 입력]`에는 확정 요구사항 컨텍스트 경로를 포함할 수 있다.
- 확정 요구사항 컨텍스트가 있으면 `요구사항 결정`, `사용자 확인 필요 없음`, `금지된 추론`, `backend 계약/미확정 사항`, `검증 기준`, `남은 미결정 사항`을 설계 경계로 사용한다.
- Design Writer는 확정 요구사항 컨텍스트에 없는 제품 UX, navigation flow, API shape, cache freshness, invalidation, optimistic update, destructive action, form validation 정책을 임의로 확정하지 않는다.
- 설계 판단 기준은 `[입력 파일]`의 `Source of Truth` 섹션으로 한정한다.
- `docs/frontend` Source of Truth가 비어 있거나 generic 문서이거나 실제 코드와 불일치하면 설계를 임의로 보강하지 않고 `TDD_BLOCKED`로 차단 사유를 남긴다.
- `[출력 파일]`은 `[입력 파일]`의 `Metadata.output_file` 값을 그대로 사용한다.
- `[체크포인트 파일]`은 `[입력 파일]`의 `Metadata.checkpoint_file` 값을 그대로 사용한다.
- 체크포인트 여부는 `[입력 파일]`의 `체크포인트 규격` 섹션을 기준으로 판단한다.
- TDD가 불필요한 경우에도 `TDD_SKIPPED` 출력 파일과 완료 snapshot을 남긴다.

Source of Truth 후보:

- `docs/PRD.md`
- `docs/frontend/README.md`
- `docs/frontend/architecture/**`
- `docs/frontend/conventions/**`
- `docs/frontend/performance/**`
- `docs/frontend/ui-ux/**`
- `docs/frontend/design/**`

체크포인트 재호출 시 아래 필드가 추가된다.

```text
[체크포인트]: [입력 파일]의 `Metadata.checkpoint_file` 경로 참조. 이어서 작업 진행.
```

### Output Template / 출력 규격

`TDD_CREATED` 상태의 `[출력 파일]`은 [../../write-frontend-tech-design-doc/references/frontend-tdd-template.md](../../write-frontend-tech-design-doc/references/frontend-tdd-template.md)의 전체 구조와 동일한 Frontend TDD 문서로 저장한다.

````markdown
# {기능명} Frontend TDD

## Metadata

```yaml
schema_version: implement-frontend-design/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-technical-design-writer
kind: design_result
iteration: 0
created_at: <ISO-8601 timestamp>
```

> 작성일: YYYY-MM-DD
> 상태: Draft | Reviewing | Approved | Superseded
> 대상 영역: {route/page/feature/widget/shared}

## 1. 설계 배경 및 목표

### 1.1 배경
{사용자 문제, 제품 맥락, 현재 frontend 구조의 제약}

### 1.2 목표
- {목표와 달성 기준}

### 1.3 비목표
- {이번 범위에서 제외하는 항목}

## 2. 사용자 흐름과 라우팅

### 2.1 진입점
- route: `{route}`
- page/layout: `{page 또는 layout}`

### 2.2 화면 흐름
{사용자 행동 순서와 화면 전환}

### 2.3 라우팅 결정
- 신규 route: {route}
- 기존 route 변경: {change}
- guard/redirect: {policy}
- URL state: {query/path state}

## 3. 폴더 구조

```text
{관련 frontend 폴더 구조}
```

### 3.1 신규 파일
| 파일 | 역할 |
|------|------|
| `{path}` | {role} |

### 3.2 변경 파일
| 파일 | 변경 이유 |
|------|-----------|
| `{path}` | {reason} |

## 4. 컴포넌트 구조

### 4.1 컴포넌트 트리
```text
{Page}
`-- {Widget}
    `-- {FeatureComponent}
```

### 4.2 책임 분리
| 컴포넌트 | 책임 | props/state |
|----------|------|-------------|
| `{Component}` | {responsibility} | {contract} |

### 4.3 재사용과 public API
{외부 import 경계, index export, shared/ui 사용 기준}

## 5. 상태관리 구조

### 5.1 상태 분류
| 상태 | 종류 | 소유 위치 | 이유 |
|------|------|-----------|------|
| `{state}` | server/client/form/url/derived | `{owner}` | {reason} |

### 5.2 상태 흐름
{상태 생성, 갱신, 초기화, 동기화 흐름}

### 5.3 폼과 검증
{form library, validation schema, submit lifecycle}

## 6. API 연동 방식

### 6.1 API 계약
| API | 요청 | 응답 | 사용 위치 |
|-----|------|------|-----------|
| `{method path}` | `{request}` | `{response}` | `{usage}` |

### 6.2 Client/Hook 설계
{API client, query/mutation hook, type 위치}

### 6.3 로딩/빈 상태
{loading, skeleton, empty, disabled 상태}

## 7. 캐싱 전략

### 7.1 Query Key
| 데이터 | query key | invalidation 조건 |
|--------|-----------|-------------------|
| `{data}` | `{key}` | `{condition}` |

### 7.2 Cache Lifetime
{staleTime, gc/cacheTime, prefetch, optimistic update 여부}

### 7.3 동기화
{mutation 후 갱신, background refresh, pagination/infinite query}

## 8. 에러 처리

### 8.1 에러 분류
| 에러 | 처리 방식 | 사용자 피드백 |
|------|-----------|---------------|
| validation | {handling} | {feedback} |
| network/server | {handling} | {feedback} |
| permission | {handling} | {feedback} |

### 8.2 복구 전략
{retry, rollback, fallback UI, error boundary}

## 9. 성능과 UX 고려사항

- 렌더링 최적화: {decision}
- 리스트/페이지네이션: {decision}
- 접근성: {decision}
- 모바일/반응형: {decision}

## 10. 검증 계획

| 시나리오 | 검증 방식 | 기대 결과 |
|----------|-----------|-----------|
| {scenario} | unit/integration/e2e/browser/manual | {expected} |

## 11. 리스크와 미결정 사항
- {risk or open question}

## 12. 완료 체크리스트
- [ ] 사용자 흐름, 라우팅, 폴더 구조가 실제 frontend architecture 문서와 충돌하지 않는다.
- [ ] 컴포넌트 책임, 상태 소유권, API client/hook, cache invalidation이 서로 연결된다.
- [ ] loading, empty, error, permission, recovery UI 상태가 필요한 수준으로 정의되어 있다.
- [ ] 성능, 접근성, 반응형 기준이 구현 범위와 검증 계획에 반영되어 있다.
- [ ] 새 TDD 추가·삭제·이름 변경이 `docs/frontend/design/README.md`에 반영되었다.
````

TDD가 불필요하거나 설계가 차단된 경우에는 `[출력 파일]`에 아래 fallback 결과를 저장한다.

```text
# Frontend Design Result
## Metadata
## 상태
## 설계 불가 사유
## 스킵 근거
## 참조 근거
```

`## Metadata` 섹션은 아래 값을 포함한다.

```yaml
schema_version: implement-frontend-design/v1
run_id: <run_id>
milestone: M<n>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: frontend-technical-design-writer
kind: design_result
iteration: 0
created_at: <ISO-8601 timestamp>
```

fallback 필드 규칙:

- `schema_version`: 항상 `implement-frontend-design/v1`
- `role`: 항상 `frontend-technical-design-writer`
- `kind`: 항상 `design_result`
- `iteration`: 항상 `0`
- `## 상태`: `tdd_skipped` 또는 `design_blocked`
- `## 설계 불가 사유`: `design_blocked`일 때 구현 전에 사용자 확인이 필요한 누락 UX/API/state/cache/navigation 정책을 포함한다. 스킵 가능한 경우 `없음`으로 쓴다.
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

### 체크포인트 규격

체크포인트 판단은 상대 기준을 먼저 적용하고, 절대 수치는 안전장치로만 사용한다. 남은 작업이 없고 곧 `TDD_CREATED:`, `TDD_SKIPPED:`, `TDD_BLOCKED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 설계 판단 주제가 state, API, component, routing, cache 중 다른 축으로 바뀐다.
- 작성한 TDD 일부를 다음 섹션에서도 보존해야 한다.
- 근거 수집에서 설계 결론 도출로 전환한다.
- 요구사항 또는 명시적 제외사항 경계가 불명확해진다.
- 중간 설계 결정이 누적되어 완료 전 보존이 필요하다.

체크포인트가 필요한 경우, 먼저 `[체크포인트 파일]` 경로에 체크포인트 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

이후에는 정상 완료 포맷(`TDD_CREATED`, `TDD_SKIPPED`, `TDD_BLOCKED`)을 섞지 말고 최소 진행 상태만 작성한다. 체크포인트는 이 계약에서 유일하게 보장되는 복구 메커니즘이다. 정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 `[체크포인트 파일]`에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Frontend Technical Design Writer Checkpoint`
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
