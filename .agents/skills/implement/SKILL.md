---
name: implement
description: 구현·리팩토링 요청을 backend/frontend/fullstack 영역으로 분류하고 `implement-backend` 또는 `implement-frontend` 실행 스킬로 라우팅하는 상위 오케스트레이션 스킬. 사용자가 단순히 "구현해줘", "만들어줘", "리팩토링해줘", "implement"처럼 영역을 명확히 지정하지 않았거나 backend와 frontend가 함께 걸친 요청일 때 사용한다.
---

# implement — 구현 라우터

## 역할

- 사용자의 구현·리팩토링 요구사항을 backend, frontend, fullstack 중 하나로 분류한다.
- fullstack 요청은 가능한 한 backend 마일스톤과 frontend 마일스톤으로 분리한다.
- 각 영역별 실행은 `implement-backend` 또는 `implement-frontend`가 담당한다.
- 이 스킬은 run id, 영역별 실행 순서, 영역 간 계약 전달, 통합 보고를 소유한다.
- 세부 D/A/B 실행 루프, 역할별 입출력 포맷, 영역 내부 checkpoint 규약은 영역별 실행 스킬이 소유한다.

## 기본 범위

- 포함: 영역이 모호한 구현 요청, backend/frontend가 함께 걸친 기능 구현, 여러 영역으로 분할해야 하는 리팩토링
- 제외: 명확한 backend-only 구현, 명확한 frontend-only 구현, 요구사항만 정리하는 PRD 작업, 구현이 없는 문서 정리
- backend-only 요청은 `implement-backend`로 진행한다.
- frontend-only 요청은 `implement-frontend`로 진행한다.

## 참조 문서

- 라우터 역할 경계와 영역별 실행 스킬 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- 라우터 요구사항 분류와 fullstack 분해 기준: [references/milestone-planning.md](references/milestone-planning.md)
- 라우터 run id와 영역 간 input/output/checkpoint 처리: [references/input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)
- 라우터 영역별 실행 순서와 통합 보고 흐름: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)
- 영역별 D/A/B 실행 계약은 이 스킬에서 열거하지 않고 `implement-backend`와 `implement-frontend`의 `references/`가 소유한다.

## 라우팅 기준

- backend: 서버 API, UseCase, domain, application, storage, external integration, DB/schema, backend policy, `docs/backend/**`
- frontend: UI, page/widget/feature/entity, client state, API client, query key/cache, rendering performance, UI/UX, `docs/frontend/**`
- fullstack: API 계약과 UI가 함께 바뀌거나 backend 결과를 frontend가 소비해야 하는 사용자 흐름
- 문서 구조 변경은 구현 흐름에 끼워 넣지 않고 별도 문서 작업으로 분리한다.
- 보안 민감 변경은 backend 정책 영향 여부를 명시한다.

## 프로세스

### 1. 요구사항을 영역별로 분류한다

- 사용자 요청을 한 문장으로 재진술해 목표를 고정한다.
- 요구사항, 명시적 제외사항, 성공 기준을 분리한다.
- 변경 예상 파일과 문서 기준으로 backend/frontend/fullstack 여부를 판정한다.
- 영역이 불명확하고 잘못 라우팅하면 작업 범위가 달라지는 경우에는 구현 전에 사용자에게 확인한다.

### 2. fullstack 요청을 분해한다

- API 계약, 도메인 상태, 데이터 저장, 외부 연동은 backend 마일스톤으로 둔다.
- 화면, 상호작용, 상태 관리, query/cache, 렌더링 성능은 frontend 마일스톤으로 둔다.
- backend 산출물이 frontend 입력이 되는 경우 backend 마일스톤을 먼저 실행한다.
- 독립적으로 검증 가능한 결과 단위가 아니면 하나의 사용자 흐름 안에서도 backend와 frontend output을 분리한다.

### 3. 영역별 실행 스킬을 호출한다

- backend 마일스톤은 `implement-backend` 프로세스를 따른다.
- frontend 마일스톤은 `implement-frontend` 프로세스를 따른다.
- 같은 run id 아래에서 영역별 input/output/checkpoint 경로가 충돌하지 않도록 sequence를 분리한다.
- 영역 간 input/output 전달과 체크포인트 재개 방식은 [input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)를 따른다.

### 4. 결과를 통합 보고한다

- 영역별 완료 마일스톤 수, A-B 라운드 수, 변경 파일, 검증 결과를 분리해 요약한다.
- backend/frontend 사이의 남은 계약 불확실성을 별도로 보고한다.
- 자동 수렴 실패 또는 사용자 확인이 필요한 항목을 영역별로 분리한다.

## 완료 산출물

- 영역별 실행 스킬과 마일스톤 목록
- 영역별 D/A/B input/output 파일 경로
- 변경 파일 목록과 검증 결과 요약
- 호출된 reviewer별 통과 여부와 남은 위반
- backend/frontend 계약 불확실성

## 검증

라우터 규약, 참조 문서, 영역별 실행 스킬 경계를 수정한 뒤에는 아래 검증을 수행한다.

- `python3 .agents/skills/implement/scripts/validate-context-checkpoints.py`
- `python3 .agents/skills/implement/scripts/check-playbook.py`
- `python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py .agents/skills/implement/SKILL.md .agents/skills/implement/references/*.md`
