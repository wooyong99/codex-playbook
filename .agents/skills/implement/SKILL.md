---
name: implement
description: 구현·리팩토링 요청을 기획/API 스펙/backend/frontend 단계로 분류하고, `product-planning-designer`, `api-contract-designer`, `implement-backend`, `implement-frontend`를 조율하는 상위 오케스트레이션 스킬. 사용자가 단순히 "구현해줘", "만들어줘", "리팩토링해줘", "implement"처럼 영역을 명확히 지정하지 않았거나 backend와 frontend가 함께 걸친 요청일 때 사용한다.
---

# implement — 구현 라우터

## 역할

- 사용자의 구현·리팩토링 요구사항을 backend, frontend, fullstack 중 하나로 분류한다.
- 요구사항이 모호하거나 업무 정책·상태·화면 흐름이 비어 있으면 `plan-implementation-requirements` 계약에 따라 `product-planning-designer`를 호출해 구현 전 기획 산출물을 만든다.
- fullstack 또는 API 변경 요청은 영역별 실행 전에 `write-api-spec` 계약에 따라 `api-contract-designer`를 호출해 backend/frontend 공통 API 스펙을 만든다.
- fullstack 요청은 가능한 한 backend 마일스톤과 frontend 마일스톤으로 분리한다.
- 각 영역별 실행은 `implement-backend` 또는 `implement-frontend`가 담당한다.
- 이 스킬은 run id, 기획/API 선행 단계의 호출 순서, 영역별 실행 순서, 영역 간 계약 전달, 통합 보고를 소유한다.
- 선행 스킬은 workflow, contract, checkpoint schema의 단일 출처이고, 서브에이전트는 해당 계약을 입력으로 받아 역할을 수행한다.
- 세부 D/A/B 실행 루프, 역할별 입출력 포맷, 영역 내부 checkpoint 규약은 영역별 실행 스킬이 소유한다.

## 기본 범위

- 포함: 영역이 모호한 구현 요청, backend/frontend가 함께 걸친 기능 구현, 여러 영역으로 분할해야 하는 리팩토링, 구현 전 요구사항 구체화와 API 스펙 선행 작업
- 제외: 구현이 없는 독립 PRD 작업, 구현이 없는 문서 정리, 코드 변경과 무관한 제품 전략 수립
- backend-only 요청은 `implement-backend`로 진행한다.
- frontend-only 요청은 `implement-frontend`로 진행한다.
- 단, backend-only 또는 frontend-only라도 업무 정책·상태·화면 흐름이 구현 품질을 좌우하고 사용자의 요구가 빈약하면 먼저 기획 phase를 실행한다.

## 참조 문서

- 라우터 역할 경계와 영역별 실행 스킬 경계: [references/orchestration-boundaries.md](references/orchestration-boundaries.md)
- 라우터 요구사항 분류와 fullstack 분해 기준: [references/milestone-planning.md](references/milestone-planning.md)
- 라우터 run id와 영역 간 input/output/checkpoint 처리: [references/input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)
- 라우터 영역별 실행 순서와 통합 보고 흐름: [references/milestone-execution-workflow.md](references/milestone-execution-workflow.md)
- 구현 전 기획 산출물 계약: [../plan-implementation-requirements/SKILL.md](../plan-implementation-requirements/SKILL.md)
- backend/frontend 공통 API 스펙 계약: [../write-api-spec/SKILL.md](../write-api-spec/SKILL.md)
- 기획 phase 수행자: `product-planning-designer`
- API spec phase 수행자: `api-contract-designer`
- 영역별 D/A/B 실행 계약은 이 스킬에서 열거하지 않고 `implement-backend`와 `implement-frontend`의 `references/`가 소유한다.

## 라우팅 기준

- backend: 서버 API, UseCase, domain, application, storage, external integration, DB/schema, backend policy, `docs/backend/**`
- frontend: UI, page/widget/feature/entity, client state, API client, query key/cache, rendering performance, UI/UX, `docs/frontend/**`
- planning-required: 업무 흐름, 정책, 상태, 화면 흐름, 도메인 용어가 구현 전에 확정되어야 하는 요청
- api-spec-required: backend API와 frontend 소비 계약이 함께 바뀌거나 병렬 구현을 위해 공통 API 스펙이 필요한 요청
- fullstack: API 계약과 UI가 함께 바뀌거나 backend 결과를 frontend가 소비해야 하는 사용자 흐름
- 문서 구조 변경은 구현 흐름에 끼워 넣지 않고 `documentation-governance-reviewer` 검토 대상으로 분리한다.
- 보안 민감 변경은 영역과 무관하게 `security-policy-reviewer`를 추가한다.

## 프로세스

### 1. 요구사항을 기획 가능 상태로 만든다

