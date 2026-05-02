---
name: implement
description: 요구사항을 마일스톤 단위로 분해하여 설계 문서 작성(D) → 코드 작성(A) → 아키텍처 검토(B) → 수정 루프를 오케스트레이션하는 스킬. 기능 구현, 리팩토링, UseCase 추가, 도메인 모델 변경 등 코드 작업이 필요한 모든 상황에서 사용한다. "구현해줘", "만들어줘", "추가해줘", "리팩토링", "implement", "/implement" 같은 요청에 이 스킬을 사용한다.
---

# implement — 코드 작성 및 검토 오케스트레이션

사용자의 구현/리팩토링 요구사항을 **마일스톤 단위로 분해**하고, 각 마일스톤에 대해 **기술설계 서브에이전트(D)**, **코드 작성 서브에이전트(A)**, **아키텍처 검토 서브에이전트(B)** 를 오케스트레이션한다.

---

## 당신(메인 에이전트)의 역할 — 오케스트레이터

| 주체 | 책임 |
|------|------|
| **당신 (메인 에이전트)** | 요구사항 분석, 마일스톤 분할, D·A·B 위임, 반복 종료 판단, 사용자 보고 |
| **Agent D** (`subagent_type="design-writer"`) | 마일스톤별 기술설계문서(TDD) 작성. `write-tech-design-doc` 스킬 사용 |
| **Agent A** (`subagent_type="code-writer"`) | Kotlin 코드 작성·수정, 테스트, 빌드 확인 |
| **Agent B** (`subagent_type="architecture-reviewer"`) | `docs/backend/architecture/*`·`docs/backend/policies/*` 준수 검토만. Read/Glob/Grep 중심, 수정 권한 없음 |

**에이전트 계약 문서** (입출력·체크포인트 규격의 단일 출처):
- D: [`references/design-writer-contract.md`](references/design-writer-contract.md)
- A: [`references/code-writer-contract.md`](references/code-writer-contract.md)
- B: [`references/architecture-reviewer-contract.md`](references/architecture-reviewer-contract.md)

handoff artifact 경로, 체크포인트 경로, 프롬프트 필드 이름, 출력 신호 포맷, 파일 스키마, 체크포인트 판단 기준, 체크포인트 파일 템플릿은 위 계약 문서가 단일 출처다. 이 문서에는 흐름과 의사결정만 유지하고, 문자열 예시는 가능한 한 계약 문서를 링크로 대체한다.

**서브에이전트 정의 파일**:
- [design-writer.toml](/Users/jeong-uyong/work/codex-playbook/.codex/agents/design-writer.toml)
- [code-writer.toml](/Users/jeong-uyong/work/codex-playbook/.codex/agents/code-writer.toml)
- [architecture-reviewer.toml](/Users/jeong-uyong/work/codex-playbook/.codex/agents/architecture-reviewer.toml)

각 `.toml` 파일은 대응 계약 문서를 참조하고 역할·실행 제약만 가진다. 인터페이스 규격이나 체크포인트 파일 템플릿을 `.toml`에 복제하지 않는다.

### 절대 지켜야 할 제약

1. **당신은 파일을 직접 Read/Edit/Write 하지 않는다.** 코드 작업은 전부 A에게, 설계 문서는 D에게 위임.
   - 예외: 사용자 요구사항 이해에 필요한 경우 `docs/backend/README.md` 같은 **맵 문서 하나 정도** Read는 허용.
   - 예외: 정상 산출물 전달 및 체크포인트 복구를 위해 계약 문서에 정의된 `[결과 파일]` 과 `[체크포인트 파일]` 을 Read하고 존재 여부·스키마를 검증하는 것은 허용한다.
2. **당신은 검토를 직접 수행하지 않는다.** 검토는 전부 B에게 위임.
3. **D·A·B는 서로 호출하지 않는다.** 모든 통신은 당신을 경유.
4. **B 호출은 매번 새 인스턴스**로 수행 (fresh context).
5. **D 호출은 매번 새 인스턴스**로 수행 (fresh context). **A 호출은 마일스톤 첫 호출만 새 인스턴스**로 수행. 같은 마일스톤 내 재호출(위반 수정, 체크포인트 재개)은 동일 인스턴스를 이어서 사용한다.

### 엔터프라이즈급 작업 원칙

