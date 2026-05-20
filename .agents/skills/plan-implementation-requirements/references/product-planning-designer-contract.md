# Product Planning Designer — Input / Output Contract

이 문서는 `plan-implementation-requirements` 스킬이 `product-planning-designer` 서브에이전트와 주고받는 인터페이스 규격을 정의한다.

## 문서 역할

이 문서는 기획자 역할의 파일 기반 인터페이스만 소유한다.

- 서브에이전트의 역할 철학은 `.codex/agents/product-planning-designer.toml`이 제공한다.
- 이 문서는 input schema, output schema, 결과 신호, 체크포인트 기준만 소유한다.
- 기획 산출물의 상세 작성 항목은 [planning-artifact-template.md](planning-artifact-template.md)를 따른다.
- API endpoint 세부 스펙은 이 문서가 아니라 `write-api-spec`가 소유한다.

## Input

오케스트레이터는 호출 전에 input artifact를 저장하고, 서브에이전트에는 입력 파일 경로와 계약 파일 경로만 포함한 짧은 프롬프트를 전달한다.

```text
[입력 파일]: .agents/runs/{run_id}/planning/001-P-r00-input.v1.yaml
[계약 파일]: .agents/skills/plan-implementation-requirements/references/product-planning-designer-contract.md
[지시]: 입력 파일을 읽고 계약 파일의 Output 규격에 따라 출력 파일과 체크포인트 파일을 저장하세요.
```

`[입력 파일]`은 YAML로 작성한다.

```yaml
schema_version: plan-implementation-requirements-input/v1
run_id: <run_id>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: product-planning-designer
kind: planning_input
iteration: 0
created_at: <ISO-8601 timestamp>
input:
  original_request: <사용자 원문 또는 요약>
  restated_goal: <한 문장 목표>
  known_requirements:
    - <명시 요구사항>
  explicit_exclusions:
    - <명시 제외사항. 없으면 "없음">
  project_context:
    product_summary: <프로젝트 또는 기능 맥락>
    existing_docs:
      - path: <참조 문서 또는 코드 경로>
        reason: <선별 이유>
  ambiguity_assessment:
    missing_decisions:
      - <구현 범위에 영향을 주는 누락 결정>
    safe_assumptions:
      - <낮은 위험의 임시 가정>
artifacts:
  output_file: .agents/runs/{run_id}/planning/001-P-r00-planning-result.v1.yaml
  checkpoint_file: .agents/runs/{run_id}/planning/P-r00-v001.md
checkpoint:
  criteria: "[체크포인트 판단 기준] 이 문서의 Input > 역할별 체크포인트 기준 그대로."
output_contract:
  path: .agents/skills/plan-implementation-requirements/references/product-planning-designer-contract.md
  section: Output
```

## Input Rules

- 구현 범위에 영향을 주는 누락 결정이 있으면 추측하지 않는다.
- 명시적 제외사항은 산출물 범위에서 제외한다.
- 기존 문서와 사용자 요청이 충돌하면 `open_questions`로 남긴다.
- output 파일은 input의 `artifacts.output_file` 값을 그대로 사용한다.
- checkpoint 파일은 input의 `artifacts.checkpoint_file` 값을 그대로 사용한다.
- 정상 완료 전에도 checkpoint 파일에 완료 snapshot을 저장한다.

### 역할별 체크포인트 기준

남은 작업이 없고 곧 `PLANNING_CREATED:` 또는 `NEEDS_CLARIFICATION:`를 반환할 수 있으면 `CONTEXT_CHECKPOINT:` 신호를 반환하지 말고 정상 완료한다.

아래 전환점 중 하나를 만나고 남은 작업이 있으면 체크포인트한다.

- 사용자 요구 분석에서 업무 흐름 모델링으로 전환한다.
- 업무 흐름에서 정책·상태·화면 설계로 전환한다.
- 산출물 일부를 다음 섹션에서도 보존해야 한다.
- 구현 범위를 바꿀 수 있는 질문이 발견된다.
- 중간 도메인 용어와 정책 결정이 누적되어 완료 전 보존이 필요하다.

## Output

작업 완료 후 반드시 아래 포맷 중 하나로 반환한다.

### Case A: 기획 산출물 작성 완료

먼저 output 파일에 planning artifact를 저장하고, checkpoint 파일에 완료 snapshot을 저장한다. 두 파일 저장이 끝난 뒤 출력 첫 줄에 output 파일 경로만 반환한다.

