---
name: setup-project-context
description: Force-initialize and fill project context placeholders in AGENTS.md, docs/backend/README.md, docs/frontend/README.md, and docs/PRD.md. When invoked, reset the project-context sections to placeholder mode as needed, ask the user for the required project facts, and then fill all target documents consistently. Use this when setting up or reinitializing codex-playbook project context.
---

# 프로젝트 컨텍스트 설정

## 목적

핵심 프로젝트 지침 문서의 프로젝트 전용 컨텍스트를 강제로 초기화한 뒤, 사용자에게 필요한 정보를 질문하고 4개 대상 문서를 일관되게 채운다.

이 스킬은 no-op 스킬이 아니다. 대상 문서가 이미 채워져 있어도 호출되면 재설정 의도로 해석하고 사용자와 상호 작용해 최신 값으로 다시 채운다.

## 적용 범위

포함:

- [AGENTS.md](../../../AGENTS.md)의 프로젝트명과 비즈니스 목표
- [docs/backend/README.md](../../../docs/backend/README.md)의 프로젝트 전용 소개
- [docs/frontend/README.md](../../../docs/frontend/README.md)의 프로젝트 전용 소개
- [docs/PRD.md](../../../docs/PRD.md)의 제품 요구사항 컨텍스트

제외:

- 공통 AI 작업 지침 자체의 재작성
- 백엔드/프론트엔드 하위 문서 맵의 구조 개편
- 사용자 답변 없이 비즈니스 목표나 PRD 내용을 임의 생성하는 작업

## 운영 모델

```text
호출 감지
  -> 대상 파일과 초기화 범위 확인
  -> 사용자에게 필수 프로젝트 사실 질문
  -> 답변을 4개 문서에 일관 반영
  -> 플레이스홀더와 값 불일치 검증
  -> 수정 파일과 사용한 답변 보고
```

## 참조 문서

- [target-files.md](references/target-files.md): 대상 파일별 소유 범위, 플레이스홀더, 일관성 규칙

## 작업 흐름

1. [target-files.md](references/target-files.md)를 먼저 읽고 대상 파일별 수정 가능 범위를 고정한다.
2. 대상 파일 4개를 읽고 현재 프로젝트 컨텍스트와 남아 있는 플레이스홀더를 확인한다.
3. 수정 가능 구간은 기존 값이 있어도 플레이스홀더 초기화 대상으로 보고 재작성 범위를 표시한다.
4. 사용자에게 필수 프로젝트 사실을 질문하고, 기존 값은 참고 정보로만 사용한다.
5. 답변받은 값은 모든 대상 문서에 동일한 의미로 반영한다.
6. 누락 답변은 임의 작성하지 않고 `미정` 또는 `확인 필요`로 표시하거나 추가 질문한다.
7. 마무리 전 대상 파일 4개를 다시 확인해 플레이스홀더와 값 불일치를 제거한다.

## 질문 원칙

이 스킬을 호출하면 기본적으로 질문이 필요하다. 한 번에 너무 많은 질문을 던지지 말고, 우선 아래 정보를 묶어 확인한다.

- 프로젝트명
- 비즈니스 목표 3개
- PRD 한 줄 요약
- 배경 및 해결하려는 문제
- 주요 사용자와 진입점
- 기능 요구사항
- 비기능 요구사항
- 제약 사항
- 주요 마일스톤 또는 타임라인

질문이 반드시 필요한 경우:

- 사용자가 일부 항목만 답하면 답변받은 값은 반영하고, 누락된 항목은 다시 질문한다.
- 저장소 이름이나 이전 대화에서 추론 가능한 값이 있어도 최종 반영 전 사용자 확인을 받는다.
- 기존 문서 값과 사용자 답변이 충돌하면 사용자 답변을 기준으로 할지 확인한다.

## 작성 규칙

- 프로젝트 전용 컨텍스트 섹션만 작업 범위로 본다.
- 같은 프로젝트명과 비즈니스 목표는 모든 대상 파일에 동일하게 반영한다.
- 사용자가 답하지 않은 비즈니스 목표나 PRD 내용을 임의로 만들지 않는다.
- 초안을 제안해야 한다면 제안안임을 분명히 하고, 최종 반영 전 사용자 확인을 받는다.
- 문구는 짧고 구체적으로 유지한다. 이 문서들은 마케팅 문서가 아니라 안내 문서다.

## 검증

- 수정한 구간이나 diff를 다시 확인한다.
- 대상 파일 4개에 초기화 대상 플레이스홀더가 남아 있지 않은지 확인한다.
- 4개 파일의 프로젝트명과 비즈니스 목표가 서로 일치하는지 확인한다.
- [target-files.md](references/target-files.md)의 파일별 작성 규칙과 충돌하지 않는지 확인한다.

## 바로 종료하지 말아야 하는 경우

아래 경우에도 no-op으로 종료하지 않는다:

- 대상 파일 4개가 이미 채워져 있을 때
- `docs/PRD.md`만 재초기화가 필요한 것처럼 보일 때
- 저장소명이나 이전 문서에서 값을 추론할 수 있을 때
- 사용자가 "setup-project-context 호출"을 명시했을 때

## 완료 기준

완료 응답에는 수정한 파일, 반영한 사용자 답변, 아직 `미정` 또는 `확인 필요`로 남긴 항목을 함께 보고한다.
