---
name: feature-delivery-orchestration-rules
description: feature delivery 요청에서 product planning, API contract, backend/frontend delivery engineer subagent를 오케스트레이션하고 결과를 통합할 때 사용한다. subagent가 다른 subagent를 호출할 수 없는 runtime에서 fullstack 기능 전달 오케스트레이션이 필요한 경우 사용한다.
---

# Feature Delivery Orchestration Rules

## 목적

feature delivery 흐름을 직접 오케스트레이션한다.

이 skill은 fullstack 기능 요청을 planning, API contract, backend, frontend 작업으로 분리하고 필요한 하위 subagent를 호출해 결과를 통합한다.

## 적용 대상

- backend와 frontend가 함께 바뀌는 기능 요청
- API 계약 안정성에 따라 backend/frontend 병렬 실행 여부를 판단해야 하는 요청
- product planning, API contract, backend delivery, frontend delivery 결과를 분리해 통합해야 하는 요청

## 작업 흐름

1. 요청을 업무 흐름, 정책, 화면/API 계약, backend 범위, frontend 범위로 나눈다.
2. planning 필요 여부, API spec 필요 여부, `stable_for_parallel` 여부를 판단한다.
3. planning이 필요하면 `product-planning-designer`를 호출하고 결과를 다음 입력으로 사용한다.
4. API spec이 필요하면 `api-contract-designer`를 호출하고 계약 안정성을 다시 판단한다.
5. API 계약이 stable이면 `backend-delivery-engineer`와 `frontend-delivery-engineer`를 병렬 후보로 호출한다.
6. API 계약이 stable이 아니면 backend/frontend 구현 호출을 중단하고 blocker/open question을 보고한다.
7. 보안 민감 요청이나 문서/스킬 계약 변경처럼 delivery 범위와 충돌하는 cross-cutting risk는 별도 subagent dispatch가 아니라 blocker, open question, follow-up으로 분리한다.
8. 하위 subagent가 `dispatch_requests`를 반환하면 그 요청을 실제 subagent 호출로 실행한다.
9. planning, API spec, backend, frontend, review phase, cross-cutting risk를 분리해 최종 보고한다.

## 대상별 처리 규칙

- `product-planning-designer`: 업무 흐름, 정책, 상태, 화면 흐름이 비어 있을 때 호출한다.
- `api-contract-designer`: backend API와 frontend 소비 계약이 함께 바뀌거나 response/request shape가 불명확할 때 호출한다.
- `backend-delivery-engineer`: 안정화된 API 계약과 backend 범위가 있을 때 호출한다.
- `frontend-delivery-engineer`: 안정화된 API 계약과 frontend 범위가 있을 때 호출한다.

Cross-cutting risk는 아래처럼 처리한다.

- secret, token, credential, 인증/인가, 민감 정보, 외부 신뢰 경계, 로그 마스킹 위험은 `security_sensitive_blocker` 또는 open question으로 남긴다.
- 문서 맵, 스킬, 서브에이전트 정의, README, docs 구조 변경은 해당 artifact 작성/검증 규칙과 validation 결과로 다루고, feature delivery 완료 조건과 섞지 않는다.

## Readiness 판단

- 업무 흐름, 정책, 상태, 화면 흐름이 비어 있으면 product planning을 먼저 둔다.
- backend API와 frontend 소비 계약이 함께 바뀌면 API spec을 먼저 둔다.
- API spec이 stable이 아니면 backend/frontend 병렬 실행 후보로 두지 않는다.
- 선행 산출물은 생산자 이름이 아니라 소비 의미로 전달한다.
- 남은 API/UI/data 계약 불확실성은 추측 없이 open question 또는 blocker로 남긴다.

## 병렬화 기준

- backend/frontend 병렬 실행은 API 계약이 `stable_for_parallel`일 때만 허용한다.
- 병렬 호출 input에는 같은 API 계약과 서로 다른 backend/frontend 범위를 분리해 전달한다.
- 한쪽 결과가 다른 쪽 입력이면 병렬로 실행하지 않는다.
- 계약이 partial, blocked, unknown이면 구현 subagent를 호출하지 않는다.

## Dispatch 루프

하위 subagent가 `dispatch_requests`를 반환하면:

1. 자동 완료로 보지 않는다.
2. 각 `target_agent`를 실제로 호출한다.
3. `parallel_allowed: true`인 요청끼리만 병렬 실행한다.
4. 반환된 결과를 원래 subagent 또는 최종 통합 단계에 다시 제공한다.
5. 실제 호출하지 않은 subagent는 실행 완료로 보고하지 않는다.

