# Router Input Output And Checkpoint Protocol

이 문서는 `implement` 라우터가 backend/frontend 실행 스킬을 조율할 때 사용하는 통합 run id, 영역별 input/output 경계, 체크포인트 확인 절차를 소유한다. D/A/B 세부 input/output payload 스키마와 체크포인트 템플릿은 `implement-backend/references`와 `implement-frontend/references`가 각각 소유한다.

## 저장 위치

라우터는 하나의 사용자 요청에 하나의 `run_id`를 만들고, 영역별 실행 스킬이 같은 run 아래에 자기 마일스톤 산출물을 저장하게 한다.

```text
.agents/runs/{run_id}/
├── planning/
│   ├── 001-P-r00-input.v1.yaml
│   ├── 001-P-r00-planning-result.v1.yaml
│   └── P-r00-v001.md
├── contracts/
│   ├── 001-C-r00-input.v1.yaml
│   ├── 001-C-r00-api-spec-result.v1.yaml
│   └── C-r00-v001.md
├── inputs/
│   ├── M1-backend/
│   │   └── 000-backend-milestone-input.v1.yaml
│   └── M2-frontend/
│       └── 000-frontend-milestone-input.v1.yaml
├── outputs/
│   ├── M1-backend/
│   └── M2-frontend/
└── checkpoints/
    ├── M1-backend/
    └── M2-frontend/
```

경로 규칙:

- `run_id`: 상위 `implement`가 생성하고 backend/frontend 실행 스킬에 전달한다.
- `planning/`: `plan-implementation-requirements`의 기획 input/output/checkpoint를 저장한다.
- `contracts/`: `write-api-spec`의 API 스펙 input/output/checkpoint를 저장한다.
- `M{n}-{area}`: 라우터가 분해한 영역별 마일스톤 식별자. `area`는 `backend` 또는 `frontend`다.
- `000-{area}-milestone-input.v1.yaml`: 라우터가 영역별 실행 스킬에 넘기는 milestone input artifact다. 영역별 실행 스킬은 이 파일을 읽어 자기 `milestone-planning.md` 기준으로 D/A/B input을 만든다.
- 영역 내부의 D/A/B 파일명과 결과 신호는 각 실행 스킬의 [input-output-checkpoint-protocol.md](../../implement-backend/references/input-output-checkpoint-protocol.md) 또는 [input-output-checkpoint-protocol.md](../../implement-frontend/references/input-output-checkpoint-protocol.md)를 따른다.
- 라우터는 `000-{area}-milestone-input.v1.yaml` 외의 영역 내부 파일명을 재정의하지 않는다.

## Area Milestone Input 처리

라우터는 backend/frontend 실행 스킬을 호출하기 전에 영역별 milestone input artifact를 저장한다. 이 artifact는 선행 산출물의 생산자 스킬 이름을 영역별 실행 스킬에 노출하는 대신, backend/frontend가 해석할 수 있는 입력 의미로 정규화한다.

```yaml
schema_version: implement-area-milestone-input/v1
run_id: <run_id>
milestone: M<n>-<area>
area: backend | frontend
created_at: <ISO-8601 timestamp>
input:
  goal: <영역 관점 목표>
  requirements: <구체적 범위와 요구사항>
  explicit_exclusions: <사용자 요청 또는 마일스톤 분할상 제외된 항목. 없으면 "없음">
  success_criteria:
    - <영역별 완료 기준>
  source_artifacts:
    - kind: requirements | domain_policy | api_contract | ui_contract | data_contract | prior_area_output
      path: <artifact 절대 경로>
      reason: <이 영역 마일스톤의 근거로 사용하는 이유>
      stability: stable | partial | blocked | unknown
  dependencies:
    run_after:
      - <선행 마일스톤 id. 없으면 "없음">
    parallel_with:
      - <병렬 실행 가능한 마일스톤 id. 없으면 "없음">
    blockers:
      - <차단 조건. 없으면 "없음">
  integration_notes:
    produces_for_other_area:
      - <다른 영역에 넘길 계약 또는 결과. 없으면 "없음">
    consumes_from_other_area:
      - <다른 영역에서 받아야 할 계약 또는 결과. 없으면 "없음">
artifacts:
  area_inputs_dir: .agents/runs/{run_id}/inputs/M<n>-<area>
  area_outputs_dir: .agents/runs/{run_id}/outputs/M<n>-<area>
  area_checkpoints_dir: .agents/runs/{run_id}/checkpoints/M<n>-<area>
consumer:
  skill: implement-backend | implement-frontend
  planning_reference: .agents/skills/implement-<area>/references/milestone-planning.md
```

처리 절차:

