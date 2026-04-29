# Playbook 적용 가이드

`codex-playbook`을 새 프로젝트나 기존 프로젝트에 붙일 때 따라갈 기본 순서.

## 1. 먼저 결정할 것

- 이 저장소를 새 프로젝트의 루트에 둘지
- 기존 프로젝트 안 일부 디렉토리로 복사할지
- 백엔드/프론트엔드 둘 다 쓸지, 한쪽만 쓸지

## 2. 클론 직후 바로 볼 파일

- [README.md](/Users/jeong-uyong/work/codex-playbook/README.md)
- [AGENTS.md](/Users/jeong-uyong/work/codex-playbook/AGENTS.md)
- [docs/backend/README.md](/Users/jeong-uyong/work/codex-playbook/docs/backend/README.md)
- [docs/frontend/README.md](/Users/jeong-uyong/work/codex-playbook/docs/frontend/README.md)

## 3. 가장 먼저 커스터마이징할 영역

### 프로젝트 컨텍스트

- `AGENTS.md`의 프로젝트명과 비즈니스 목표
- `docs/backend/README.md`의 프로젝트명
- `docs/frontend/README.md`의 프로젝트명

이 작업은 [`setup-project-context` 스킬](../.agents/skills/setup-project-context/SKILL.md)로 진행할 수 있다.

### 서브에이전트

- `.codex/agents/*.toml` 이 현재 프로젝트에 맞는지 확인한다.
- 계약 문서 경로, 읽어야 할 문서 범위, sandbox 설정을 점검한다.

### 스킬

- `.agents/skills/` 아래 스킬이 현재 프로젝트에 필요한지 확인한다.
- 필요 없는 스킬은 제거하거나 비활성화하고, 필요한 스킬은 프로젝트 규칙에 맞춰 수정한다.

## 4. 백엔드 문서 적용 순서

1. [docs/backend/README.md](/Users/jeong-uyong/work/codex-playbook/docs/backend/README.md)
2. `docs/backend/architecture/*`
3. `docs/backend/policies/*`
4. `docs/backend/design/*`

기존 코드베이스가 있다면 `reverse-engineer-strategies-v1` 같은 스킬로 `strategies/` 문서를 실제 코드에 맞게 채운다.

## 5. 프론트엔드 문서 적용 순서

1. [docs/frontend/README.md](/Users/jeong-uyong/work/codex-playbook/docs/frontend/README.md)
2. `docs/frontend/architecture/*`
3. `docs/frontend/conventions/*`
4. `docs/frontend/performance/*`
5. `docs/frontend/ui-ux/*`

## 6. 적용 후 점검

- 플레이스홀더가 남아 있지 않은가
- 문서 맵 링크가 현재 구조와 맞는가
- AI 에이전트가 읽는 문서 경로가 실제 저장소 구조와 맞는가
- 프로젝트에 없는 전략을 문서에 일반론으로 남겨두지 않았는가