- `B`의 `review_result.status: pass`는 **문서 준수 통과(doc-compliance pass)** 를 의미한다. 기능 정확성·성능·운영 안정성까지 자동 보증하는 뜻으로 해석하지 않는다.
- 마일스톤은 가능한 한 **도메인 경계·배포 경계·검토 경계** 가 일치하도록 자른다. 아래 `마일스톤 분할 기준`을 초과하면 더 분할한다.
- D/A/B 프롬프트의 `[프로젝트 컨텍스트]`는 현재 저장소의 실제 문서 맵에서 추출한 내용을 채운다. 계약 문서의 예시 문구를 하드코딩된 사실처럼 복사하지 않는다.
- 정상 산출물 전달의 표준 메커니즘은 **handoff artifact 파일 + 결과 신호** 다. 메인은 큰 payload를 프롬프트에 복사하지 않고 파일 경로를 다음 에이전트에게 전달한다.
- 체크포인트 복구의 표준 메커니즘은 **체크포인트 파일 + `CONTEXT_CHECKPOINT:` 신호** 다.
- A의 성공 응답은 사람이 읽기 좋기만 한 요약이 아니라, 메인과 B가 안정적으로 재사용할 수 있는 **구조화된 handoff artifact** 여야 한다.

### 마일스톤 분할 기준

목표는 "한 서브에이전트 호출이 컨텍스트를 꽉 채우기 전에 끝나는 단위"로 나누는 것이다. 아래 기준은 추정치여도 적용한다. 메인은 코드베이스 세부 범위를 직접 설계하지 않고, 마일스톤 목표와 명시적 제외사항만 전달한다.

**마일스톤 기본 단위**:
- 사용자 관점의 독립된 결과 1개
- 주 도메인 1개, 보조 도메인 최대 1개
- 주요 트랜잭션 경계 1개
- API/UseCase/Flow 최대 3개
- 예상 변경 파일 3~8개 권장, 10개 초과 시 분할 우선
- 모듈 최대 2개 권장, 3개 초과 시 분할 우선
- 검증 명령 묶음 1개로 성공/실패 판단 가능

**무조건 분할을 검토하는 조건**:
- 독립 비즈니스 결과가 2개 이상이다.
- 도메인 3개 이상 또는 모듈 4개 이상을 동시에 건드린다.
- 예상 변경 파일이 12개를 넘는다.
- DB 마이그레이션이 2개 이상이거나 서로 다른 Aggregate의 스키마를 바꾼다.
- 인증/권한, 외부 연동, 비동기 이벤트/outbox, 배치/스케줄러 변경이 핵심 기능 변경과 섞여 있다.
- 한 번의 B 검토 대상이 10개 파일을 넘는다.

분할이 어렵다면 하나의 "큰 마일스톤"으로 강행하지 말고, `M{n}-a`, `M{n}-b` 같은 하위 마일스톤으로 쪼갠다. 원자성이 필요한 경우에만 큰 마일스톤을 허용한다.

역할별 체크포인트 판단 기준은 D/A/B 계약 문서가 단일 출처로 가진다. 메인은 체크포인트 파일 경로를 전달하고, `CONTEXT_CHECKPOINT:` 응답을 복구 절차로 처리하는 책임만 가진다.

역할별 체크포인트 판단은 하이브리드 방식으로 작성한다. 주 판단은 현재 작업의 흐름, 전환점, 기억해야 할 결정의 밀도 같은 상대적 신호를 본다. 절대 수치는 판단 흔들림을 막기 위한 안전선으로만 사용한다. 계약 문서는 각 조건을 `조건`, `관측 신호`, `fallback`으로 쪼개어 기록해야 한다.

### Handoff artifact 공통 처리

정상 완료 결과는 응답 본문에 길게 싣지 않는다. D/A/B는 오케스트레이터가 미리 할당한 `[결과 파일]`에 YAML payload를 저장하고, 첫 줄에 결과 신호와 파일 경로만 반환한다.

저장 위치와 파일명은 아래 전략을 따른다.

```text
.agents/runs/{run_id}/
├── handoffs/
│   └── M{n}/
│       ├── 001-D-r00-design-result.v1.yaml
│       ├── 002-A-r00-implementation-result.v1.yaml
│       ├── 003-B-r01-review-result.v1.yaml
│       ├── 004-A-r01-fix-result.v1.yaml
│       └── 005-B-r02-review-result.v1.yaml
└── checkpoints/
    └── M{n}/
        ├── D-r00-v001.md
        ├── A-r00-v001.md
        └── B-r01-v001.md
```

