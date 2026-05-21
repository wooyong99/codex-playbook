---
name: frontend-technical-design-writing-rules
description: 프론트엔드 구현 전에 사용자 흐름, route, component, state, API, cache, error, browser 검증 계획을 기술설계문서로 정리해야 할 때 사용하는 작성 규칙.
---

# Frontend Technical Design Writing Rules

## 목적

목표:

frontend 변경의 설계 판단을 `frontend_design_basis` payload와 필요한 기술설계문서로 정리한다.

## 성공 기준

- `frontend_design_basis`에 설계 범위와 제외 범위가 명확하다.
- 사용자 흐름, route, component 책임, state 소유권이 설명된다.
- API, cache, loading/error, 접근성, 반응형, browser 검증 계획이 필요한 수준으로 다뤄진다.
- 새 설계 문서가 생기면 `docs/frontend/design/README.md` 문서 맵이 갱신된다.

## 핵심 규칙

- 확인한 `docs/frontend/**`, API 계약, 실제 frontend 코드만 설계 근거로 사용한다.
- state는 server, client, form, URL, derived state로 구분한다.
- API 연동은 타입, hook/client, loading/error, invalidation 기준까지 포함한다.
- 상세 절차나 템플릿이 필요할 때만 `references/frontend-tdd-workflow.md`와 `references/frontend-tdd-template.md`를 추가로 읽는다.

## 안티패턴

- API response shape를 추측해 frontend 설계에서 확정하는 것.
- component 구조만 나열하고 사용자 흐름과 상태 소유권을 비워두는 것.
- build 통과를 browser, 접근성, 반응형 검증 계획으로 대체하는 것.

## 금지사항

- backend persistence, transaction, domain policy 설계를 frontend TDD에 포함하지 않는다.
- code implementation이나 architecture review를 이 skill의 책임으로 옮기지 않는다.
- subagent lifecycle, retry, scheduling, workflow orchestration을 정의하지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 자료

- [Frontend docs](../../../docs/frontend/README.md)
- [Frontend architecture](../../../docs/frontend/architecture/README.md)
- [Frontend design docs](../../../docs/frontend/design/README.md)
- [Frontend stage payload contracts](../frontend-stage-payload-contracts.md)
- [Reference map](references/reference-map.md)
- [Detailed workflow](references/frontend-tdd-workflow.md)
- [TDD template](references/frontend-tdd-template.md)
