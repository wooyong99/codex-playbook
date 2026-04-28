---
name: setup-project-context
description: Fill project-specific placeholders in AGENTS.md, docs/backend/README.md, and docs/frontend/README.md by reading the current files, finding unresolved project placeholders, interviewing the user only for missing facts, and updating the documents consistently. Use this when setting up a new codex-playbook project, when those files still contain placeholders such as {프로젝트명} or {비즈니스 목표 1}, or when a user asks to initialize project context documents.
---

# 프로젝트 컨텍스트 설정

핵심 프로젝트 지침 문서에 남아 있는 프로젝트 전용 플레이스홀더를 실제 정보로 채운다.

## 대상 파일

항상 아래 파일부터 확인한다:

- [AGENTS.md](../../../AGENTS.md)
- [docs/backend/README.md](../../../docs/backend/README.md)
- [docs/frontend/README.md](../../../docs/frontend/README.md)

[references/target-files.md](references/target-files.md)에서 현재 플레이스홀더 목록과 작성 규칙을 먼저 확인한다.

## 작업 절차

### 1. 현재 상태 확인

- 대상 파일 3개를 읽는다.
- `{프로젝트명}`, `{비즈니스 목표 1}` 같은 미해결 플레이스홀더를 찾는다.
- 이미 실제 프로젝트 내용으로 채워진 섹션은 건너뛴다.

### 2. 부족한 정보만 질문

- 실제 값이 필요한 플레이스홀더에 대해서만 짧게 추가 질문한다.
- 서로 밀접한 질문은 가능한 한 한 번에 묶어서 묻는다.
- 저장소 이름이나 이전 대화에서 명확히 알 수 있는 값은 재사용하고, 그 가정은 짧게 밝힌다.

### 3. 일관되게 반영

- 같은 프로젝트명은 모든 대상 파일에 동일하게 반영한다.
- [AGENTS.md](../../../AGENTS.md)에서는 프로젝트 전용 플레이스홀더 섹션만 채운다. 사용자가 요청하지 않았다면 공통 작업 지침은 다시 쓰지 않는다.
- 백엔드/프론트엔드 README에서는 프로젝트 전용 플레이스홀더만 교체하고, 기존 문서 맵과 구조는 유지한다.

### 4. 마무리 전 검증

- 수정한 구간이나 diff를 다시 확인한다.
- 대상 플레이스홀더가 수정한 섹션 안에 남아 있지 않은지 확인한다.
- 어떤 파일을 수정했는지, 어떤 가정을 사용했는지 함께 보고한다.

## 작성 규칙

- 프로젝트 전용 플레이스홀더만 작업 범위로 본다.
- 사용자가 초안을 명시적으로 요청하지 않았다면 비즈니스 목표를 임의로 만들지 않는다.
- 비즈니스 목표 초안을 제안해야 한다면, 제안안임을 분명히 하고 쉽게 수정할 수 있게 짧고 단순하게 쓴다.
- 문구는 짧고 구체적으로 유지한다. 이 문서들은 마케팅 문서가 아니라 안내 문서다.

## 질문이 필요한 경우

아래 경우에는 바로 쓰지 말고 먼저 사용자에게 확인한다:

- 가능한 프로젝트명이 여러 개라서 어느 값을 써야 할지 불분명할 때
- 비즈니스 목표가 필요하지만 현재 정보만으로 추론할 수 없을 때
- 플레이스홀더는 이미 모두 치환되어 있고, 남은 요청이 단순 치환이 아니라 더 넓은 문서 개편에 해당할 때
