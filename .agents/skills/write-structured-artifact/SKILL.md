---
name: write-structured-artifact
description: Create or update project Markdown documents, Codex skills, and subagent TOML definitions with a layered structure. Use when writing or refactoring md files, SKILL.md files, new skills via skill-creator, references, contracts, or .codex/agents/*.toml files so purpose, responsibility, scope, and flow appear before low-level procedures, schemas, implementation details, or code style rules.
---

# Write Structured Artifact

## 목적

문서, 스킬, 서브에이전트 정의를 상위 개념에서 세부 구현 순서로 읽히도록 작성한다.

이 스킬은 새 artifact 생성과 기존 artifact 재구성에 모두 사용한다. 특히 새 스킬을 만들 때는 먼저 `skill-creator`로 scaffold를 생성한 뒤 이 스킬의 구조 원칙을 적용한다.

## 적용 대상

- Markdown 문서: `*.md`, project docs, references, contracts, playbooks
- Codex skills: `.agents/skills/**/SKILL.md`
- Skill 생성 작업: `skill-creator`로 만든 scaffold 후속 정리
- Subagent 정의: `.codex/agents/*.toml`

## 구조 원칙

모든 대상은 아래 목표를 만족해야 한다.

- 고수준 내용과 저수준 내용을 명확하게 분리한다.
- 각 문서의 역할, 책임, 목적, 전체 흐름이 먼저 보이도록 구조화한다.
- 구체적인 처리 방법, 구현 절차, 코드 스타일 등의 내용은 하위 섹션 또는 별도 참고 문서로 분리한다.
- 문서를 읽을 때 상위 개념 -> 세부 구현 순서로 이해할 수 있도록 계층 구조를 개선한다.

성공 기준:

- 고수준 개념과 저수준 구현 내용이 구조적으로 분리된다.
- 전체 구조를 빠르게 이해할 수 있는 문서 계층이 형성된다.
- 세부 구현 내용이 상위 수준 설명을 방해하지 않도록 정리된다.

## 작성 순서

1. 대상 유형을 분류한다: 일반 Markdown, skill, subagent TOML 중 하나로 본다.
2. artifact의 역할을 한 문장으로 고정한다.
3. 상단에 목적, 적용 범위, 책임 또는 전체 흐름을 먼저 배치한다.
4. 세부 절차, schema, 파일명 규칙, 코드 스타일, 예시는 하위 섹션이나 별도 reference로 내린다.
5. 다른 문서가 소유해야 할 내용은 중복하지 말고 링크로 연결한다.
6. 작성 후 성공 기준 체크리스트로 자체 검토한다.
7. 가능하면 `scripts/check_structured_artifact.py`로 대상 파일을 점검한다.

## Markdown 문서 패턴

일반 Markdown 문서는 아래 순서를 기본값으로 사용한다.

```text
# 문서 제목

## 목적
## 적용 범위
## 책임 또는 소유권
## 전체 흐름 또는 문서 계층
## 세부 규칙
## 예외와 경계
## 검증 또는 완료 기준
```

문서가 계약서나 프로토콜이면 `세부 규칙` 아래에 schema, 결과 신호, 파일명 규칙을 둔다. 상단에는 이 문서가 무엇을 소유하고 무엇을 소유하지 않는지만 둔다.

## Skill 작성 패턴

새 skill 생성 요청이면 반드시 `skill-creator`를 먼저 사용해 scaffold를 만든다.

그 다음 `SKILL.md`는 아래 순서로 정리한다.

```text
---
name: <skill-name>
description: <무엇을 하고 언제 쓰는지 구체적으로 설명>
---

# <Skill Title>

## 목적
## 적용 대상
## 작업 흐름
## 대상별 처리 규칙
## 검증
```

규칙:

- frontmatter에는 `name`과 `description`만 둔다.
- description에는 trigger 조건을 충분히 포함한다.
- `SKILL.md`에는 핵심 workflow만 둔다.
- 긴 템플릿, schema, 세부 정책은 `references/`로 분리한다.
- 반복적이고 결정적인 검증은 `scripts/`로 분리한다.
- scaffold placeholder 문구는 반드시 제거한다.
- `agents/openai.yaml`이 있으면 skill 이름과 설명에 맞게 갱신한다.

## Subagent TOML 작성 패턴

서브에이전트는 특정 workflow에 종속된 절차서가 아니라 독립 역할 수행자의 판단 기준이어야 한다.

`developer_instructions`는 아래 순서를 기본값으로 사용한다.

```text
You are the <Role> sub-agent for this project.

정체성:
판단 철학:
판단 렌즈:
작업 경계 또는 검토 경계:
엄격한 제약:
```

규칙:

- 특정 스킬, 계약 파일, 고정 Source of Truth 경로를 agent TOML에 넣지 않는다.
- 어떤 입력 파일, 출력 파일, 기준 문서를 사용할지는 호출 input이 결정하게 한다.
- 구현자, reviewer, writer 같은 역할 경계를 명확히 한다.
- 절차, schema, checkpoint template은 스킬 references 또는 계약 문서로 분리한다.
- 사용자와 직접 대화하지 않는 경우에도 구조화된 결과 반환 의무를 명시한다.

## Refactoring Existing Artifacts

기존 문서를 고칠 때는 내용을 삭제하기 전에 소유권을 먼저 판단한다.

- 상위 문서에 세부 schema가 섞여 있으면 protocol 또는 contract reference로 이동한다.
- 역할 철학 문서에 workflow 절차가 섞여 있으면 스킬 workflow 문서로 이동한다.
- 같은 내용이 여러 문서에 반복되면 단일 출처를 정하고 나머지는 링크로 대체한다.
- 문서 맵이 있으면 새 reference 추가 후 맵을 갱신한다.

## 검증

기본 확인:

- 상단 30% 안에 목적, 적용 범위, 책임 또는 전체 흐름이 드러나는가
- schema, 파일명, 코드 스타일, 명령어 같은 저수준 내용이 상위 설명보다 먼저 나오지 않는가
- 이 문서가 소유하지 않는 내용이 분리되거나 링크 처리됐는가
- scaffold placeholder가 남아 있지 않은가

보조 스크립트:

```bash
python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py <path> [<path> ...]
```

스크립트는 구조 누락을 빠르게 찾는 보조 도구다. 통과가 좋은 문서를 보장하지는 않으며, 실패하면 사람이 구조 원칙에 맞게 보정한다.
