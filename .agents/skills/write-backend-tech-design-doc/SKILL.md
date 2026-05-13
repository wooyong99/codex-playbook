---
name: write-backend-tech-design-doc
description: 백엔드 기술설계문서(TDD, Technical Design Document)를 작성하는 스킬. backend 기능 개발이나 시스템 유지보수 시 아키텍처 판단 근거, 계층 분리 설계, 트랜잭션 경계, 예외·실패 처리 전략, 동시성·정합성 보장 방안, 확장 가능성까지 포함하는 실제 구현 가능 수준의 기술설계문서를 생성한다. UseCase, 도메인 모델, storage/external/app/application 계층 변경, DB/schema, 트랜잭션, 정합성, backend 설계 리뷰 자료가 필요할 때 사용한다.
---

# write-backend-tech-design-doc — 백엔드 기술설계문서 작성

## 목적

기술설계문서(TDD)는 "무엇을 만든다"보다 **"왜 이렇게 설계했는가"**에 초점을 맞춘 엔지니어링 문서다.
실행 계획서가 작업 순서와 범위를 다룬다면, TDD는 아키텍처 판단의 근거, 계층 간 책임 분배, 트랜잭션 경계, 실패 시나리오 대응, 동시성 제어, 확장성 설계를 다룬다.

이 문서를 읽는 사람이 "이 코드가 왜 이렇게 생겼는지"를 이해할 수 있어야 한다.

## 적용 범위

포함:

- backend 신규 기능 또는 기존 기능 변경의 설계
- UseCase, 도메인 모델, storage/external/app/application 계층 변경
- DB schema, 트랜잭션, 정합성, 예외, 실패 처리, 동시성, 성능 판단
- 구현 전에 reviewer와 구현자가 공유할 수 있는 설계 근거 문서

제외:

- 단일 CRUD 또는 단순 UseCase 추가처럼 별도 설계 근거가 거의 없는 작업
- frontend 상태/API/component/routing 설계
- 실제 코드 구현 절차를 TDD 안에 장황하게 나열하는 작업
- 저장소 문서와 코드에서 확인되지 않은 프로젝트 규칙을 임의로 추가하는 작업

## 운영 모델

```text
설계 대상 고정
  -> 현재 backend 문서와 코드 근거 수집
  -> 아키텍처와 도메인 판단 도출
  -> 트랜잭션, 실패, 동시성, 검증 전략 정리
  -> TDD 문서 저장 또는 기존 문서 갱신
  -> 문서 맵과 산출물 검증
```

## 참조 문서

- [references/README.md](references/README.md): 이 스킬의 참조 문서 맵
- [backend-tdd-workflow.md](references/backend-tdd-workflow.md): 설계 대상 식별부터 저장까지의 상세 흐름
- [backend-tdd-template.md](references/backend-tdd-template.md): 최종 TDD 구조와 섹션별 작성 기준

## 작업 흐름

1. 사용자 요청에서 설계 대상, 포함 범위, 제외 범위를 한 문장으로 고정한다.
2. 범위가 모호하면 구현이나 문서 작성 전에 질문한다.
3. [backend-tdd-workflow.md](references/backend-tdd-workflow.md)에 따라 필요한 backend 문서와 관련 코드를 선별해 확인한다.
4. 설계 판단은 확인한 근거와 프로젝트의 실제 architecture 문서에 맞춘다.
5. [backend-tdd-template.md](references/backend-tdd-template.md)의 섹션 구조를 기준으로 TDD를 작성한다.
6. 새 문서를 만들면 `docs/backend/design/README.md` 문서 맵을 갱신한다.

## 작성 규칙

- 모든 내용은 한국어로 작성한다.
- 코드 예시, 파일 경로, SQL, 클래스명은 원문 그대로 유지한다.
- 각 주요 설계 결정에는 "왜 이 선택을 했는가"를 함께 적는다.
- 계층 책임, 트랜잭션 경계, 실패 처리, 동시성 제어는 단순 나열이 아니라 판단 근거를 포함한다.
- 해당 없는 섹션은 빈 상태로 두지 않고 생략하거나 `해당 없음`으로 명시한다.

## 검증

- TDD가 설계 배경, 현행 분석, 아키텍처, 도메인 모델, 트랜잭션, 실패 처리, 동시성, 검증 계획을 필요한 수준으로 다루는지 확인한다.
- 설계 판단이 `docs/backend/**`와 실제 backend 코드에서 확인한 사실과 충돌하지 않는지 확인한다.
- 새 파일을 만든 경우 `docs/backend/design/README.md`에 문서 맵이 반영되었는지 확인한다.
- 가능하면 구조 검증을 수행한다.

```bash
python3 .agents/skills/write-structured-artifact/scripts/check_structured_artifact.py .agents/skills/write-backend-tech-design-doc/SKILL.md .agents/skills/write-backend-tech-design-doc/references/*.md
```

## 완료 기준

완료 응답에는 작성 또는 갱신한 TDD 경로, 설계 범위, 주요 설계 판단, 남은 확인 필요 사항을 함께 보고한다.
