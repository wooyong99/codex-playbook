# Agent Architecture

## 목적

이 문서는 codex-playbook의 스킬과 서브에이전트가 무엇이고, 서로 어떤 관계를 가지며, 어떤 구조로 설계되어 있는지 설명한다.

스킬과 서브에이전트는 같은 수준의 구성 요소가 아니다. 스킬은 재사용 가능한 작업 규칙이고, 서브에이전트는 특정 역할과 판단 책임을 가진 실행 주체다. 이 둘을 분리해 두면 대형 코드베이스에서도 작업 흐름, 판단 기준, 검증 근거를 일관되게 유지할 수 있다.

## 적용 범위

이 문서는 이 저장소가 직접 소유하는 구성 요소만 다룬다.

- 프로젝트 스킬: `.agents/skills/**/SKILL.md`
- 서브에이전트 정의: `.codex/agents/*.toml`
- 평가 suite: `.agents/evals`
- 검증 스크립트: `.agents/scripts`

시스템 제공 스킬, 외부 플러그인 스킬, 모델 런타임 자체의 동작 방식은 이 문서의 범위가 아니다.

## 핵심 개념

### Skill

스킬은 특정 작업을 수행할 때 적용하는 재사용 가능한 규칙 묶음이다.

스킬은 다음을 소유한다.

- 언제 이 규칙을 적용해야 하는지
- 어떤 순서로 사고하고 작업해야 하는지
- 어떤 Source of Truth를 읽어야 하는지
- 어떤 검증 기준을 만족해야 하는지
- 반복 가능한 검증 스크립트나 템플릿이 있다면 어디에 있는지

스킬은 실행 주체가 아니다. 스킬 자체가 다른 스킬이나 서브에이전트를 호출하지 않는다. 스킬은 호출자가 읽고 적용하는 작업 규약이다.

Stage skill은 특정 서브에이전트 이름이나 역할 인스턴스에 의존하지 않는다. 서로 다른 stage 사이의 연결은 실행 주체가 아니라 입력/출력 payload로 표현한다. Backend stage payload의 단일 출처는 [backend-stage-payload-contracts](.agents/skills/backend-stage-payload-contracts.md), frontend stage payload의 단일 출처는 [frontend-stage-payload-contracts](.agents/skills/frontend-stage-payload-contracts.md)다.

### Subagent

서브에이전트는 특정 역할과 판단 책임을 가진 실행 주체다.

서브에이전트는 다음을 소유한다.

- 역할 정체성
- 판단 철학
- 판단 렌즈
- 작업 경계
- 엄격한 제약
- 기본으로 활성화할 rule skill

서브에이전트는 자기 역할 안에서 스킬을 적용한다. 예를 들어 backend delivery engineer는 backend 기술 설계, 코드 구현, 아키텍처 리뷰 규칙을 단계별로 직접 적용한다.

서브에이전트는 다른 서브에이전트를 직접 호출할 수 있다고 가정하지 않는다. 하위 호출이 필요하면 `dispatch_requests`처럼 호출자에게 요청을 반환하고, 실제 호출은 상위 호출자가 수행한다.

### Orchestration

오케스트레이션은 여러 서브에이전트의 작업 순서와 병렬 가능성을 판단하고 결과를 통합하는 작업이다.

이 저장소에서는 [feature-delivery-orchestration-rules](.agents/skills/feature-delivery-orchestration-rules/SKILL.md)가 feature delivery 오케스트레이션 규칙을 소유한다. 그러나 이 스킬도 실행 주체는 아니다. 실제로 product planning, API contract, backend/frontend delivery subagent를 호출하는 주체는 이 스킬을 적용하는 상위 호출자다.

이 구조는 subagent가 subagent를 호출할 수 없는 runtime에서도 일관된 fullstack delivery 흐름을 유지하기 위한 설계다.

### Source of Truth

문서와 코드가 판단 근거다.

- 제품 요구와 프로젝트 맥락: [AGENTS.md](AGENTS.md), [PRD](docs/PRD.md)
- backend 기준: [docs/backend](docs/backend/README.md)
- frontend 기준: [docs/frontend](docs/frontend/README.md)
- rule id와 violation metadata: [docs/rules](docs/rules/README.md)
- 평가 기준: [.agents/evals](.agents/evals/README.md)

