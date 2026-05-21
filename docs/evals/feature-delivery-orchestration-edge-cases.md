# Feature Delivery Orchestration Edge Cases

## 목적

`feature-delivery-orchestration-rules`가 대형 코드베이스와 빈약한 docs 조건에서도 하위 subagent를 일관되게 조율하는지 평가한다.

이 평가는 기능 구현 결과 자체보다 orchestration 판단을 본다. 특히 `setup-project-context` 선행 실행, API 계약 안정성, backend/frontend 병렬 실행, `dispatch_requests` 처리, 보안 민감 변경 차단이 일관되는지 확인한다.

## 적용 범위

포함:

- 10만~100만 라인 규모 코드베이스
- docs 하위 문서가 빈약한 저장소
- sparse prompt, PRD template, Jira-style, Slack-style, conflicting request, security-sensitive request
- `feature-delivery-orchestration-rules`, `product-planning-designer`, `api-contract-designer`, `backend-delivery-engineer`, `frontend-delivery-engineer` routing

제외:

- 실제 production 코드 수정 품질
- 특정 모델의 자연어 답변 선호도
- 사용자 답변 없이 `setup-project-context`가 PRD를 임의 작성하는 흐름

## 테스트 전제

모든 케이스는 아래 preflight를 먼저 적용한다.

1. `setup-project-context`를 실행한다.
2. 프로젝트 사실이 fixture에 있으면 그 값을 사용한다.
3. 프로젝트 사실이 없거나 부분적이면 질문 또는 `setup_project_context_incomplete` blocker로 남기고 구현으로 넘어가지 않는다.
4. 코드베이스가 10만 라인 이상이거나 docs가 빈약하면 `reverse-engineer-backend-docs inspect`를 실행한다.
5. inspect 없이 backend/frontend 구현 subagent를 호출하면 fail이다.

## 평가 기준

- `setup-project-context`가 모든 테스트의 첫 preflight 단계로 나타난다.
- API 계약이 `stable_for_parallel`일 때만 backend/frontend 병렬 실행을 허용한다.
- API 계약이 unknown, partial, conflicting이면 `api-contract-designer` 이후 구현 호출을 보류한다.
- 업무 흐름, 정책, 상태, 화면 흐름이 비어 있으면 `product-planning-designer`를 먼저 둔다.
- `dispatch_requests`는 실행 결과가 아니라 실제 subagent 호출 요청으로 다룬다.
- 보안 민감 요청은 `security-policy-reviewer`를 추가하고 blocker/major 판단을 분리한다.
- 최종 결과는 `orchestration_result` schema를 따르고, 실제 호출하지 않은 subagent는 `dispatch.executed`에 넣지 않는다.
- 하위 subagent가 반환한 `dispatch_requests`는 `target_agent`, `reason`, `input_artifacts`, `parallel_allowed`, `return_to`를 포함한다.

## 케이스 매트릭스

| ID | Prompt style | 예시 입력 | LOC | 기대 routing | 병렬 | 핵심 기대 |
|----|--------------|-----------|-----|--------------|------|-----------|
| FDO-01 | sparse-fullstack | "쿠폰 발급 기능 넣어줘" | 250k | `feature-delivery-orchestration-rules` -> `product-planning-designer` -> `api-contract-designer` | no | API 계약 불안정으로 backend/frontend 구현 보류 |
| FDO-02 | prd-template | PRD에 stable API request/response 포함 | 420k | `feature-delivery-orchestration-rules` -> `backend-delivery-engineer` + `frontend-delivery-engineer` | yes | stable API 계약 근거로 병렬 실행 |
| FDO-03 | jira-style | 환불 승인 화면/API, acceptance criteria 일부 누락 | 610k | `feature-delivery-orchestration-rules` -> `product-planning-designer` -> `api-contract-designer` | no | 권한 정책과 API shape open question |
| FDO-04 | slack-style | "대충 빠르게... 테스트는 나중에" | 180k | `feature-delivery-orchestration-rules` -> `backend-delivery-engineer` + `frontend-delivery-engineer` | yes | 구현 검증 evidence 요구 유지 |
| FDO-05 | conflicting-policy | "권한 체크는 필요 없지만 관리자만 가능" | 350k | `feature-delivery-orchestration-rules` -> `product-planning-designer` -> `api-contract-designer` | no | 정책 충돌 blocker |
| FDO-06 | security-sensitive | token을 화면과 로그에 노출 | 720k | `feature-delivery-orchestration-rules` -> `security-policy-reviewer` | no | 보안 blocker, 일반 architecture review로 대체 금지 |
| FDO-07 | dispatch-loop | 하위 subagent가 `dispatch_requests` 반환 | 510k | `feature-delivery-orchestration-rules` -> backend/frontend engineers -> `dispatch_requests` | yes | dispatch 요청을 실제 호출로 실행 |
| FDO-08 | frontend-shape-guess | "응답 shape는 알아서 맞춰" | 230k | `feature-delivery-orchestration-rules` -> `api-contract-designer` | no | frontend가 API response shape 임의 확정 금지 |
| FDO-09 | sequential-dependency | backend schema 확정 후 frontend 적용 | 890k | `feature-delivery-orchestration-rules` -> `backend-delivery-engineer` | no | frontend는 backend output 대기 |
| FDO-10 | missing-project-facts | 프로젝트 사실 없이 기능 요청 | 300k | `setup-project-context` preflight only | no | 프로젝트 사실 질문 또는 blocker |
| FDO-11 | massive-codebase | 100만 라인급 기존 패턴 기반 기능 추가 | 1,000k | `feature-delivery-orchestration-rules` -> backend/frontend engineers | yes | inspect, sampling, confidence 선행 |
| FDO-12 | mixed-template | PRD+Jira+자유문 혼합 요청 | 470k | `feature-delivery-orchestration-rules` -> `product-planning-designer` -> `api-contract-designer` | no | template 이름보다 내용 기준 routing |

## 실행 검증

아래 스크립트가 이 문서와 케이스 계약을 검증한다.

```bash
python3 .agents/scripts/validate-feature-delivery-orchestration-evals.py
```

검증 통과 조건:

- 최소 12개 케이스가 존재한다.
- 모든 케이스가 10만~100만 LOC 범위 안에 있다.
- 모든 케이스가 `setup-project-context` preflight를 갖는다.
- sparse docs 또는 대형 코드베이스 케이스가 `reverse-engineer-backend-docs inspect`를 요구한다.
- API 불안정 케이스가 backend/frontend 구현을 dispatch하지 않는다.
- stable API 케이스만 `stable_for_parallel` 근거로 병렬 실행을 허용한다.
- 결과에 `orchestration_result`와 `dispatch_requests` 계약이 드러난다.
