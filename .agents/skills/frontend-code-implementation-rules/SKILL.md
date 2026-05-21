---
name: frontend-code-implementation-rules
description: UI, route/page, component, client state, API client, query/cache 코드를 요구사항과 설계 결정에 맞게 수정하고 구현 검증 evidence를 남겨야 할 때 사용하는 구현 규칙.
---

# Frontend Code Implementation Rules

## 목적

목표:

입력된 frontend 요구사항, `frontend_design_basis`, API/UI 계약을 실제 클라이언트 코드로 옮기고 `implementation_result`를 남긴다.

## 성공 기준

- 사용자 흐름의 loading/error/empty/success 상태가 고려된다.
- 변경 파일과 변경 이유가 명확하다.
- build/test/typecheck/browser 같은 구현 검증 evidence가 있다.
- backend API 또는 infra 계약 불확실성이 분리된다.

## 핵심 규칙

- route/page, feature/entity, component, state/API/cache 책임을 섞지 않는다.
- 서버 상태, 클라이언트 상태, URL 상태, 폼 상태의 소유권을 구분한다.
- API error, loading, retry, cache invalidation을 계약 기준으로 처리한다.
- 브라우저 검증이 필요한 UI 변경은 이유 없이 생략하지 않는다.
- build/test/typecheck/browser check 실패가 있으면 구현 완료로 보고하지 않는다.

## Architecture Review 재작업 입력

`architecture_review_result` 또는 `remediation_input`이 입력되면 [Frontend stage payload contracts](../frontend-stage-payload-contracts.md)의 필드를 기준으로 처리한다.

- violation payload의 근거와 수정 범위를 먼저 확인한다.
- `requested_action` 범위 안에서만 수정하고, 새 UI/API/state 설계 결정을 임의로 만들지 않는다.
- 수정 후 `rerun_required`에 적힌 build/test/typecheck/browser check를 다시 실행한다.
- 같은 위반이 해결되지 않거나 설계 결정 충돌이 의심되면 구현 완료로 보고하지 않고 불확실성으로 반환한다.

## 안티패턴

- API response shape를 UI에서 임의로 만든다.
- 공통 컴포넌트 계약을 기능 화면 편의로 깨뜨린다.
- build 통과만으로 접근성, 반응형, 상호작용 검증을 대체한다.

## 금지사항

- architecture pass 여부를 직접 확정하지 않는다.
- architecture review나 security review를 구현 검증 evidence로 대체하지 않는다.
- backend persistence 정책을 frontend 코드에 숨겨 넣지 않는다.
- 입력에 없는 화면 또는 디자인 체계를 불필요하게 바꾸지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 Docs

- [Frontend docs](../../../docs/frontend/README.md)
- [Frontend architecture](../../../docs/frontend/architecture/README.md)
- [Frontend conventions](../../../docs/frontend/conventions/README.md)
- [Frontend UI/UX](../../../docs/frontend/ui-ux/README.md)
- [Frontend stage payload contracts](../frontend-stage-payload-contracts.md)
