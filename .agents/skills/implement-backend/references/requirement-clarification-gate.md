# Backend Requirement Clarification Gate

이 문서는 `implement-backend`가 backend 구현을 시작하기 전에 사용자 요구사항의 모호성을 어떻게 분석하고, 어떤 정보가 부족하면 구현을 멈추고 질문해야 하는지 정의한다.

마일스톤 분할은 [milestone-planning.md](milestone-planning.md)가 소유하고, design/implementation/review 실행 순서는 [milestone-execution-workflow.md](milestone-execution-workflow.md)가 소유한다. 이 문서는 그보다 앞선 요구사항 명확화 게이트만 소유한다.

## 목적

`implement-backend`는 추상적인 backend 요청을 바로 구현하지 않는다.

사용자가 "상품 등록 기능 구현", "조회 API 추가", "구조 개선"처럼 추상적으로 요청하면 메인 에이전트는 먼저 구현 방식에 영향을 주는 비즈니스, 운영, 정합성 결정을 식별한다. 결정에 필요한 핵심 정보가 없으면 구현, TDD 작성, architecture review input 생성을 시작하지 않고 사용자에게 질문한다.

## 게이트 위치

요구사항 명확화 게이트는 모든 backend 마일스톤 계획과 서브에이전트 호출보다 먼저 수행한다.

```text
Backend request
  -> Main agent performs requirement clarification gate
  -> If decision-critical info is missing, stop and ask user
  -> Main agent records clarified requirement context
  -> Main agent plans backend milestones
  -> Backend Design Writer / Implementation Engineer / Architecture Reviewer loop
```

## 분석 항목

메인 에이전트는 구현 전에 아래 항목을 확인한다.

- 유저 플로우: 누가, 어떤 순서로, 어떤 목적을 위해 기능을 사용하는가
- 상태 변화 흐름: 생성, 변경, 승인, 취소, 삭제, 노출 같은 상태 전이가 있는가
- 조회 패턴: 관리자 목록, 사용자 피드, 상세 조회, 검색, 리포트 중 무엇인가
- 데이터 규모: 예상 row 수, 증가 속도, 조회 빈도, 장기 보관 여부가 구현 방식에 영향을 주는가
- 정합성 요구사항: 강한 일관성, 최종 일관성, 부분 성공 허용 여부가 무엇인가
- 동시성 요구사항: 중복 요청, 경합 자원, 순서 보장, lock 또는 versioning이 필요한가
- 이벤트 처리 방식: 동기 처리, 비동기 이벤트, outbox, queue, CDC, scheduler가 필요한가
- 실패 처리 정책: rollback, retry, compensation, dead letter, 수동 복구가 필요한가
- 운영 정책: 실패 추적, 재처리 API, 감사 로그, 관리자 개입, 알림, 모니터링이 필요한가
- 성능 요구사항: 응답 시간, 처리량, pagination, index, cache, batch 기준이 있는가

## 질문 우선순위

질문은 구현 영향도가 큰 순서로 묻는다.

1. 유저 플로우
2. 정합성 요구사항
3. 실패 처리 정책
4. 운영 정책
5. 동시성 요구사항
6. 이벤트 처리 방식
7. 성능 요구사항
8. 조회 패턴과 데이터 규모

한 번에 모든 항목을 묻지 않는다. 구현 구조를 결정하는 데 필요한 핵심 질문을 1~3개로 압축하고, 답변에 따라 다음 질문이 필요한지 판단한다.

## 추론 가능 항목

아래 항목은 저장소의 기존 코드와 문서 관례를 근거로 메인 에이전트가 합리적으로 추론할 수 있다.

- 코드 스타일
- 패키지와 모듈 구조
- DTO, UseCase, repository, port naming
- RESTful URL 규칙
- validation, error response, logging 같은 기존 공통 정책의 적용 방식
- compile/test 명령과 artifact 저장 방식

추론한 항목은 확정 요구사항이 아니라 "코드베이스 관례 기반 구현 선택"으로 다룬다.

## 추론 금지 항목

