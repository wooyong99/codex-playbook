# API Contract Designer — Input / Output Contract

이 문서는 `write-api-spec` 스킬이 `api-contract-designer` 서브에이전트와 주고받는 인터페이스 규격을 정의한다.

## 문서 역할

이 문서는 API 계약 작성 역할의 파일 기반 인터페이스만 소유한다.

- 서브에이전트의 역할 철학은 `.codex/agents/api-contract-designer.toml`이 제공한다.
- 이 문서는 input schema, output schema, 결과 신호, 체크포인트 기준만 소유한다.
- API 스펙 상세 항목은 [api-spec-template.md](api-spec-template.md)를 따른다.
- backend/frontend 구현 세부 설계는 각 실행 스킬이 소유한다.

## Input

오케스트레이터는 호출 전에 input artifact를 저장하고, 서브에이전트에는 입력 파일 경로와 계약 파일 경로만 포함한 짧은 프롬프트를 전달한다.

```text
[입력 파일]: .agents/runs/{run_id}/contracts/001-C-r00-input.v1.yaml
[계약 파일]: .agents/skills/write-api-spec/references/api-contract-designer-contract.md
[지시]: 입력 파일을 읽고 계약 파일의 Output 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

`[입력 파일]`은 YAML로 작성한다.

```yaml
schema_version: write-api-spec-input/v1
run_id: <run_id>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: api-contract-designer
kind: api_spec_input
iteration: 0
created_at: <ISO-8601 timestamp>
input:
  planning_result_file: <plan-implementation-requirements output artifact 절대 경로>
  api_scope:
    - <스펙으로 만들 operation 또는 사용자 흐름>
  explicit_exclusions:
    - <API 스펙에서 제외할 항목. 없으면 "없음">
  project_context:
    existing_api_docs:
      - path: <참조 API 문서 또는 코드 경로>
        reason: <선별 이유>
    backend_frontend_conventions:
      - <확인된 컨벤션>
  unresolved_planning_questions:
    - question: <API 스펙에 영향을 주는 질문. 없으면 "없음">
      impact: <영향>
artifacts:
  output_file: .agents/runs/{run_id}/contracts/001-C-r00-api-spec-result.v1.yaml
  checkpoint_file: .agents/runs/{run_id}/contracts/C-r00-v001.md
checkpoint:
  criteria: "[체크포인트 판단 기준] 이 문서의 Input > 역할별 체크포인트 기준 그대로."
output_contract:
  path: .agents/skills/write-api-spec/references/api-contract-designer-contract.md
  section: Output
```

## Input Rules

- API 스펙은 기획 산출물의 업무 흐름, 정책, 상태, 화면 설계를 기준으로 작성한다.
- API에 영향을 주는 질문이 남아 있으면 endpoint를 추측하지 않는다.
- 기존 API 컨벤션이 있으면 우선 적용하고, 충돌은 `uncertainties`에 남긴다.
- output 파일은 input의 `artifacts.output_file` 값을 그대로 사용한다.
- checkpoint 파일은 input의 `artifacts.checkpoint_file` 값을 그대로 사용한다.
- 정상 완료 전에도 checkpoint 파일에 완료 snapshot을 저장한다.

### 역할별 체크포인트 기준

남은 작업이 없고 곧 `API_SPEC_CREATED:` 또는 `API_SPEC_BLOCKED:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 기획 산출물 분석에서 operation 도출로 전환한다.
- operation 목록에서 DTO/error/auth 세부화로 전환한다.
- backend 계약에서 frontend 소비 계약으로 전환한다.
- 병렬 구현 가능성 판단 전 중간 계약 보존이 필요하다.
- API 스펙을 막는 정책 질문이 발견된다.

## Output

작업 완료 후 반드시 아래 포맷 중 하나로 반환한다.

### Case A: API 스펙 작성 완료

먼저 output 파일에 API spec artifact를 저장하고, checkpoint 파일에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 output 파일 경로만 반환한다.

```text
API_SPEC_CREATED: {[출력 파일] 절대 경로}
```