스킬과 서브에이전트는 Source of Truth를 대체하지 않는다. 이들은 Source of Truth를 어떻게 읽고 적용할지 정하는 작업 체계다.

## 전체 구조

```text
.
├── AGENTS.md
├── AGENT_ARCHITECTURE.md
├── .agents/
│   ├── skills/      # reusable rule skills
│   ├── scripts/     # repository and agent workflow validation
│   └── evals/       # agent workflow evaluation suite
├── .codex/
│   └── agents/      # role-based subagent definitions
└── docs/            # project Source of Truth
```

구성 요소의 책임은 아래처럼 나뉜다.

| 구성 요소 | 본질 | 책임 | 책임이 아닌 것 |
|-----------|------|------|----------------|
| `docs/**` | Source of Truth | 프로젝트 목표, 정책, 아키텍처, 컨벤션 | 실행 주체 |
| `.agents/skills/**` | 작업 규칙 | 사고 순서, 판단 기준, 템플릿, 검증 규칙 | 독립 실행 주체 |
| `.codex/agents/*.toml` | 역할 주체 | 특정 역할의 판단과 작업 수행 | 다른 subagent 직접 호출 가정 |
| `.agents/scripts/**` | 자동 검증 | 링크, 구조, workflow contract, eval coverage 검증 | 사람이 해야 할 설계 판단 대체 |
| `.agents/evals/**` | 평가 suite | 에이전트 협력 품질과 edge case 검증 | 제품 요구사항 문서 |

## 현재 Subagent 구성

### Product Planning Designer

[product-planning-designer](.codex/agents/product-planning-designer.toml)는 사용자 요구사항을 업무 흐름, 도메인 구조, 정책, 상태, 화면 설계로 추상화한다.

적용 스킬:

- [product-requirements-planning-rules](.agents/skills/product-requirements-planning-rules/SKILL.md)

책임:

- 모호한 요구사항을 업무 흐름과 정책 단위로 분해한다.
- 상태, 전이, guard, side effect를 명시한다.
- 구현 범위에 영향을 주는 공백은 질문 또는 불확실성으로 남긴다.

책임이 아닌 것:

- API endpoint 세부 스펙 확정
- backend/frontend 기술 설계
- 코드 구현

### API Contract Designer

[api-contract-designer](.codex/agents/api-contract-designer.toml)는 기획 산출물을 backend와 frontend가 공유할 수 있는 API 계약으로 변환한다.

적용 스킬:

- [api-contract-design-rules](.agents/skills/api-contract-design-rules/SKILL.md)

책임:

- operation, request, response, error, auth, cache, mock, contract test 후보를 정리한다.
- backend와 frontend가 병렬 구현 가능한지 `stable_for_parallel` 관점으로 판단한다.
- 정책이나 상태가 불명확한 operation은 확정하지 않는다.

책임이 아닌 것:

- 제품 정책 창작
- backend handler 구현
- frontend client 구현

### Backend Delivery Engineer

[backend-delivery-engineer](.codex/agents/backend-delivery-engineer.toml)는 backend 요청을 기술 설계, 코드 구현, 아키텍처 리뷰 단계로 직접 수행하고 결과를 통합한다.

적용 스킬:

- [backend-technical-design-writing-rules](.agents/skills/backend-technical-design-writing-rules/SKILL.md)
- [backend-code-implementation-rules](.agents/skills/backend-code-implementation-rules/SKILL.md)
- [backend-architecture-review-rules](.agents/skills/backend-architecture-review-rules/SKILL.md)

책임:

- 설계 필요 여부를 판단하고 TDD 또는 skip 근거를 남긴다.
- backend 코드를 요구사항과 설계 결정에 맞게 수정한다.
- compile, test, typecheck 같은 구현 검증 evidence를 남긴다.
- 구현 diff를 Source of Truth 기준으로 리뷰하고 pass/violation을 분리한다.
- blocker/major violation은 remediation input으로 되돌려 최대 3회까지 재작업한다.

책임이 아닌 것:

- frontend UI 구현
- infra 배포 책임
- 보안 민감 신호를 architecture pass로 흡수하는 것

### Frontend Delivery Engineer

