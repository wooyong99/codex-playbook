---
name: backend-code-implementation-rules
description: 백엔드 코드를 요구사항과 설계 결정에 맞게 수정하고 compile/test/typecheck 같은 구현 검증 evidence를 남겨야 할 때 사용하는 구현 규칙.
---

# Backend Code Implementation Rules

## 목적

목표:

입력된 backend 요구사항과 설계 결정을 실제 코드 변경으로 옮기고 구현 검증 evidence를 남긴다.

## 성공 기준

- 변경 파일과 변경 이유가 명확하다.
- Source of Truth와 설계 결정이 구현에 반영된다.
- compile/test/typecheck 같은 구현 검증 evidence가 있다.
- frontend 또는 infra로 넘길 계약 불확실성이 분리된다.

## 핵심 규칙

- 요구사항과 명시적 제외사항 밖으로 범위를 넓히지 않는다.
- domain, application, storage, external, app 계층 책임을 섞지 않는다.
- transaction, consistency, exception, security 정책을 docs 기준으로 보존한다.
- compile/test/typecheck 실패가 있으면 구현 완료로 보고하지 않는다.

## 안티패턴

- 설계 산출물의 결정과 다른 구조로 구현한다.
- 테스트를 맞추기 위해 domain policy를 우회한다.
- frontend 표시 편의를 backend domain 책임으로 끌어온다.

## 금지사항

- architecture pass 여부를 직접 확정하지 않는다.
- architecture review나 security review를 구현 검증 evidence로 대체하지 않는다.
- 입력에 없는 파일을 불필요하게 수정하지 않는다.
- secret, token, credential을 코드나 로그에 남기지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 Docs

- [Backend docs](../../../docs/backend/README.md)
- [Backend architecture](../../../docs/backend/architecture/README.md)
- [Backend policies](../../../docs/backend/policies/README.md)