`[출력 파일]`은 YAML로 작성한다.

```yaml
schema_version: write-api-spec/v1
run_id: <run_id>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: api-contract-designer
kind: api_spec_result
iteration: 0
created_at: <ISO-8601 timestamp>
status: completed
payload:
  stable_for_parallel: <true | false>
  spec_summary:
    goal: <API 스펙 목표>
    linked_planning_result_file: <기획 산출물 경로>
    covered_flows:
      - <사용자 흐름>
  global_contract:
    base_path: <공통 base path 또는 "프로젝트 컨벤션 따름">
    auth: <인증 방식>
    content_type: <예: application/json>
    error_shape: <공통 오류 응답 shape>
    date_time_format: <날짜/시간 형식>
    pagination: <공통 페이지네이션 규칙>
    idempotency: <공통 멱등성 규칙>
  operations:
    - operation_id: <고유 operation id>
      method: <GET | POST | PUT | PATCH | DELETE>
      path: <endpoint path>
      purpose: <업무 목적>
      linked_flow_step: <기획 산출물의 흐름 단계>
      auth_policy: <권한 정책>
      request:
        path_params:
          - name: <이름>
            type: <타입>
            required: <true | false>
        query_params:
          - name: <이름>
            type: <타입>
            required: <true | false>
        body:
          schema: <객체 schema 또는 null>
          validation:
            - <검증 규칙>
      response:
        success_status: <HTTP status>
        body_schema: <응답 schema>
        empty_state: <빈 결과 의미>
      errors:
        - status: <HTTP status>
          code: <서비스 error code>
          message_policy: <사용자 표시 또는 내부 처리 정책>
          recovery: <사용자 또는 시스템 복구 방식>
      side_effects:
        - <상태 변경, 이벤트, 알림, 감사 로그>
      cache:
        key_hint: <frontend cache key 힌트>
        invalidation:
          - <무효화 조건>
      concurrency:
        idempotency_key: <필요 여부>
        conflict_policy: <충돌 처리>
      parallel_work:
        backend_ready: <true | false>
        frontend_ready: <true | false>
        blockers:
          - <병렬 구현 차단 요소. 없으면 "없음">
  shared_schemas:
    - name: <DTO 또는 value object 이름>
      fields:
        - name: <필드명>
          type: <타입>
          required: <true | false>
          description: <도메인 의미>
  frontend_consumption:
    screens:
      - screen: <화면명>
        operations:
          - <operation id>
        ui_states:
          - <loading | empty | success | error 등>
  backend_implementation_notes:
    use_cases:
      - <backend use case 후보>
    transaction_boundaries:
      - <트랜잭션 경계>
    persistence_notes:
      - <저장 또는 조회 힌트>
  contract_tests:
    - scenario: <계약 검증 시나리오>
      request: <요청 예시>
      expected_response: <응답 예시>
  mock_scenarios:
    - name: <frontend 병렬 구현용 mock scenario>
      operations:
        - <operation id>
  uncertainties:
    - <있다면 기재. 없으면 "없음">
```

### Case B: API 스펙 차단

API 계약을 확정할 수 없는 질문이 남으면 output 파일과 checkpoint 파일을 저장한 뒤 아래 신호를 반환한다.

```text
API_SPEC_BLOCKED: {[출력 파일] 절대 경로}
```

이 경우 output 파일의 `status`는 `blocked`이고 `payload.uncertainties`와 `payload.operations[].parallel_work.blockers`에 차단 요소를 저장한다.

### Case C: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 checkpoint 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 checkpoint 파일에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# API Contract Designer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | planning_analysis_done | operation_batch_done | schema_batch_done | frontend_contract_done | blocked_by_policy | 기타}`
- `## 현재 목표`
- `## 핵심 규칙`
- `## 금지 규칙`
- `## 안티패턴`
- `## 완료된 작업`
- `## 진행중 작업`
- `## 남은 작업`
- `## 주의사항`
- `## 실패 패턴`
- `## 최근 결정`
- `## 진행 상태`