```text
PLANNING_CREATED: {[출력 파일] 절대 경로}
```

`[출력 파일]`은 YAML로 작성한다.

```yaml
schema_version: plan-implementation-requirements/v1
run_id: <run_id>
sequence: <오케스트레이터가 파일명에 부여한 순번>
role: product-planning-designer
kind: planning_result
iteration: 0
created_at: <ISO-8601 timestamp>
status: completed
payload:
  requirement_summary:
    goal: <한 문장 목표>
    scope:
      - <포함 범위>
    explicit_exclusions:
      - <제외 범위>
    success_criteria:
      - <인수 기준>
  actors_and_permissions:
    - actor: <사용자 또는 시스템 행위자>
      responsibility: <업무 책임>
      permissions:
        - <권한>
  business_flow:
    diagram: <Mermaid 또는 단계형 흐름도>
    steps:
      - trigger: <시작 조건>
        actor: <행위자>
        action: <업무 행동>
        system_response: <시스템 반응>
        result_state: <결과 상태>
  process_model:
    - name: <업무 프로세스명>
      preconditions:
        - <선행 조건>
      main_flow:
        - <정상 흐름>
      alternate_flows:
        - <대체 흐름>
      failure_recovery:
        - <실패와 복구>
  domain_model:
    glossary:
      - term: <도메인 용어>
        meaning: <정의>
    entities:
      - name: <엔티티 또는 개념>
        responsibility: <책임>
        key_fields:
          - <식별자 또는 핵심 속성>
        relationships:
          - <관계>
  policy_definitions:
    business_rules:
      - <업무 규칙>
    authorization_rules:
      - <권한 정책>
    validation_rules:
      - <검증 정책>
    operational_rules:
      - <감사, 알림, 보존, 외부 연동 정책>
  state_definitions:
    states:
      - name: <상태명>
        description: <의미>
        owner: <상태를 소유하는 도메인 또는 화면>
    transitions:
      - from: <이전 상태>
        to: <다음 상태>
        trigger: <전이 조건>
        guard: <허용 조건>
        side_effects:
          - <부수 효과>
  screen_design:
    screens:
      - name: <화면명>
        entry_points:
          - <진입점>
        primary_actions:
          - <주요 액션>
        states:
          - loading
          - empty
          - success
          - error
        navigation:
          - <다음 화면 또는 종료 흐름>
  data_and_events:
    commands:
      - <사용자가 실행하는 변경 요청 후보>
    queries:
      - <화면이 조회해야 하는 데이터 후보>
    events:
      - <감사, 알림, 외부 연동 이벤트 후보>
  api_spec_inputs:
    candidate_operations:
      - <API 스펙으로 전환할 operation 후보>
    shared_dtos:
      - <backend/frontend가 공유해야 할 데이터 의미>
  non_functional_requirements:
    - <성능, 보안, 접근성, 감사, 운영 제약>
  assumptions:
    - <낮은 위험의 가정>
  open_questions:
    - question: <남은 질문. 없으면 "없음">
      blocks_implementation: <true | false>
      reason: <영향>
```

### Case B: 사용자 확인 필요

구현 범위나 정책을 바꾸는 질문이 남아 있으면 output 파일과 checkpoint 파일을 저장한 뒤 아래 신호를 반환한다.

```text
NEEDS_CLARIFICATION: {[출력 파일] 절대 경로}
```

이 경우 output 파일의 `status`는 `needs_clarification`이고 `payload.open_questions`에 사용자에게 물을 질문을 저장한다.

### Case C: 컨텍스트 체크포인트

역할별 체크포인트 기준 중 하나를 만족했고 남은 작업이 있는 경우, 먼저 checkpoint 파일을 저장한다. 신호만 반환하고 파일을 남기지 않는 것은 실패다. 저장이 끝난 뒤 출력 첫 줄에 아래 신호를 출력한다.

```text
CONTEXT_CHECKPOINT: {[체크포인트 파일] 경로}
```

정상 완료 경로에서는 위 신호를 반환하지 않지만, 같은 템플릿의 완료 snapshot을 checkpoint 파일에 반드시 저장한다.

체크포인트 파일은 아래 섹션을 포함한다.

- `# Product Planning Designer Checkpoint`
- `## 체크포인트 사유`: `{normal_completion | requirement_batch_done | flow_model_done | policy_batch_done | screen_batch_done | clarification_needed | 기타}`
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
