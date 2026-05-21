---
name: api-contract-design-rules
description: 제품 요구사항, 업무 흐름, 도메인 상태, 화면 설계를 backend와 frontend가 공유할 수 있는 API 계약으로 구체화해야 할 때 사용하는 API contract design 규칙.
---

# API Contract Design Rules

## 목적

목표:

제품 요구사항과 화면 흐름을 backend/frontend 병렬 구현이 가능한 API 계약으로 구체화한다.

## 성공 기준

- operation id, method, path, 목적이 endpoint별로 명확하다.
- request, response, error, auth, status code가 operation 단위로 정의된다.
- 화면 상태와 API 성공, 실패, 빈 응답이 연결된다.
- backend side effect와 frontend cache invalidation 조건이 드러난다.
- 병렬 구현 가능 여부와 blocker가 operation 단위로 표시된다.

## 핵심 규칙

- API 계약은 product requirements artifact의 업무 흐름, 정책, 상태, 화면 설계를 기준으로 작성한다.
- API에 영향을 주는 open question이 남아 있으면 endpoint shape를 추측하지 않는다.
- request/response schema는 backend 보장 의미와 frontend 소비 의미를 함께 설명한다.
- 상세 산출물 구조가 필요할 때만 `references/api-spec-template.md`를 추가로 읽는다.

## 안티패턴

- frontend 편의를 위해 backend가 보장하지 않는 response shape를 확정하는 것.
- operation별 side effect, cache invalidation, error recovery를 생략하는 것.
- API spec의 `stable_for_parallel` 판단 없이 backend/frontend 병렬 구현으로 넘기는 것.

## 금지사항

- backend handler, use case, storage 구현을 이 skill의 책임으로 옮기지 않는다.
- frontend API client, query hook, component 구현을 이 skill의 책임으로 옮기지 않는다.
- subagent lifecycle, retry, scheduling, workflow orchestration을 정의하지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 자료

- [Planning artifact template](../product-requirements-planning-rules/references/planning-artifact-template.md)
- [API spec template](references/api-spec-template.md)
