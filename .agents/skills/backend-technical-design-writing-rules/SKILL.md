---
name: backend-technical-design-writing-rules
description: 백엔드 구현 전에 아키텍처 판단, 계층 책임, 트랜잭션, 정합성, 실패 처리, 동시성, 검증 계획을 기술설계문서로 정리해야 할 때 사용하는 작성 규칙.
---

# Backend Technical Design Writing Rules

## 목적

목표:

backend 변경의 설계 판단을 `backend_design_basis` payload와 필요한 기술설계문서로 정리한다.

## 성공 기준

- `backend_design_basis`에 설계 범위와 제외 범위가 명확하다.
- 아키텍처 판단과 계층 책임 분리가 근거와 함께 설명된다.
- 트랜잭션, 정합성, 실패 처리, 동시성, 검증 계획이 필요한 수준으로 다뤄진다.
- 새 설계 문서가 생기면 `docs/backend/design/README.md` 문서 맵이 갱신된다.

## 핵심 규칙

- 확인한 `docs/backend/**`와 실제 backend 코드만 설계 근거로 사용한다.
- 각 주요 결정에는 선택 이유와 대안을 함께 남긴다.
- UseCase, domain, application, storage, external, app 계층 책임을 분리해 설명한다.
- 상세 절차나 템플릿이 필요할 때만 `references/backend-tdd-workflow.md`와 `references/backend-tdd-template.md`를 추가로 읽는다.

## 안티패턴

- 구현 순서를 장황하게 나열하고 설계 판단을 비워두는 것.
- 저장소에서 확인되지 않은 architecture rule을 임의로 추가하는 것.
- 단순 변경에 과도한 TDD를 작성해 delivery 흐름을 막는 것.

## 금지사항

- frontend 상태, routing, component 설계를 backend TDD에 포함하지 않는다.
- code implementation이나 architecture review를 이 skill의 책임으로 옮기지 않는다.
- subagent lifecycle, retry, scheduling, workflow orchestration을 정의하지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 자료

- [Backend docs](../../../docs/backend/README.md)
- [Backend architecture](../../../docs/backend/architecture/README.md)
- [Backend design docs](../../../docs/backend/design/README.md)
- [Backend stage payload contracts](../backend-stage-payload-contracts.md)
- [Reference map](references/reference-map.md)
- [Detailed workflow](references/backend-tdd-workflow.md)
- [TDD template](references/backend-tdd-template.md)
