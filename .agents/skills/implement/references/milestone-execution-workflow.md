# Router Milestone Execution Workflow

이 문서는 `implement` 라우터의 영역 분류, backend/frontend 실행 스킬 호출, 결과 통합 흐름을 소유한다. 영역 내부 D/A/B 실행 루프는 `implement-backend/references/milestone-execution-workflow.md`와 `implement-frontend/references/milestone-execution-workflow.md`가 각각 소유한다.

## 전체 흐름

각 사용자 요청은 아래 순서로 실행한다.

1. 요구사항을 backend, frontend, fullstack 중 하나로 분류한다.
2. fullstack 요청은 가능한 한 backend 마일스톤과 frontend 마일스톤으로 분리한다.
3. 영역별 실행 스킬을 호출한다.
4. 영역별 input/output 파일과 검증 결과를 확인한다.
5. 영역 간 계약 불확실성이 남으면 사용자에게 보고하거나 후속 마일스톤으로 분리한다.
6. 모든 영역이 완료되면 통합 결과를 보고한다.

## Step 1. 요청 분류

- 사용자 요청을 한 문장 목표로 고정한다.
- 요구사항, 명시적 제외사항, 성공 기준을 분리한다.
- 변경 예상 파일과 문서 기준으로 backend/frontend/fullstack 여부를 판정한다.
- 잘못 라우팅하면 구현 범위가 달라지는 경우에는 구현 전에 사용자에게 확인한다.

## Step 2. Fullstack 분해

- API 계약, 도메인 상태, 데이터 저장, 외부 연동은 backend 마일스톤으로 둔다.
- 화면, 상호작용, 상태 관리, query/cache, 렌더링 성능은 frontend 마일스톤으로 둔다.
- backend 산출물이 frontend 입력이 되는 경우 backend 마일스톤을 먼저 실행한다.
- 독립적으로 검증 가능한 결과 단위가 아니면 하나의 사용자 흐름 안에서도 backend와 frontend output을 분리한다.

## Step 3. 영역별 실행 스킬 호출

- backend 마일스톤은 `implement-backend` 프로세스를 따른다.
- frontend 마일스톤은 `implement-frontend` 프로세스를 따른다.
- 같은 run id 아래에서 영역별 input/output/checkpoint 경로가 충돌하지 않도록 마일스톤 id를 분리한다.
- 영역 내부 D/A/B 계약, 체크포인트 기준, 검증 명령 판단은 해당 실행 스킬의 `references/` 문서를 따른다.

## Step 4. 결과 통합

- backend 실행 결과에서 frontend가 소비해야 할 API 계약, 미해결 사항, 검증 결과를 읽는다.
- frontend 실행 결과에서 backend 계약 누락, API 불확실성, UI 검증 결과를 읽는다.
- 한 영역이 실패해도 다른 영역의 완료 상태를 덮어쓰지 않는다.
- 문서 또는 보안 supplemental reviewer 결과는 해당 영역의 결과와 함께 보고한다.

## Step 5. 계약 불확실성 처리

- backend 결과가 frontend 구현에 필요한 계약을 제공하지 못하면 frontend 마일스톤을 시작하지 않는다.
- frontend 구현 중 backend 계약 불확실성이 드러나면 새 backend 마일스톤으로 분리하거나 사용자에게 범위 확장을 확인한다.
- 영역 간 계약 불확실성은 임의로 추측하지 않고 결과 보고의 별도 항목으로 남긴다.

## Escalation

자동 수렴에 실패하면 마지막 영역별 결과를 3~5줄로 요약하고 사용자 선택을 기다린다.

선택지:

- 현재 상태로 커밋하고 수동 검토
- 실패한 영역만 재시작
- 요구사항을 재정의하고 전체 run 재시작
- 실패한 영역을 스킵하고 완료된 영역만 유지
- 전체 중단

## 전체 완료 보고

모든 영역이 완료되면 아래 항목을 요약한다.

- 완료한 backend/frontend 마일스톤 수
- 영역별 D/A/B input/output 파일 경로
- 변경 파일 수와 주요 변경 요약
- 실행한 검증 명령과 결과
- 남은 API/UI/data 계약 불확실성
- 커밋 그룹핑 또는 커밋 작성 제안
