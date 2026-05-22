---
name: write-subagent-artifact
description: Use when creating or updating Codex subagent TOML definitions under .codex/agents, including role identity, responsibility boundaries, context principles, judgment criteria, and output principles.
---

# Write Subagent Artifact

## 목적

Codex subagent TOML을 특정 workflow 절차서가 아니라 독립 역할 수행자의 판단 기준으로 작성한다.

이 스킬은 프로젝트 문서나 Codex skill 작성용 스킬이 아니다. 스킬 생성과 수정은 `write-skill-artifact`가 소유한다.

## 적용 대상

- `.codex/agents/*.toml`

## 책임

- subagent의 정체성, 책임, 판단 기준, 작업 경계를 분리한다.
- 호출 input으로 결정돼야 할 파일 경로와 계약 문서를 TOML에 고정하지 않는다.
- 절차, schema, checkpoint template, payload 세부 항목을 TOML에 넣지 않는다.
- 독립 컨텍스트 윈도우에서 동작해도 역할을 수행할 수 있게 작성한다.

## 작업 흐름

1. subagent 역할을 한 문장으로 고정한다.
2. 구현자, reviewer, writer 등 역할 경계를 먼저 정한다.
3. `developer_instructions`를 정체성, 책임, 컨텍스트 원칙, 판단 기준, 경계, 입력·출력 원칙, 완료 체크리스트, 금지 규칙 순서로 작성한다.
4. workflow 절차, 계약 schema, 체크포인트 템플릿은 skill references 또는 contract 문서로 분리한다.
5. TOML이 호출 input만으로 동작하는지 검토한다.
6. 검증 스크립트와 필요한 수동 점검을 실행한다.

## TOML 작성 패턴

`developer_instructions`는 아래 순서를 기본값으로 사용한다.

```text
You are the <Role> sub-agent for this project.

정체성:
책임:
컨텍스트 원칙:
판단 기준:
작업 경계 또는 검토 경계:
입력·출력 원칙:
완료 체크리스트:
- [ ] 정체성, 책임, 판단 기준이 서로 충돌하지 않는다.
- [ ] 특정 스킬, 계약 파일, 고정 Source of Truth 경로 없이 호출 input만으로 동작한다.
- [ ] 구현자, reviewer, writer 등 다른 역할의 책임을 대신 수행하지 않는다.
- [ ] 입력·출력 원칙이 payload 항목이 아니라 출력 규격 준수 원칙만 담는다.
금지 규칙:
```

규칙:

- 특정 스킬, 계약 파일, 고정 Source of Truth 경로를 agent TOML에 넣지 않는다.
- 어떤 입력 파일, 출력 파일, 기준 문서를 사용할지는 호출 input이 결정하게 한다.
- 구현자, reviewer, writer 같은 역할 경계를 명확히 한다.
- 독립 컨텍스트 윈도우에서 동작하므로 이전 대화나 메인 에이전트의 암묵적 기억을 전제하지 않게 한다.
- 절차, schema, checkpoint template은 skill references 또는 계약 문서로 분리한다.
- `입력·출력 원칙`에는 출력 규격 준수 원칙만 두고, payload 항목이나 응답 필드 목록은 계약 문서로 분리한다.
- `완료 체크리스트`는 subagent TOML이 독립 역할 수행자로 완성됐는지 최종 확인하는 항목만 둔다.
- 사용자와 직접 대화하지 않는 경우에도 구조화된 결과 반환 의무를 명시한다.

## 검증

기본 확인:

- `name`, `description`, `developer_instructions`가 모두 있는가
- 정체성, 책임, 컨텍스트 원칙, 판단 기준, 경계, 입력·출력 원칙, 완료 체크리스트, 금지 규칙이 있는가
- workflow 절차, payload 필드 목록, checkpoint template이 TOML에 들어가지 않았는가
- 고정 Source of Truth 경로와 계약 파일 경로가 TOML에 박혀 있지 않은가

보조 스크립트:

```bash
python3 .agents/skills/write-subagent-artifact/scripts/check_subagent_artifact.py <agent.toml> [<agent.toml> ...]
```