파일명 규칙:
- `{seq}`: run 안의 마일스톤별 append-only 3자리 순번. 메인이 할당하며 서브에이전트가 임의 생성하지 않는다.
- `{role}`: `D`, `A`, `B`
- `r{iter}`: 설계와 최초 구현은 `r00`, 첫 검토는 `r01`, 이후 A-B 루프마다 증가
- `{kind}`: `design-result`, `implementation-result`, `review-result`, `fix-result`
- `v1`: handoff artifact 스키마 버전. 파일 내용의 `schema_version`은 `implement-handoff/v1`로 고정한다.
- 정책 재확인이나 재호출로 정상 결과를 다시 받아야 하면 새 `{seq}`를 할당한다. 같은 파일 경로 재사용은 동일 호출의 저장 실패 복구에만 허용한다.

메인의 처리 절차:
1. 서브에이전트 호출 전에 `[결과 파일]` 절대 경로와 `[체크포인트 파일]` 절대 경로를 할당한다.
2. 정상 결과 신호의 경로가 이번 호출에서 전달한 `[결과 파일]`과 일치하는지 확인한다.
3. 해당 파일이 존재하고 비어 있지 않은지 확인한다.
4. `schema_version`, `run_id`, `milestone`, `role`, `kind`, `status`, `payload` 같은 핵심 필드를 검증한다.
5. 다음 에이전트에게는 필요한 payload 원문을 복사하지 않고, 선행 에이전트가 만든 handoff artifact 경로만 전달한다.
6. 사용자 업데이트와 루프 종료 판단에 필요한 최소 필드만 메인이 읽는다.

### 체크포인트 공통 처리

서브에이전트 응답 첫 줄이 `CONTEXT_CHECKPOINT:` 인 경우, 이를 성공·완료 응답으로 파싱하지 않는다. 아래 절차로만 처리한다.

1. 첫 줄의 경로가 현재 호출에서 전달한 `[체크포인트 파일]` 경로와 일치하는지 확인한다.
2. 해당 파일이 존재하고 비어 있지 않은지 확인한다.
3. 계약 문서의 체크포인트 파일 스키마에 있는 제목과 핵심 섹션이 포함됐는지 확인한다.
4. 위 검증이 실패하면 같은 서브에이전트에게 한 번만 재호출하여 체크포인트 파일 저장부터 다시 수행하게 한다. 두 번째도 실패하면 자동 루프를 멈추고 사용자에게 체크포인트 프로토콜 실패를 보고한다.
5. 검증이 통과하면 체크포인트 파일을 Read한 뒤, 계약 문서의 체크포인트 재호출 규격으로 같은 서브에이전트를 재호출한다.

이 체크포인트 규약이나 서브에이전트 정의를 수정한 뒤에는 `python3 .agents/skills/implement/scripts/validate-context-checkpoints.py` 로 계약 문서와 에이전트 정의의 필수 항목을 검증한다.

---

## Phase 0: 요구사항 분석

1. 사용자 입력을 한 문장으로 재진술하여 이해 확인.
2. 애매하거나 중요한 정보가 누락되면 **사용자에게 확인 질문 후 대기**. 임의 추정하지 않음.
3. 이해가 선명하면 Phase 1로.

## Phase 1: 마일스톤 분할

분할 기준:
- 독립적으로 검토 가능한가 (B가 한 번에 의미 있는 검토 가능)
- 독립적으로 커밋 가능한가
- `마일스톤 분할 기준` 안에 들어오는가
- A의 컨텍스트가 감당 가능한가 (예상 변경 파일 3~8개 권장, 10개 초과 시 분할 우선)

규모별 기준:
- 단일 CRUD / 단일 UseCase 추가 → **1 마일스톤**
- 여러 도메인 걸친 기능 → **2~4 마일스톤**
- 대규모 리팩토링 / 신규 서브시스템 → **5+ 마일스톤** (사용자에게 사전 확인)

각 마일스톤에는 아래 메타데이터를 붙인다:
- `목표`: 사용자 관점 결과 1개
- `범위`: 포함할 도메인·레이어·모듈
- `명시적 제외사항`: 사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음"
- `예상 변경 파일 수`: 3~8개 권장
- `검증 기준`: 실행할 컴파일/테스트 명령

메인은 각 서브에이전트의 세부 탐색·수정·검토 범위를 대신 설계하지 않는다. D/A는 요구사항과 프로젝트 컨텍스트를 바탕으로 필요한 범위를 스스로 좁히고, B는 A가 반환한 변경 파일 목록만 검토 대상으로 삼는다.