`dispatch_requests` 항목은 아래 필드를 갖춘다.

```yaml
dispatch_requests:
  - target_agent: backend-delivery-engineer | frontend-delivery-engineer | product-planning-designer | api-contract-designer
    reason: "<호출 사유>"
    input_artifacts:
      - "<전달할 planning/API/review 산출물 또는 사용자 입력>"
    required_context:
      - "<대상 subagent가 반드시 알아야 하는 범위/제약>"
    depends_on:
      - "<먼저 완료되어야 하는 target_agent 또는 artifact>"
    parallel_allowed: true | false
    blocked_by:
      - "<계약/정책/입력 불확실성. 없으면 빈 목록>"
    return_to: feature-delivery-orchestration-rules | "<원래 요청한 subagent>"
```

필수 규칙:

- `target_agent`, `reason`, `input_artifacts`, `parallel_allowed`, `return_to`는 생략하지 않는다.
- `depends_on`이 비어 있지 않으면 `parallel_allowed: false`로 둔다.
- `blocked_by`가 비어 있지 않으면 실제 호출하지 않고 blocker/open question으로 통합한다.
- 같은 API 계약을 공유하는 backend/frontend 요청은 같은 `input_artifacts` 계약을 참조해야 한다.

## 결과 통합

최종 보고에는 아래 항목을 분리한다.

```yaml
orchestration_result:
  entry_skill: feature-delivery-orchestration-rules
  request_summary: "<요청 요약>"
  scope:
    business_flow: known | partial | unknown
    backend: required | not_required | blocked
    frontend: required | not_required | blocked
    api_contract: stable_for_parallel | partial | blocked | unknown
  readiness:
    planning: required | skipped | completed | blocked
    api_contract: required | skipped | completed | blocked
    backend_frontend_parallel: true | false
    parallel_reason: "<API 계약 안정성 또는 순차 의존성 근거>"
  dispatch:
    executed:
      - "<실제 호출한 subagent>"
    skipped:
      - target_agent: "<호출하지 않은 subagent>"
        reason: "<skip/block 근거>"
    pending_dispatch_requests: []
  results:
    planning: "<결과 또는 skip/block 근거>"
    api_contract: "<결과와 stability 판단>"
    backend_delivery: "<결과 또는 blocked 사유>"
    frontend_delivery: "<결과 또는 blocked 사유>"
    review_phases:
      - owner: backend-delivery-engineer | frontend-delivery-engineer
        result: pass | violation | blocked | not_run
    cross_cutting_risks:
      - risk_id: security_sensitive_blocker | documentation_contract_change | "<risk id>"
        handling: blocked | open_question | follow_up | not_applicable
  open_questions:
    - "<남은 계약/정책/UI/data 불확실성>"
  follow_ups:
    - "<후속 작업>"
```

필수 규칙:

- `backend_frontend_parallel`은 API 계약이 `stable_for_parallel`일 때만 `true`로 둔다.
- 실제 호출하지 않은 subagent는 `executed`에 넣지 않는다.
- review phase 결과는 implementation evidence와 분리한다.
- security/documentation risk는 별도 subagent 실행 결과로 꾸미지 않고 blocker/open question/follow-up으로 보고한다.
- `open_questions`에는 추측으로 해소한 항목을 넣지 않는다.

## 안티패턴

- 상위 subagent가 자동으로 다른 subagent를 호출한다고 기대한다.
- API 계약이 stable이 아닌데 backend/frontend를 병렬 실행한다.
- planning 결과를 구현 완료로 보고한다.
- 하위 subagent가 반환한 `dispatch_requests`를 실행 결과처럼 취급한다.
- backend/frontend 세부 구현 규칙을 이 skill에 복사한다.
- API response shape를 frontend task에서 임의 확정한다.

## 검증

- fullstack 요청에서 이 skill이 feature delivery 오케스트레이션 진입점으로 선택되는지 확인한다.
- `dispatch_requests`가 실제 subagent 호출로 이어졌는지 확인한다.
- backend/frontend 병렬 실행 근거가 API 계약 안정성으로 설명되는지 확인한다.
- 실제 호출하지 않은 subagent를 완료로 보고하지 않았는지 확인한다.
- 보안 민감 요청과 문서/스킬 계약 변경이 실행 결과로 흡수되지 않고 blocker/open question/follow-up으로 분리됐는지 확인한다.

## 참조 Docs

- [PRD](../../../docs/PRD.md)
