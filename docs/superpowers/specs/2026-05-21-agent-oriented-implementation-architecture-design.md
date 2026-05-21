# Agent-Oriented Implementation Architecture Design

## 목적

구현 playbook을 `feature orchestration skill -> delivery engineer subagent -> rule skill -> docs` 구조로 정리한다.

## 목표

- backend, frontend 요청에는 의미 있는 delivery engineer subagent가 선택된다.
- feature delivery 요청에는 하위 subagent들을 오케스트레이션하는 skill이 선택된다.
- delivery engineer subagent는 자기 단계의 작업 규약 skill을 사용한다.
- skill은 목표, 성공 기준, 핵심 규칙, 안티패턴, 금지사항만 담는 짧은 context package가 된다.
- docs는 durable knowledge만 소유하고 실행 흐름을 알지 않는다.

## 성공 기준

- backend 요청: `backend-delivery-engineer`가 기술 설계, 코드 구현, 아키텍처 리뷰를 수행한다.
- frontend 요청: `frontend-delivery-engineer`가 기술 설계, 코드 구현, 아키텍처 리뷰를 수행한다.
- feature delivery 요청: `feature-delivery-orchestration-rules`가 product planning, API contract, backend/frontend delivery engineer 호출을 조율한다.
- broad `implement*` skill은 제거되고 역할별 `*-rules` skill로 대체된다.
- 기술설계 스킬은 `backend-technical-design-writing-rules`, `frontend-technical-design-writing-rules`처럼 실행이 아니라 작업 규칙을 나타낸다.
- 기획과 API 계약 스킬은 `product-requirements-planning-rules`, `api-contract-design-rules`처럼 작업 규칙을 나타낸다.

## 핵심 규칙

- Orchestrator는 workflow를 소유한다.
- Delivery subagent는 실제 작업과 리뷰를 수행한다.
- Skill은 작업 규약과 판단 기준만 제공한다.
- Docs는 project knowledge만 제공한다.
- 네이밍은 책임을 드러내야 한다.

## 안티패턴

- `implement-backend`처럼 skill 이름이 실행 workflow를 소유하는 것처럼 보이는 구조.
- 하나의 generic coordinator가 backend/frontend/feature delivery 의미를 모두 흐리는 구조.
- skill 문서에 subagent lifecycle, retry, scheduling을 넣는 구조.
- docs가 특정 subagent 호출 흐름을 설명하는 구조.

## 금지사항

- skill이 다른 skill이나 subagent를 호출한다고 작성하지 않는다.
- delivery engineer subagent가 feature 전체 workflow를 조율하지 않는다.
- feature orchestration skill이 domain code를 직접 수정하지 않는다.
- API 계약이 불안정한 feature delivery 작업을 병렬 구현으로 보지 않는다.