[frontend-delivery-engineer](.codex/agents/frontend-delivery-engineer.toml)는 frontend 요청을 기술 설계, UI/client 구현, 아키텍처 리뷰 단계로 직접 수행하고 결과를 통합한다.

적용 스킬:

- [frontend-technical-design-writing-rules](.agents/skills/frontend-technical-design-writing-rules/SKILL.md)
- [frontend-code-implementation-rules](.agents/skills/frontend-code-implementation-rules/SKILL.md)
- [frontend-architecture-review-rules](.agents/skills/frontend-architecture-review-rules/SKILL.md)

책임:

- route, component, state, API, cache, error, browser 검증 계획을 안정화한다.
- UI/client 코드를 요구사항과 설계 결정에 맞게 수정한다.
- build, test, typecheck, browser 같은 구현 검증 evidence를 남긴다.
- 구현 diff를 Source of Truth 기준으로 리뷰하고 pass/violation을 분리한다.
- blocker/major violation은 remediation input으로 되돌려 최대 3회까지 재작업한다.

책임이 아닌 것:

- backend persistence 구현
- infra 배포 책임
- API response shape를 임의 확정하는 것

## 현재 Skill 구성

### Project Context Skills

| Skill | 역할 |
|-------|------|
| [setup-project-context](.agents/skills/setup-project-context/SKILL.md) | 프로젝트명, 비즈니스 목표, PRD, backend/frontend README의 기본 컨텍스트를 일관되게 채운다. |
| [reverse-engineer-backend-docs](.agents/skills/reverse-engineer-backend-docs/SKILL.md) | 기존 backend 코드베이스를 분석해 `docs/backend`를 실제 코드 기반 문서로 갱신한다. |
| [write-structured-artifact](.agents/skills/write-structured-artifact/SKILL.md) | Markdown, skill, subagent TOML을 목적, 책임, 흐름이 먼저 보이도록 구조화한다. |

### Feature Delivery Skills

| Skill | 역할 |
|-------|------|
| [feature-delivery-orchestration-rules](.agents/skills/feature-delivery-orchestration-rules/SKILL.md) | fullstack 기능 요청에서 planning, API contract, backend/frontend delivery subagent 호출 순서를 판단한다. |
| [product-requirements-planning-rules](.agents/skills/product-requirements-planning-rules/SKILL.md) | 업무 흐름, 정책, 상태, 화면 설계, 인수 기준을 구체화한다. |
| [api-contract-design-rules](.agents/skills/api-contract-design-rules/SKILL.md) | product planning 결과를 backend/frontend가 공유할 API 계약으로 변환한다. |

### Backend Delivery Skills

| Skill | 역할 |
|-------|------|
| [backend-technical-design-writing-rules](.agents/skills/backend-technical-design-writing-rules/SKILL.md) | backend 구현 전에 아키텍처 판단과 검증 계획을 TDD로 정리한다. |
| [backend-code-implementation-rules](.agents/skills/backend-code-implementation-rules/SKILL.md) | backend 코드를 요구사항과 설계 결정에 맞게 수정하고 구현 검증 evidence를 남긴다. |
| [backend-architecture-review-rules](.agents/skills/backend-architecture-review-rules/SKILL.md) | backend 변경이 architecture boundary, dependency direction, policy, TDD 결정에 맞는지 독립 검토한다. |

### Frontend Delivery Skills

| Skill | 역할 |
|-------|------|
| [frontend-technical-design-writing-rules](.agents/skills/frontend-technical-design-writing-rules/SKILL.md) | frontend 구현 전에 route, component, state, API, cache, error, browser 검증 계획을 TDD로 정리한다. |
| [frontend-code-implementation-rules](.agents/skills/frontend-code-implementation-rules/SKILL.md) | UI/client 코드를 요구사항과 설계 결정에 맞게 수정하고 구현 검증 evidence를 남긴다. |
| [frontend-architecture-review-rules](.agents/skills/frontend-architecture-review-rules/SKILL.md) | frontend 변경이 architecture, conventions, performance, UI/UX 기준에 맞는지 독립 검토한다. |

## Feature Delivery 관계 흐름

일반적인 fullstack 기능 요청은 아래 흐름으로 처리된다.

