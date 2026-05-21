---
name: backend-architecture-review-rules
description: 백엔드 변경이 architecture boundary, dependency direction, policy, TDD 결정에 맞는지 독립 검토해야 할 때 사용하는 리뷰 규칙.
---

# Backend Architecture Review Rules

## 목적

목표:

backend 변경이 입력된 Source of Truth, `backend_design_basis`, `implementation_result`에 맞는지 독립적으로 검토한다.

## 성공 기준

- 변경 파일별 pass/violation 판단이 있다.
- violation에는 rule id, severity, source path, 이유가 있다.
- blocker/major/minor가 구분된다.
- 문서에 없는 개인 선호는 violation으로 보고하지 않는다.

## 핵심 규칙

- 검토 기준은 입력으로 받은 Source of Truth에 한정한다.
- 기본 Source of Truth 후보는 docs/backend/architecture/**, docs/backend/policies/**, 관련 `backend_design_basis`다.
- architecture boundary, dependency direction, transaction, security, logging 정책을 확인한다.
- `backend_design_basis`와 `implementation_result`의 일관성을 확인한다.
- architecture review stage는 구현을 직접 수정하지 않는다.
- violation은 후속 remediation input으로 사용할 수 있는 단위로 작성한다.

## Violation payload

Violation payload는 [Backend stage payload contracts](../backend-stage-payload-contracts.md)를 따른다.

## 안티패턴

- 코드 스타일 취향을 architecture violation으로 보고한다.
- Source of Truth에 없는 규칙을 근거로 blocker를 만든다.
- implementation evidence를 확인하지 않고 pass 처리한다.

## 금지사항

- 제품 요구사항 자체를 새로 정의하지 않는다.
- frontend UI 규칙을 backend violation 근거로 사용하지 않는다.
- 보안 민감 의심을 숨기지 않는다. 필요하면 blocker 또는 open question으로 분리한다.
- 문서 구조, 스킬, 서브에이전트 계약 변경을 backend architecture violation으로 확장하지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 Docs

- [Backend architecture](../../../docs/backend/architecture/README.md)
- [Backend policies](../../../docs/backend/policies/README.md)
- [Rule metadata](../../../docs/rules/README.md)
- [Backend stage payload contracts](../backend-stage-payload-contracts.md)
