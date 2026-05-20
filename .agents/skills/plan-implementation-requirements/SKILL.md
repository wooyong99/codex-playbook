---
name: plan-implementation-requirements
description: 사용자 구현·리팩토링 요청을 업무 흐름, 업무 프로세스, 도메인 구조, 정책, 상태, 화면 설계, 인수 기준으로 구체화하는 스킬. 요구사항이 빈약하거나 모호해 구현 범위·정책·화면 흐름·도메인 상태를 안전하게 확정할 수 없을 때 질문으로 보강하고, `implement` 또는 API 스펙 작성 전에 기획 산출물이 필요할 때 사용한다.
---

# Plan Implementation Requirements

## 목적

`plan-implementation-requirements`는 구현 전에 사용자의 요구를 현실 업무 흐름과 시스템 흐름으로 추상화한다.

이 스킬은 코드 구현을 수행하지 않는다. 구현자가 바로 설계와 API 스펙으로 이어갈 수 있도록 업무 흐름, 정책, 상태, 화면, 도메인 구조, 인수 기준을 일관된 artifact로 고정한다.

이 스킬은 `product-planning-designer`가 직접 로드하는 역할 지침이 아니라, 메인 오케스트레이터가 `product-planning-designer`를 호출할 때 사용하는 workflow, input/output 계약, checkpoint schema의 단일 출처다.

## 적용 대상

포함:

- 구현 또는 리팩토링 요구사항이 업무 정책, 상태 전이, 화면 흐름, API 계약에 영향을 주는 경우
- 사용자의 설명이 짧거나 모호해 구현 전에 질문이 필요한 경우
- fullstack 구현 전에 backend/frontend 공통 기준이 되는 기획 산출물이 필요한 경우
- 기존 PRD보다 더 작은 기능 단위의 실행 가능한 요구사항 정의가 필요한 경우

제외:

- 코드 구현, 테스트 작성, 파일 수정 자체
- backend/frontend 기술설계 세부화
- OpenAPI 또는 endpoint 단위 API 스펙 작성

API 스펙은 이 스킬의 기획 산출물을 입력으로 `write-api-spec`가 작성한다.

## 참조 문서

- 기획자 서브에이전트 계약: [references/product-planning-designer-contract.md](references/product-planning-designer-contract.md)
- 기획 산출물 템플릿: [references/planning-artifact-template.md](references/planning-artifact-template.md)

## 작업 흐름

### 1. 요구사항 밀도를 판정한다

- 사용자 요청을 한 문장 목표로 재진술한다.
- 요구사항, 명시적 제외사항, 성공 기준, 관련 사용자 유형을 분리한다.
- 구현에 필요한 업무 정책, 상태 전이, 화면 흐름, 데이터 의미 중 비어 있는 축을 찾는다.
- 아래 항목 중 하나라도 비어 있고 추측하면 구현 범위가 달라지는 경우에는 artifact 작성 전에 사용자에게 질문한다.

질문이 필요한 조건:

- 누가 어떤 권한으로 기능을 쓰는지 불명확하다.
- 업무 시작 조건, 종료 조건, 취소·반려·재시도 흐름이 불명확하다.
- 상태 이름, 상태 전이 조건, 실패 시 복구 방식이 불명확하다.
- 화면 진입점, 주요 액션, 성공·실패 피드백이 불명확하다.
- 정책이 제품 판단인지 기술 판단인지 구분되지 않는다.
- 데이터 보존, 감사, 권한, 알림, 외부 연동 같은 운영 정책이 기능 결과에 영향을 준다.

질문 규칙:

- 한 번에 3~7개 이하의 결정 질문만 한다.
- 구현자가 임의로 정하면 위험한 질문만 남긴다.
- 낮은 위험의 세부 표현, 버튼 문구, 내부 파일명은 질문하지 않고 후속 설계로 넘긴다.

### 2. 업무 흐름과 도메인을 모델링한다

메인 오케스트레이터는 [product-planning-designer-contract.md](references/product-planning-designer-contract.md)에 따라 input artifact를 만들고 `product-planning-designer` 서브에이전트를 호출한다.

호출 프롬프트에는 입력 파일 경로와 계약 파일 경로만 전달한다. `product-planning-designer` TOML에는 이 스킬 경로를 고정하지 않는다.

서브에이전트를 사용할 수 없으면 메인 오케스트레이터가 같은 계약과 템플릿을 따라 산출물을 직접 작성한다.

반드시 다룰 산출물:

- 요구사항 요약과 범위
- 사용자·행위자·권한 모델
- 업무 흐름도
- 업무 프로세스 모델
- 도메인 모델과 용어 사전
- 정책 정의서
- 상태 정의서
- 화면 설계서
- 인수 기준과 검증 관점

추가로 검토할 산출물:

- 데이터 정의와 식별자 규칙
- 예외·실패·복구 시나리오
- 알림, 감사 로그, 외부 연동, 배치 같은 운영 이벤트
- 비기능 요구사항과 제약
- API 스펙 작성을 위한 command/query/event 후보

### 3. 모호성을 닫는다

- 산출물 안의 `open_questions`가 구현 범위나 API 스펙을 바꿀 수 있으면 사용자에게 확인한다.
- 확인 전에도 진행 가능한 항목은 `assumptions`로 분리한다.
- 임의 가정이 backend/frontend 계약을 바꾸는 경우에는 완료로 처리하지 않는다.

### 4. 다음 단계 입력을 만든다

기획 산출물이 안정되면 다음 단계에 넘길 경로와 요약을 남긴다.

- `write-api-spec` 입력: 기획 output artifact, API 후보, open question 결과
- `implement-backend` 입력: 도메인 모델, 정책 정의, 상태 정의, backend 책임 후보
- `implement-frontend` 입력: 사용자 흐름, 화면 설계, 상태별 UI, frontend 책임 후보

## 검증

- `product-planning-designer` 계약 문서와 템플릿 링크가 실제 파일을 가리키는지 확인한다.
- output artifact에 업무 흐름, 정책 정의, 상태 정의, 화면 설계, 인수 기준이 모두 있는지 확인한다.
- 구현을 막는 open question이 남아 있으면 완료가 아니라 사용자 확인 필요 상태로 처리한다.
- 스킬 수정 후 `quick_validate.py`와 `check_structured_artifact.py`를 실행한다.

## 완료 기준

- 요구사항의 목표, 범위, 제외사항, 성공 기준이 분리되어 있다.
- 업무 흐름과 상태 전이가 구현 가능한 수준으로 정의되어 있다.
- 정책 정의가 제품 정책, 권한 정책, 검증 정책, 운영 정책으로 나뉘어 있다.
- 화면 설계가 사용자 진입점, 액션, 상태별 피드백을 포함한다.
- API 스펙 작성에 필요한 command/query/event 후보와 데이터 의미가 드러난다.
- 남은 질문은 구현을 막는 질문과 후속 세부화 질문으로 구분되어 있다.