1. 라우터는 기획/API/선행 영역 output artifact를 `source_artifacts`로 정규화한다.
2. `kind`는 생산자 스킬 이름이 아니라 영역별 실행 스킬이 해석할 입력 의미로 작성한다.
3. `stability: blocked`가 있으면 해당 영역 실행을 시작하지 않고 차단 사유를 사용자에게 보고한다.
4. 영역별 실행 스킬은 이 파일을 읽고 자기 `milestone-planning.md` 기준으로 D/A/B input을 만든다.
5. 영역별 D/A/B 계약 문서는 이 artifact의 schema를 재정의하지 않는다.

## Planning And API Spec 처리

라우터는 영역별 실행 전에 필요한 경우 기획 산출물과 API 스펙을 생성한다.

처리 절차:

1. 사용자 요청 하나에 하나의 `run_id`를 만들고 planning/contracts 경로를 먼저 준비한다.
2. 기획 산출물이 필요한 경우 `plan-implementation-requirements` 계약에 맞춰 input artifact를 저장하고 `product-planning-designer` 결과 신호를 확인한다.
3. `PLANNING_CREATED:`이면 결과 파일이 존재하고 비어 있지 않은지 확인한다.
4. `NEEDS_CLARIFICATION:`이면 output artifact의 blocking 질문을 사용자에게 묻고, 영역별 실행을 시작하지 않는다.
5. API 스펙이 필요한 경우 planning output artifact 경로를 `write-api-spec` 계약에 맞춘 input artifact에 넣고 `api-contract-designer`에 전달한다.
6. `API_SPEC_CREATED:`이면 결과 파일의 `payload.stable_for_parallel`을 확인한다.
7. `API_SPEC_BLOCKED:`이면 차단 요소를 사용자 확인 또는 backend 선행 마일스톤으로 분리한다.
8. planning/API checkpoint 신호는 해당 스킬의 계약 문서에 따라 같은 서브에이전트 역할로 재개한다.

## Router Output 처리

라우터는 backend/frontend 실행 스킬의 결과를 통합하기 위해 필요한 최소 정보만 읽는다.

처리 절차:

1. 영역별 실행 전에 `run_id`, 마일스톤 id, 명시적 제외사항, 성공 기준, area milestone input artifact 경로를 고정한다.
2. 공통 API 스펙이 있으면 backend/frontend milestone input artifact의 `source_artifacts`에 같은 계약 artifact 경로를 의미 기반으로 기록한다.
3. backend 산출물이 frontend 입력이 되면 backend 실행 결과에서 API 계약, 미해결 사항, 변경 파일 요약만 읽어 frontend 마일스톤 입력으로 넘긴다.
4. frontend 산출물이 backend 선행 작업 필요성을 드러내면 새 backend 마일스톤을 만들거나 사용자에게 계약 불확실성을 보고한다.
5. 영역별 실행 스킬이 반환한 D/A/B output 파일 경로가 실제로 존재하고 비어 있지 않은지 확인한다.
6. 영역 내부 payload 원문을 불필요하게 복사하지 않고, 통합 보고에 필요한 요약 필드만 읽는다.
7. backend/frontend 중 하나가 실패하면 다른 영역의 완료 상태와 분리해 보고한다.

## Router Checkpoint 처리

라우터는 영역별 실행 스킬이 남긴 체크포인트를 직접 해석해 수정하지 않는다. 체크포인트 재개는 해당 실행 스킬의 프로토콜로 되돌려 보낸다.

처리 절차:

1. 영역별 실행 중 `CONTEXT_CHECKPOINT:` 신호가 반환되면 해당 경로가 현재 영역 마일스톤의 checkpoint 경로인지 확인한다.
2. 파일 존재 여부와 비어 있지 않은지만 확인한다.
3. 체크포인트 파일의 세부 섹션 검증과 재호출 형식은 해당 영역 실행 스킬의 프로토콜을 따른다.
4. 같은 영역의 실행 스킬로 재개하고, 다른 영역 마일스톤에는 체크포인트 내용을 복사하지 않는다.
5. 체크포인트 복구가 두 번 실패하면 자동 루프를 멈추고 사용자에게 영역, 마일스톤, 실패 경로를 보고한다.

## 통합 보고

최종 보고에는 아래 항목을 영역별로 분리해 포함한다.

- 완료한 backend/frontend 마일스톤 수
- planning/API spec artifact 경로와 blocking question 여부
- 영역별 D/A/B input/output 파일 경로
- 영역별 검증 명령과 결과
- 남은 API 계약, UI 계약, 데이터 계약 불확실성
- 자동 수렴 실패 또는 사용자 확인이 필요한 항목

## 검증 스크립트

라우터 프로토콜이나 영역별 실행 프로토콜을 수정한 뒤에는 아래 명령으로 필수 항목을 검증한다.

```bash
python3 .agents/skills/implement/scripts/validate-context-checkpoints.py
```