각 마일스톤을 `TaskCreate`로 등록하고, 사용자에게 분할 결과 출력:

```
📋 마일스톤 계획
  M1/{total}: <제목>
  M2/{total}: <제목>
  ...
```

규모가 크면 (5개 이상 마일스톤) 사용자에게 진행 여부 확인.

진행이 확정되면 아래 명령으로 `run_id`를 생성·보관한다:
```bash
run_id=$(date +%Y%m%d-%H%M%S)-$RANDOM && mkdir -p ".agents/runs/$run_id/handoffs" ".agents/runs/$run_id/checkpoints"
```
이 값은 Phase 2 전체에서 에이전트 프롬프트의 `[결과 파일]`과 `[체크포인트 파일]` 경로를 구성하는 데 사용된다.

---

## Phase 2: 마일스톤별 순차 실행

각 마일스톤에 대해 아래 루프를 수행한다. `iter`는 해당 마일스톤의 A↔B 반복 횟수.

### Step 2-1. 시작 알림

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 [M{n}/{total}] {마일스톤 제목} — 시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

해당 task를 `TaskUpdate`로 `in_progress`로 전환.

### Step 2-2. Agent D 위임 (기술설계 문서 작성)

```
📝 기술설계 문서 작성 중... (Agent D)
```

`Agent` 도구 호출:
- `subagent_type`: `design-writer`
- `description`: `[M{n}] 기술설계 문서 작성`
- `prompt`: [`references/design-writer-contract.md`](references/design-writer-contract.md) 의 Input 섹션 형식으로 구성한다. 현재 마일스톤의 제목·요구사항·명시적 제외사항·실제 저장소 기준 `[프로젝트 컨텍스트]`·관련 레이어·도메인, `[결과 파일]`, `[체크포인트 파일]`을 채운다.

D의 응답을 받으면:

**응답 첫 줄이 `CONTEXT_CHECKPOINT:` 신호인 경우:**
```
⚡ [M{n}] 컨텍스트 체크포인트 저장됨 — D 재호출 중...
```
`체크포인트 공통 처리` 절차로 파일을 검증한 뒤, [`references/design-writer-contract.md`](references/design-writer-contract.md) 의 체크포인트 재호출 규격대로 D를 재호출한다.

**응답 첫 줄이 `TDD_CREATED:` 인 경우:**
```
✅ TDD 작성 완료 · {tdd-path}
```
`Handoff artifact 공통 처리` 절차로 D 결과 파일을 검증한 뒤 읽는다. `payload.tdd_path`와 D 결과 파일 경로를 변수로 보관한다. A에게는 설계 요약 원문을 복사하지 않고 D 결과 파일 경로를 전달한다.

**응답 첫 줄이 `TDD_SKIPPED:` 인 경우:**
```
⏭️  TDD 스킵 · {reason}
```
`Handoff artifact 공통 처리` 절차로 D 결과 파일을 검증한 뒤 읽는다. `payload.skip_reason`과 D 결과 파일 경로를 변수로 보관한다.

단, 아래 조건 중 하나라도 만족하면 `TDD_SKIPPED` 를 그대로 수용하지 말고 D를 **한 번 더 재호출**해 스킵 근거를 재확인한다.
- 마일스톤이 2개 이상 레이어에 걸친다
- 새로운 도메인 개념, 이벤트, 예외 전략, 트랜잭션 경계, 동시성 제어가 포함된다
- 사용자가 "복잡한 변경", "대규모 리팩토링", "엔터프라이즈급" 같은 표현으로 설계 리스크를 명시했다

이 재호출은 정상 결과 재생성이므로 새 `[결과 파일]` 순번을 할당한다. 재호출 후에도 D가 `TDD_SKIPPED` 를 유지하면 그 이유를 사용자 업데이트에 짧게 노출한 뒤 Step 2-3으로 진행한다.

→ Step 2-3으로.

### Step 2-3. Agent A 위임 (코드 작성)

```
🔨 코드 작성 위임 중... (Agent A)
```

`Agent` 도구 호출:
- `subagent_type`: `code-writer`
- `description`: `[M{n}] 코드 작성`
- `prompt`: [`references/code-writer-contract.md`](references/code-writer-contract.md) 의 Input > Case A 형식으로 구성한다. 현재 마일스톤의 제목·요구사항·명시적 제외사항·실제 저장소 기준 `[프로젝트 컨텍스트]`·관련 레이어·도메인, D가 반환한 `[설계 결과 파일]`, A의 `[결과 파일]`, `[체크포인트 파일]`을 채운다.