아래 항목은 사용자 또는 명시 Source of Truth와 합의 없이 확정하지 않는다.

- 비즈니스 정책
- 운영 정책
- 실패 처리 정책
- 정합성 정책
- 재처리 정책
- 동시성 정책
- 이벤트 유실 허용 여부
- 감사 로그 필요 여부
- 관리자 개입 또는 수동 복구 필요 여부

이 항목이 구현 방식에 영향을 주는데 입력에서 확인되지 않으면 구현을 시작하지 않는다.

## 운영 가능성 확인

운영 정책은 아키텍처 요구사항으로 취급한다.

- 단순 자동 재시도만 필요하면 retry 정책과 실패 로그 중심으로 설계할 수 있다.
- 운영자가 실패 건을 직접 재처리해야 하면 실패 상태 모델, 운영 API, 멱등성, 감사 로그가 필요할 수 있다.
- 이벤트 유실이 허용되지 않으면 transactional outbox, event sourcing, CDC, transactional messaging, durable queue 기반 command queue 같은 구조를 검토해야 한다.
- 중복 실행을 막아야 하면 idempotency key, unique constraint, versioning, lock, processed event table 중 실제 요구와 코드베이스에 맞는 방식을 선택해야 한다.

운영 정책이 확정되지 않은 상태에서 "일단 retry만 넣는다", "나중에 운영자가 DB를 고친다" 같은 결정을 임의로 하지 않는다.

## 모호한 요청별 질문 예시

상품 등록 기능:

- 상품과 옵션을 하나의 요청에서 함께 저장하는가, 옵션을 나중에 별도로 등록하는가
- 임시 저장, 승인, 노출 상태가 필요한가
- 등록 실패나 외부 연동 실패를 운영자가 추적하거나 재처리해야 하는가

목록 조회 API:

- 관리자 백오피스 목록인가, 사용자 피드/탐색 목록인가
- 데이터 규모와 정렬 기준은 무엇인가
- offset pagination, cursor pagination, search index, cache 중 어떤 선택이 필요한 요구인가

구조 개선:

- 개선 대상 계층과 성공 기준은 무엇인가
- 공개 API, DB schema, 도메인 동작 변경은 제외되는가
- 운영 로그, 오류 정책, transaction boundary 같은 기존 정책을 바꿀 수 있는가

## 확정 요구사항 컨텍스트

게이트를 통과하면 메인 에이전트는 이후 role input artifact에서 참조할 수 있도록 확정 요구사항 컨텍스트를 남긴다.

컨텍스트는 아래 내용을 포함한다.

- 요구사항 결정: 사용자 또는 Source of Truth로 확정된 정책
- 사용자 확인 필요 없음: 코드베이스 관례로 처리해도 되는 구현 선택
- 금지된 추론: 아직 확정되지 않아 구현에 반영하면 안 되는 정책
- 남은 미결정 사항: 이번 마일스톤에서 제외하거나 사용자 확인이 필요한 항목

이 컨텍스트는 독립 파일로 저장하거나 role input artifact의 `설계 입력`, `구현 지시`, `검토 지시` 섹션에 경로로 기록할 수 있다.

## 중단 기준

아래 조건 중 하나라도 해당하면 backend 구현을 시작하지 않고 사용자에게 질문한다.

- 상태 모델, transaction boundary, API 구조 중 하나가 답변에 따라 달라진다.
- 정합성, 실패 처리, 재처리, 운영 정책이 여러 구현 대안으로 갈린다.
- 이벤트 유실 허용 여부나 중복 실행 방지 방식이 불명확하다.
- 조회 API에서 데이터 규모나 사용 패턴에 따라 pagination 또는 indexing 전략이 달라진다.
- 구조 개선 요청에서 변경 가능 범위와 성공 기준이 불명확하다.

단순 CRUD나 국소 리팩토링처럼 결정 영향도가 낮고 기존 코드 관례가 충분히 명확하면, 메인 에이전트는 확정된 기본값과 가정을 기록한 뒤 마일스톤 계획으로 진행할 수 있다.