1. 호출자가 [feature-delivery-orchestration-rules](.agents/skills/feature-delivery-orchestration-rules/SKILL.md)를 적용한다.
2. 업무 흐름, 정책, 상태, 화면 흐름이 불명확하면 [product-planning-designer](.codex/agents/product-planning-designer.toml)를 호출한다.
3. backend API와 frontend 소비 계약이 함께 바뀌거나 response/request shape가 불명확하면 [api-contract-designer](.codex/agents/api-contract-designer.toml)를 호출한다.
4. API 계약이 `stable_for_parallel`이면 [backend-delivery-engineer](.codex/agents/backend-delivery-engineer.toml)와 [frontend-delivery-engineer](.codex/agents/frontend-delivery-engineer.toml)를 병렬 후보로 호출한다.
5. API 계약이 `partial`, `blocked`, `unknown`이면 backend/frontend 구현 호출을 중단하고 blocker 또는 open question으로 보고한다.
6. 각 delivery engineer는 자기 영역에서 기술 설계, 코드 구현, 아키텍처 리뷰, 재작업 루프를 수행한다.
7. 호출자는 planning, API contract, backend delivery, frontend delivery, review phase, cross-cutting risk를 분리해 최종 결과를 통합한다.

## Review와 검증 구조

이 저장소는 별도 reviewer subagent를 두지 않는다. review는 delivery engineer 내부 단계로 존재하지만, 구현 단계와 분리된 독립 판단으로 수행된다.

원칙:

- 구현 검증 evidence와 architecture review 판정은 섞지 않는다.
- architecture review는 diff, 구현 검증 evidence, rule skill, Source of Truth만 기준으로 판단한다.
- 보안 민감 신호는 architecture pass로 흡수하지 않고 `security_sensitive_blocker` 또는 open question으로 분리한다.
- 문서 구조, 스킬, 서브에이전트 계약 변경은 authoring rule과 validation script로 검증한다.

검증 스크립트:

- [check-playbook.py](.agents/scripts/check-playbook.py): 플레이북 전체 링크, placeholder, rule metadata, workflow validation을 실행한다.
- [validate-agent-workflow-architecture.py](.agents/scripts/validate-agent-workflow-architecture.py): agent/skill 구조와 제거된 구성 요소 재등장을 검사한다.
- [validate-enterprise-eval-suite.py](.agents/scripts/validate-enterprise-eval-suite.py): 대형 코드베이스 평가 suite 구성을 검사한다.
- [validate-feature-delivery-orchestration-evals.py](.agents/scripts/validate-feature-delivery-orchestration-evals.py): feature delivery edge case routing 기대값을 검사한다.
- [validate-skill-authoring-quality.py](.agents/scripts/validate-skill-authoring-quality.py): skill 작성 품질 기준을 검사한다.

## 설계 원칙

- 역할 주체와 작업 규칙을 분리한다.
- subagent는 판단 주체이고, skill은 재사용 가능한 규칙이다.
- subagent가 subagent를 직접 호출한다고 가정하지 않는다.
- 오케스트레이션은 상위 호출자가 skill 규칙을 적용해 수행한다.
- 구현 evidence, review 판정, blocker, open question을 한 문장으로 뭉개지 않는다.
- Source of Truth는 `docs/**`와 실제 코드이며, skill과 subagent는 그 적용 방식을 정한다.
- 대형 코드베이스에서는 전체 정독보다 census, sampling, confidence report, backlog를 우선한다.

## 변경 시 점검 기준

스킬이나 서브에이전트를 추가, 제거, 이름 변경할 때는 아래를 함께 확인한다.

- 해당 역할이 실행 주체인지 작업 규칙인지 먼저 구분한다.
- 실행 주체라면 `.codex/agents/*.toml`에 역할, 판단 철학, 경계, 기본 skill config를 둔다.
- 작업 규칙이라면 `.agents/skills/**/SKILL.md`에 목적, 적용 대상, 작업 흐름, 검증을 둔다.
- 반복 검증은 가능하면 `.agents/scripts`로 분리한다.
- 평가 기준은 `.agents/evals`에 둔다.
- 문서 링크와 구조 검증을 실행한다.

기본 검증 명령:

```bash
python3 .agents/scripts/check-playbook.py
```
