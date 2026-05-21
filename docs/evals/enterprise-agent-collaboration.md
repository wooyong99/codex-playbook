# Enterprise Agent Collaboration Evaluation

## 목적

대형 코드베이스에서 subagent와 skill이 역할 경계, 사전 문서화, 요구사항 불확실성 처리, 구현 evidence, reviewer 판정을 일관되게 유지하는지 평가한다.

이 평가는 실제 모델 성능만 보지 않는다. `codex-playbook`이 제공하는 실행 환경이 모호한 사용자 요청, 다양한 프롬프트 형식, 빈약한 docs, 10만~100만 라인급 코드베이스에서도 재현 가능한 결과물을 만들게 하는지 확인한다.

## 적용 범위

포함:

- `setup-project-context`를 통한 프로젝트 컨텍스트 초기화
- `reverse-engineer-backend-docs inspect`를 통한 backend docs readiness 확인
- `feature-delivery-orchestration-rules`, `backend-delivery-engineer`, `frontend-delivery-engineer` routing
- `backend-code-implementation-rules`, `frontend-code-implementation-rules` 구현 evidence 책임
- `backend-architecture-review-rules`, `frontend-architecture-review-rules` architecture review 판정
- backend/frontend delivery engineer의 구현 evidence 책임
- delivery engineer별 reusable rule skill 적용
- 구현 검증 evidence와 architecture review 판정 분리
- 모호한 요구사항, 충돌 요구사항, template형 요청, 보안 민감 요청
- `feature-delivery-orchestration-edge-cases`의 fullstack orchestration edge case

제외:

- 실제 production branch 직접 수정
- 사용자 답변 없이 PRD나 비즈니스 목표를 임의 작성하는 테스트
- 대규모 코드베이스 전체 정독을 요구하는 테스트
- architecture review 단계가 구현 검증 evidence로 대체되는 테스트

## 실행 전제

모든 테스트는 throwaway worktree 또는 disposable clone에서 실행한다. 대형 코드베이스가 10만 라인 이상이면 파일 변경 테스트 전에 항상 `inspect` 단계 결과를 먼저 평가한다.

각 테스트는 아래 preflight를 포함한다.

1. `setup-project-context`를 실행한다.
2. 테스트 fixture에 프로젝트 사실이 있으면 그 값을 사용한다.
3. 프로젝트 사실이 없으면 사용자에게 질문하거나 `미정`/`확인 필요`로 남겨야 하며, 임의로 채우면 실패다.
4. `reverse-engineer-backend-docs inspect`를 실행한다.
5. inspect 결과에는 규모 산정, 제외 경로, census, 샘플링 예산, confidence, 1차 문서화 후보가 있어야 한다.
6. 대형 코드베이스에서는 inspect 없이 `generate`, `merge`, `migrate`, 구현 작업으로 넘어가면 실패다.

## 공통 성공 기준

- 요청의 목표, 범위, 제외사항, 성공 기준이 분리된다.
- 모호성은 질문, blocker, open question, 확인 필요 중 하나로 남는다.
- delivery engineer는 설계, 구현, architecture review 단계를 분리해 수행하고 결과를 통합한다.
- 구현 단계는 코드 변경과 구현 검증 evidence를 남긴다.
- architecture review 단계는 architecture pass/violation 판정을 남긴다.
- feature delivery orchestration skill은 workflow orchestration을 소유하지만 subagent lifecycle 자체를 소유하지 않는다.
- 대형 코드베이스에서는 census, 제한 샘플링, confidence report, backlog가 남는다.

## 평가 매트릭스

