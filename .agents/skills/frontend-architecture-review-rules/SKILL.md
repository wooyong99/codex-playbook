---
name: frontend-architecture-review-rules
description: 프론트엔드 변경이 architecture, conventions, performance, UI/UX 기준에 맞는지 독립 검토해야 할 때 사용하는 리뷰 규칙.
---

# Frontend Architecture Review Rules

## 목적

목표:

frontend 변경이 입력된 Source of Truth와 설계 결정에 맞는지 독립적으로 검토한다.

## 성공 기준

- 변경 파일별 pass/violation 판단이 있다.
- violation에는 rule id, severity, source path, 이유가 있다.
- blocker/major/minor가 구분된다.
- 문서에 없는 개인 선호는 violation으로 보고하지 않는다.

## 핵심 규칙

- 검토 기준은 입력으로 받은 Source of Truth에 한정한다.
- routing, component responsibility, state ownership, API/cache, performance, UI/UX 규칙을 확인한다.
- TDD 또는 설계 skip 근거와 구현 결과의 일관성을 확인한다.
- reviewer는 구현을 직접 수정하지 않는다.
- violation은 구현자가 재작업할 수 있는 단위로 작성한다.

## Violation payload

Violation에는 아래 항목을 포함한다.

- `rule_id`: 안정적인 규칙 식별자. 없으면 후보 규칙임을 명시한다.
- `severity`: `blocker`, `major`, `minor`, `info` 중 하나.
- `source_path`: 위반 근거가 되는 Source of Truth 경로.
- `line_range`: 근거 문서 또는 변경 파일의 관련 줄 범위.
- `violated_rule`: 위반한 규칙 원문 또는 체크리스트 항목.
- `affected_files`: 수정이 필요한 파일 목록.
- `reason`: 왜 위반인지에 대한 근거.
- `requested_action`: 특정 구현 방식을 강제하지 않는 수정 방향.
- `rerun_required`: 수정 후 다시 실행해야 할 검증.

## 안티패턴

- 미적 취향을 architecture violation으로 보고한다.
- Source of Truth에 없는 규칙을 근거로 blocker를 만든다.
- 브라우저 검증이 필요한 변경의 미검증 상태를 pass로 처리한다.

## 금지사항

- backend domain 또는 persistence 정책을 frontend violation 근거로 사용하지 않는다.
- 제품 요구사항 자체를 새로 정의하지 않는다.
- 접근성, 성능, 보안 민감 의심을 숨기지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 Docs

- [Frontend architecture](../../../docs/frontend/architecture/README.md)
- [Frontend conventions](../../../docs/frontend/conventions/README.md)
- [Frontend performance](../../../docs/frontend/performance/README.md)
- [Frontend UI/UX](../../../docs/frontend/ui-ux/README.md)
- [Rule metadata](../../../docs/rules/README.md)
