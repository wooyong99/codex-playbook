---
name: product-requirements-planning-rules
description: 구현 또는 리팩토링 전에 업무 흐름, 도메인 구조, 정책, 상태, 화면 설계, 인수 기준을 구체화해야 할 때 사용하는 product requirements planning 규칙.
---

# Product Requirements Planning Rules

## 목적

목표:

사용자 요청을 구현 가능한 제품 요구사항, 업무 흐름, 정책, 상태, 화면 설계, 인수 기준으로 구체화한다.

## 성공 기준

- 목표, 범위, 제외사항, 성공 기준이 분리된다.
- 업무 흐름과 상태 전이가 구현 가능한 수준으로 정의된다.
- 정책이 업무, 권한, 검증, 운영, 예외 정책으로 구분된다.
- 화면 설계가 진입점, 주요 액션, 상태별 피드백을 포함한다.
- API 계약 설계에 필요한 command, query, event 후보와 데이터 의미가 드러난다.

## 핵심 규칙

- 구현 범위가 바뀔 수 있는 질문은 추측하지 않고 open question으로 남긴다.
- 낮은 위험의 문구, 버튼명, 내부 파일명은 후속 설계로 넘긴다.
- 현실 업무 흐름과 시스템 상태 전이를 분리해 설명한다.
- 상세 산출물 구조가 필요할 때만 `references/planning-artifact-template.md`를 추가로 읽는다.

## 안티패턴

- 요구사항이 모호한데 바로 API 계약이나 코드 구현으로 넘기는 것.
- 제품 정책, 권한 정책, 검증 정책, 운영 정책을 한 문장으로 뭉개는 것.
- 화면 상태를 success 중심으로만 보고 loading, empty, error, 권한별 차이를 빠뜨리는 것.

## 금지사항

- backend/frontend 기술설계나 코드 구현을 이 skill의 책임으로 옮기지 않는다.
- API endpoint, DTO, error shape를 이 단계에서 최종 확정하지 않는다.
- subagent lifecycle, retry, scheduling, workflow orchestration을 정의하지 않는다.

## 검증

- skill frontmatter가 현재 책임과 일치하는지 확인한다.
- 참조 docs 링크가 실제 파일을 가리키는지 확인한다.
- 이 skill에 orchestration, subagent lifecycle, scheduling 책임이 들어오지 않았는지 확인한다.

## 참조 자료

- [PRD](../../../docs/PRD.md)
- [Planning artifact template](references/planning-artifact-template.md)