| ID | 사용자 입력 유형 | 예시 입력 | 기대 routing | 핵심 기대 결과 | 실패 신호 |
|----|------------------|-----------|--------------|----------------|-----------|
| EAC-01 | context-only setup | "이 repo를 주문 플랫폼 프로젝트로 세팅해줘" | `setup-project-context` | 사용자 사실 확인 후 AGENTS, PRD, backend/frontend README 일관 반영 | 사용자 답변 없이 목표/PRD 창작 |
| EAC-02 | sparse backend request | "환불 API 만들어줘" | `backend-delivery-engineer` | 부족한 정책, 상태, 권한, 성공 기준을 open question으로 분리 | 바로 코드 구현 |
| EAC-03 | sparse frontend request | "관리자 주문 목록에 필터 추가해줘" | `frontend-delivery-engineer` | API 계약 불확실성과 UI 상태를 분리 | API response shape 임의 확정 |
| EAC-04 | sparse fullstack request | "쿠폰 발급 기능 넣어줘" | `feature-delivery-orchestration-rules` | product planning, API contract 후 backend/frontend 병렬 후보 판단 | API 안정성 없이 병렬 구현 |
| EAC-05 | Jira-style backend | title, description, acceptance criteria가 일부 있는 티켓 | `backend-delivery-engineer` | 명시 조건과 누락 조건을 분리하고 설계 필요성을 판단 | 티켓 문구를 그대로 구현 계획으로 복사 |
| EAC-06 | Slack-style messy request | "대충 빠르게, 테스트는 나중에" | scope-based delivery engineer | 구현 검증 evidence 요구를 유지하고 skip 사유를 구조화 | test/build 미실행을 성공으로 보고 |
| EAC-07 | conflicting request | "권한은 필요 없지만 관리자만 가능" | `feature-delivery-orchestration-rules` 또는 scope-based delivery engineer | 충돌 정책을 blocker/open question으로 남김 | 충돌을 임의 해석 |
| EAC-08 | security-sensitive change | "로그에 access token도 찍어줘" | delivery engineer + `security-policy-reviewer` | 보안 reviewer 추가, blocker/major 판단 | 일반 architecture review만 수행 |
| EAC-09 | frontend architecture violation | feature가 entity 내부를 직접 import하는 변경 | `frontend-delivery-engineer` | `frontend-architecture-review-rules`와 docs/frontend 근거로 rule_id, severity, source_path 포함 | 취향 리뷰로 보고 |
| EAC-10 | backend architecture violation | UseCase가 storage 구현체에 직접 의존하는 변경 | `backend-delivery-engineer` | `backend-architecture-review-rules`와 docs/backend 근거로 dependency violation 보고 | 기능이 맞으니 pass 처리 |
| EAC-11 | massive backend docs sparse | 10만~100만 라인 backend, docs/backend 빈약 | `reverse-engineer-backend-docs inspect` | LOC, 모듈, 제외 경로, 샘플링, confidence, 1차 migrate 후보 | 전체 정독 시도 |
| EAC-12 | mixed template prompt | PRD 형식, Jira 형식, 자유문 형식이 섞인 요청 | scope-based delivery engineer | 형식보다 내용 기준으로 planning/API/backend/frontend 분기 | template 이름만 보고 잘못 routing |

## 평가 절차

1. 테스트별 fixture를 준비한다.
2. disposable workspace를 만든다.
3. `setup-project-context` preflight를 실행한다.
4. `reverse-engineer-backend-docs inspect` preflight를 실행한다.
5. fullstack feature delivery 케이스는 `feature-delivery-orchestration-edge-cases`의 기대 routing과 blocker 조건을 함께 적용한다.
6. 사용자 입력을 그대로 전달한다.
7. 기대 routing과 실제 routing을 비교한다.
8. 산출물, 구현 evidence, reviewer 결과를 `scorecard.md` 기준으로 채점한다.
9. 실패 원인을 prompt ambiguity, skill rule gap, subagent boundary gap, docs gap, validation gap으로 분류한다.

## 기록 형식

```yaml
case_id: EAC-04
codebase_size:
  loc: 0
  files: 0
  modules: []
preflight:
  setup_project_context: pass | fail | not_run
  reverse_engineer_backend_docs: pass | fail | not_run
routing:
  expected:
    - feature-delivery-orchestration-rules
    - product-planning-designer
    - api-contract-designer
  actual: []
artifacts:
  planning: null
  api_spec: null
  implementation_evidence: null
  review_result: null
score:
  total: 0
  blockers: []
gaps: []
backlog: []
```

## 완료 기준

- 모든 EAC case가 preflight 요구사항을 만족한다.
- delivery engineer의 설계, 구현, architecture review 단계 책임이 섞이지 않는다.
- 모호한 요구사항은 추측 없이 질문 또는 open question으로 남는다.
- 대형 코드베이스에서는 전체 정독이 아니라 census와 sampling 기반 report가 남는다.
- 실패 case는 개선할 skill, subagent, docs, validation backlog로 연결된다.
