---
name: feature-delivery-readiness-rules
description: 기능 전달 구현에서 기획 산출물, API 스펙, backend/frontend 병렬 위임 가능 여부를 판단하는 계약 조율 규칙. 업무 흐름과 API 계약 안정성 기준이 필요한 요청에서 사용한다.
---

# Feature Delivery Readiness Rules

## 목적

목표:

현실 업무 흐름과 API 계약을 먼저 안정화해 backend/frontend 작업을 안전하게 분리한다.

## 성공 기준

- planning 산출물이 필요한지 판단한다.
- API spec 산출물이 필요한지 판단한다.
- `stable_for_parallel` 기준으로 backend/frontend 병렬 가능 여부를 결정한다.
- 남은 API/UI/data 계약 불확실성을 추측 없이 남긴다.

## 핵심 규칙

- 업무 흐름, 정책, 상태, 화면 흐름이 비어 있으면 product planning을 먼저 둔다.
- backend API와 frontend 소비 계약이 함께 바뀌면 API spec을 먼저 둔다.
- API spec이 stable이 아니면 backend/frontend 병렬 실행 후보로 두지 않는다.
- 선행 산출물은 생산자 이름이 아니라 소비 의미로 전달한다.

## 안티패턴

- API response shape를 frontend task에서 임의 확정한다.
- planning 완료를 구현 완료로 보고한다.
- backend 결과가 frontend 입력인데 두 작업을 독립 병렬로 둔다.

## 금지사항

- 이 skill은 subagent를 호출하거나 workflow를 실행하지 않는다.
- backend/frontend 세부 구현 규칙을 포함하지 않는다.
- 계약 불확실성을 stable로 바꾸지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 Docs

- [PRD](../../../docs/PRD.md)
- [Review routing](../../../docs/review/README.md)