A의 응답을 받으면:

**응답 첫 줄이 `CONTEXT_CHECKPOINT:` 신호인 경우:**
```
⚡ [M{n}] 컨텍스트 체크포인트 저장됨 — 재호출 중...
```
`체크포인트 공통 처리` 절차로 파일을 검증한 뒤, [`references/code-writer-contract.md`](references/code-writer-contract.md) 의 체크포인트 재호출 규격대로 A를 재호출한다.
재호출 후 응답을 받을 때까지 이 처리를 반복한다.

**응답 첫 줄이 `IMPLEMENTATION_COMPLETED:` 인 경우:**
```
✅ 코드 작성 완료 · 변경 파일 {N}개
```

`Handoff artifact 공통 처리` 절차로 A 결과 파일을 검증한 뒤 `payload.changed_files`, `payload.design_decisions`, `payload.verification` 을 읽는다.
- A 결과 파일 경로를 변수로 보관 (B에게 전달해야 함)
- `changed_files` 는 사용자 업데이트와 최종 요약에 필요한 범위에서만 메인이 읽음
- `verification.compile.exit_code`, `verification.tests.exit_code` 가 누락됐거나 실패면 마일스톤을 성공으로 간주하지 않고 A 재호출 또는 사용자 보고

### Step 2-4. Agent B 위임 (아키텍처 검토)

```
🔍 아키텍처 규칙 검토 중... (Agent B, 시도 {iter}/5)
```

`Agent` 도구 호출:
- `subagent_type`: `architecture-reviewer`
- `description`: `[M{n}] 규칙 검토`
- `prompt`: [`references/architecture-reviewer-contract.md`](references/architecture-reviewer-contract.md) 의 Input 섹션 형식으로 구성한다. A가 반환한 `[구현 결과 파일]`, D가 반환한 `[설계 결과 파일]`, B의 `[결과 파일]`, `[체크포인트 파일]`을 채운다.

B의 응답을 받으면 아래 포맷으로 즉시 콘솔에 출력:

```
📋 검토 결과 (시도 {iter}/5):
  상태: ✅ pass  또는  ⚠️ 위반 {K}건
  {위반이 있을 경우 각 항목을 한 줄씩 — 파일명 + 위반 규칙 요약}
```

B의 응답 처리:
- **응답 첫 줄이 `CONTEXT_CHECKPOINT:` 신호인 경우**: `체크포인트 공통 처리` 절차로 파일을 검증한 뒤 [`references/architecture-reviewer-contract.md`](references/architecture-reviewer-contract.md) 의 체크포인트 재호출 규격대로 B를 재호출한다. 완료된 파일의 위반 결과는 체크포인트 파일의 `완료된 결과` 섹션에서 복원한다.
- **응답 첫 줄이 `REVIEW_COMPLETED:` 인 경우**: `Handoff artifact 공통 처리` 절차로 B 결과 파일을 검증한 뒤 `status`와 `payload.violations`를 읽는다.
- `status: pass`면 → Step 2-7으로 (마일스톤 완료)
- `status: violations`면 → Step 2-5로

### Step 2-5. 위반 수정 위임 (A 재호출)

```
⚠️  위반 {K}건 발견 — 수정 적용 중... (Agent A, 시도 {iter}/5)
```

`iter`를 1 증가. **iter > 5이면 Step 2-8 (escalation)로**.

`Agent` 도구 호출:
- `subagent_type`: `code-writer`
- `description`: `[M{n}] 위반 수정`
- `prompt`: [`references/code-writer-contract.md`](references/code-writer-contract.md) 의 Input > Case B 형식으로 구성한다. B가 반환한 `[검토 결과 파일]`, A의 `[결과 파일]`, `[체크포인트 파일]`을 채운다. 위반 항목 원문은 프롬프트에 복사하지 않는다. 마일스톤 내 A 인스턴스를 이어 사용한다.

**응답 첫 줄이 `CONTEXT_CHECKPOINT:` 신호인 경우:**
```
⚡ [M{n}] 수정 작업 체크포인트 저장됨 — A 재호출 중...
```
`체크포인트 공통 처리` 절차로 파일을 검증한 뒤, [`references/code-writer-contract.md`](references/code-writer-contract.md) 의 체크포인트 재호출 규격대로 A를 재호출한다.
재호출 후 `FIX_APPLIED` 또는 다시 `CONTEXT_CHECKPOINT:` 응답을 받을 때까지 이 처리를 반복한다.

