---
name: write-skill-artifact
description: Use when creating or updating project Codex skill folders, SKILL.md files, skill references, scripts, assets, or agents/openai.yaml metadata under .agents/skills.
---

# Write Skill Artifact

## 목적

Codex skill artifact를 목적, 적용 범위, 작업 흐름, 대상별 규칙, 검증 순서로 읽히게 작성한다.

이 스킬은 프로젝트 문서 작성용 스킬이 아니다. 일반 Markdown 문서, backend/frontend 지식 문서, PRD, TDD 본문 작성은 각 영역의 문서 규칙이나 전용 스킬이 소유한다.

## 적용 대상

- `.agents/skills/**/SKILL.md`
- `.agents/skills/**/references/**`
- `.agents/skills/**/scripts/**`
- `.agents/skills/**/assets/**`
- `.agents/skills/**/agents/openai.yaml`

## 책임

- skill의 trigger 조건과 책임을 명확히 한다.
- `SKILL.md`에는 핵심 workflow만 남긴다.
- 긴 템플릿, schema, 세부 정책은 `references/`로 분리한다.
- 반복적이고 결정적인 검증은 `scripts/`로 분리한다.
- UI metadata가 있으면 skill 이름과 설명에 맞게 `agents/openai.yaml`을 갱신한다.

## 작업 흐름

1. 사용자가 새 skill 생성을 요청하면 먼저 `skill-creator`로 scaffold 원칙을 확인한다.
2. skill의 역할을 한 문장으로 고정한다.
3. frontmatter의 `name`과 `description`을 trigger 중심으로 작성한다.
4. 본문은 목적, 적용 대상, 책임, 작업 흐름, 대상별 규칙, 검증 순서로 정리한다.
5. 긴 세부 내용은 `references/`, 반복 검증은 `scripts/`, 출력 자산은 `assets/`로 분리한다.
6. placeholder 문구와 임시 예시를 제거한다.
7. 검증 스크립트와 필요한 수동 점검을 실행한다.

## SKILL.md 작성 패턴

```text
---
name: <skill-name>
description: Use when <specific trigger conditions>
---

# <Skill Title>

## 목적
## 적용 대상
## 책임
## 작업 흐름
## 대상별 처리 규칙
## 검증
```

규칙:

- frontmatter에는 `name`과 `description`만 둔다.
- `name`은 lowercase kebab-case로 작성한다.
- `description`은 workflow 요약이 아니라 언제 이 skill을 써야 하는지 설명한다.
- `SKILL.md`에는 핵심 workflow와 분기 기준만 둔다.
- `references/` 문서는 `SKILL.md`에서 직접 링크하고, 언제 읽어야 하는지 설명한다.
- scaffold placeholder 문구는 반드시 제거한다.

## 리소스 분리 규칙

- `references/`: 상세 템플릿, contract, schema, 정책, 긴 예시
- `scripts/`: 반복 검증, 변환, 생성, 포맷팅처럼 결정적인 작업
- `assets/`: 결과물에 복사하거나 변형할 정적 자산
- `agents/openai.yaml`: UI 표시 이름, 짧은 설명, 기본 프롬프트

## 검증

기본 확인:

- skill 이름과 description이 실제 trigger 조건을 가리키는가
- `SKILL.md` 상단에 목적, 적용 대상, 책임이 드러나는가
- 세부 템플릿과 schema가 본문을 과도하게 차지하지 않는가
- `references/`, `scripts/`, `assets/`가 필요 이상으로 생성되지 않았는가
- placeholder가 남아 있지 않은가

보조 스크립트:

```bash
python3 .agents/skills/write-skill-artifact/scripts/check_skill_artifact.py <SKILL.md> [<SKILL.md> ...]
```
