---
name: write-frontend-tech-design-doc
description: 프론트엔드 기술설계문서(TDD)를 작성하는 스킬. 상태관리 구조, API 연동 방식, 컴포넌트 구조, 라우팅, 캐싱 전략, 에러 처리, 폴더 구조를 포함한 frontend 설계 문서가 필요할 때 사용한다. 신규 화면/기능 설계, 프론트엔드 리팩토링 설계, React/Vue/Svelte 등 클라이언트 앱의 상태/API/cache/component/routing 설계가 필요한 요청에서 사용한다.
---

# write-frontend-tech-design-doc — 프론트엔드 기술설계문서 작성

## 목적

프론트엔드 기능 구현 전 기술설계문서(TDD)를 작성한다.

문서는 "무엇을 만들지"보다 "상태, API, 컴포넌트, 라우팅, 캐싱, 에러 처리를 왜 이렇게 구성하는지"에 집중한다. 실제 프로젝트 문서와 코드에서 확인한 사실만 근거로 삼는다.

## 적용 범위

포함:

- 신규 화면, 기능, 사용자 흐름의 frontend 설계
- 상태관리, API client/hook, component, routing, caching, error handling, folder structure 설계
- React, Vue, Svelte 등 client application의 변경 전 설계
- frontend 구현자와 reviewer가 공유할 수 있는 설계 근거 문서

제외:

- backend 내부 구현 설계
- 확인되지 않은 API 계약을 추측해 확정하는 작업
- 단순 copy, label 변경처럼 별도 frontend 설계 판단이 거의 없는 작업
- 실제 코드 구현 절차를 TDD 안에 장황하게 나열하는 작업

## 운영 모델

```text
설계 대상 고정
  -> 현재 frontend 문서와 코드 근거 수집
  -> 사용자 흐름, routing, component 책임 정리
  -> 상태, API, cache, error, UX 판단 도출
  -> TDD 문서 저장 또는 기존 문서 갱신
  -> 문서 맵과 산출물 검증
```

## 참조 문서

- [references/README.md](references/README.md): 이 스킬의 참조 문서 맵
- [frontend-tdd-workflow.md](references/frontend-tdd-workflow.md): 설계 대상 식별부터 저장까지의 상세 흐름
- [frontend-tdd-template.md](references/frontend-tdd-template.md): 최종 TDD 구조와 섹션별 작성 기준

## 작업 흐름

1. 설계 대상 기능 또는 리팩토링 범위를 한 문장으로 고정한다.
2. 사용자 흐름, 진입 route, 주요 화면, API 계약, 상태 범위, 성능/UX 제약을 확인한다.
3. [frontend-tdd-workflow.md](references/frontend-tdd-workflow.md)에 따라 필요한 frontend 문서와 코드를 선별해 읽는다.
4. 확인된 근거로 routing, component, state, API, cache, error 처리 판단을 정리한다.
5. [frontend-tdd-template.md](references/frontend-tdd-template.md)의 섹션 구조를 기준으로 TDD를 작성한다.
6. 새 문서를 만들면 `docs/frontend/design/README.md` 문서 맵을 갱신한다.

## 작성 원칙

- 상태는 server state, client state, form state, URL state, derived state로 분류한다.
- API 연동은 endpoint 나열이 아니라 타입, hook, loading/error, invalidation까지 포함한다.
- 컴포넌트 구조는 책임과 데이터 흐름을 보여야 한다.
- 라우팅은 route, layout, guard, redirect, URL state를 포함한다.
- 캐싱 전략은 query key, stale policy, invalidation, optimistic update 여부를 포함한다.
- 에러 처리는 사용자 피드백과 복구 전략까지 포함한다.
- 폴더 구조는 프로젝트의 실제 architecture 문서를 우선한다.
- 문서에 없는 프레임워크나 라이브러리를 임의로 도입하지 않는다.

## 검증

- 상태관리 구조가 server/client/form/url/derived 기준으로 분류되었다.
- API 연동 방식이 타입, hook, loading/error, invalidation까지 설명한다.
- 컴포넌트 구조가 책임 분리와 public API 경계를 포함한다.
- 라우팅과 URL state가 명시되었다.
- 캐싱 전략과 에러 처리가 사용자 경험과 연결되었다.
- 폴더 구조가 `docs/frontend/architecture/**`와 충돌하지 않는다.
- 검증 계획이 unit/integration/e2e/browser/manual 중 필요한 방식을 포함한다.
- 가능하면 구조 검증을 수행한다.

```bash
python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py .agents/skills/write-frontend-tech-design-doc/SKILL.md .agents/skills/write-frontend-tech-design-doc/references/*.md
```

## 완료 기준

완료 응답에는 작성 또는 갱신한 TDD 경로, 설계 범위, 주요 frontend 설계 판단, 남은 확인 필요 사항을 함께 보고한다.