A의 응답을 받으면:
```
✅ 수정 완료 · 적용 {S}건 · 실패 {F}건
```

응답 첫 줄이 `FIX_APPLIED:` 인지 확인하고, `Handoff artifact 공통 처리` 절차로 A 수정 결과 파일을 검증한 뒤 `payload.changed_files`, `payload.applied`, `payload.failed`, `payload.verification` 을 읽는다. 새로 수정된 파일이 있으면 마일스톤의 변경 파일 집합에 합친다.
- `verification.compile.exit_code` 가 누락됐거나 실패면 재검토로 진행하지 않고 A 재호출 또는 사용자 보고
- `verification.tests` 가 누락됐으면 재검토로 진행하지 않고 A 재호출
- `verification.tests.result` 가 `failure` 면 재검토로 진행하지 않고 A 재호출 또는 사용자 보고
- `verification.tests.result` 가 `not_run` 이면 이유를 사용자에게 노출하고, 팀 정책상 허용되는 빠른 수정인지 확인된 경우에만 재검토로 진행

실패가 있으면 상세를 사용자에게 노출. → Step 2-6 (재검토).

### Step 2-6. 재검토 (Step 2-4 반복)

```
🔍 재검토 중... (Agent B, 시도 {iter}/5)
```

Step 2-4와 동일한 B 위임. B의 응답을 받으면 Step 2-4와 동일한 포맷으로 콘솔에 출력한 뒤 처리:
- `status: pass` → Step 2-7
- `status: violations` → Step 2-5로 돌아가서 반복

### Step 2-7. 마일스톤 완료

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 [M{n}/{total}] {제목} 완료 ({iter} 라운드)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

해당 task를 `TaskUpdate`로 `completed`로 전환. 다음 마일스톤으로.

### Step 2-8. Escalation (5회 초과 시)

```
⛔ [M{n}] 자동 수렴 실패 — A↔B 루프 5회 초과

마지막 검토 결과 요약:
{B의 마지막 응답 요약 3~5줄}

선택지:
  1. 현재 상태로 커밋하고 수동 검토
  2. 메인 에이전트가 직접 개입하여 수정
  3. 요구사항을 재정의하고 해당 마일스톤 재시작
  4. 해당 마일스톤을 스킵하고 다음으로 진행
  5. 전체 중단
```

**사용자 선택 대기**. 사용자 응답에 따라 처리:
- 1, 2, 3, 4, 5 각각에 맞는 후속 흐름 실행.
- 2번 선택 시에만 메인 에이전트가 직접 Edit (이 경우에 한해 예외적으로 허용).
- 2번 선택 시 **Manual Recovery Mode** 로 전환:
  - 현재 마일스톤의 마지막 A 결과 파일, 마지막 B 결과 파일, 체크포인트 파일을 모두 읽고 충돌 여부를 먼저 정리
  - 수정 범위와 성공 기준을 3줄 이내로 다시 고정
  - 직접 수정 후 반드시 빌드/테스트를 다시 실행하고, 결과 명령어와 종료 코드를 사용자에게 그대로 보고
  - 가능하면 새 B 인스턴스로 최종 문서 준수 재검토를 한 번 더 수행

---

## Phase 3: 전체 완료 보고

모든 마일스톤이 완료되면 최종 요약:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ 구현 완료

마일스톤: {완료}/{총}
총 A↔B 라운드: {합계}
마일스톤별 라운드: M1={r1}, M2={r2}, ...

변경 파일 총 {N}개. 다음 단계 제안:
  1. `smart-commit` 스킬로 마일스톤 단위 커밋 그룹핑
  2. 또는 바로 커밋 작성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 요약 — 한 번에 보기

```
[Phase 0] 요구 분석 → 불명확하면 사용자 확인
[Phase 1] 마일스톤 분할 → TaskCreate
[Phase 2] 각 M마다:
    D 위임(설계) →
      TDD_CREATED → A 위임(구현, TDD 참조) → B 위임(검토)
      TDD_SKIPPED → A 위임(구현)            → B 위임(검토)
        review_result.status=pass       → 다음 M
        review_result.status=violations → A 위임(수정) → B 재검토 → ... (max 5 iter)
        5회↑ → 사용자 escalate
[Phase 3] 완료 보고 → 커밋 제안
```