- 사용자 요청을 한 문장으로 재진술해 목표를 고정한다.
- 요구사항, 명시적 제외사항, 성공 기준을 분리한다.
- 업무 흐름, 정책, 상태 전이, 화면 흐름, 도메인 용어 중 구현에 필요한데 비어 있는 축을 찾는다.
- 비어 있는 축을 추측하면 구현 범위가 달라지는 경우 사용자에게 질문하거나 기획 phase를 실행한다.
- 기획 phase는 `plan-implementation-requirements`의 workflow와 계약 파일을 로드하고, `product-planning-designer`에 input artifact와 계약 경로를 전달해 수행한다.
- 기획 산출물은 `.agents/runs/{run_id}/planning/` 아래에 저장하고 이후 API 스펙과 영역별 실행 입력으로 넘긴다.

### 2. API 스펙 필요 여부를 판정한다

- backend API와 frontend 소비 계약이 함께 바뀌면 API spec phase를 실행한다.
- API spec phase는 `write-api-spec`의 workflow와 계약 파일을 로드하고, `api-contract-designer`에 input artifact와 계약 경로를 전달해 수행한다.
- API 스펙은 기획 산출물의 업무 흐름, 정책, 상태, 화면 설계를 기준으로 만든다.
- API 스펙이 `stable_for_parallel`이면 backend/frontend 마일스톤을 같은 계약으로 병렬 실행할 수 있다.
- API 스펙이 차단되면 영역별 실행을 시작하지 않고 사용자 질문 또는 backend 선행 마일스톤으로 분리한다.

### 3. 요구사항을 영역별로 분류한다

- 변경 예상 파일과 문서 기준으로 backend/frontend/fullstack 여부를 판정한다.
- 기획 산출물과 API 스펙이 있으면 이를 라우팅의 기준 입력으로 사용한다.
- 영역이 불명확하고 잘못 라우팅하면 작업 범위가 달라지는 경우에는 구현 전에 사용자에게 확인한다.

### 4. fullstack 요청을 분해한다

- API 계약, 도메인 상태, 데이터 저장, 외부 연동은 backend 마일스톤으로 둔다.
- 화면, 상호작용, 상태 관리, query/cache, 렌더링 성능은 frontend 마일스톤으로 둔다.
- 공통 API 스펙이 안정적이면 backend/frontend 마일스톤을 병렬 실행 후보로 둔다.
- API 스펙 없이 backend 산출물이 frontend 입력이 되는 경우 backend 마일스톤을 먼저 실행한다.
- 독립적으로 검증 가능한 결과 단위가 아니면 하나의 사용자 흐름 안에서도 backend와 frontend output을 분리한다.

### 5. 영역별 실행 스킬을 호출한다

- backend 마일스톤은 `implement-backend` 프로세스를 따른다.
- frontend 마일스톤은 `implement-frontend` 프로세스를 따른다.
- 기획 산출물과 API 스펙 경로는 영역별 milestone input artifact의 `source_artifacts`로 정규화해 전달한다.
- 같은 run id 아래에서 영역별 input/output/checkpoint 경로가 충돌하지 않도록 sequence를 분리한다.
- 영역 간 input/output 전달과 체크포인트 재개 방식은 [input-output-checkpoint-protocol.md](references/input-output-checkpoint-protocol.md)를 따른다.

### 6. 결과를 통합 보고한다

- 기획 산출물과 API 스펙 결과를 먼저 요약한다.
- 영역별 완료 마일스톤 수, A-B 라운드 수, 변경 파일, 검증 결과를 분리해 요약한다.
- backend/frontend 사이의 남은 계약 불확실성을 별도로 보고한다.
- 자동 수렴 실패 또는 사용자 확인이 필요한 항목을 영역별로 분리한다.

## 검증

- 라우터, planning/API, backend/frontend 계약 문서 링크가 실제 파일을 가리키는지 확인한다.
- `python3 .agents/skills/implement/scripts/validate-context-checkpoints.py`로 라우터와 영역별 계약 필수 항목을 검증한다.
- `python3 .agents/skills/implement/scripts/check-playbook.py`로 문서 링크와 플레이북 일관성을 검증한다.
- 새 스킬 또는 서브에이전트가 추가되면 `quick_validate.py`와 `check_structured_artifact.py`를 함께 실행한다.

## 완료 산출물

- 기획 산출물 경로와 남은 사용자 확인 질문
- API 스펙 경로와 병렬 구현 가능 여부
- 영역별 실행 스킬과 마일스톤 목록
- 영역별 D/A/B input/output 파일 경로
- 변경 파일 목록과 검증 결과 요약
- 호출된 reviewer별 통과 여부와 남은 위반
- backend/frontend 계약 불확실성
