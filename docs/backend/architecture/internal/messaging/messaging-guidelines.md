# Messaging Guidelines

이 문서는 `backend/internal/messaging` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략 보강 기준을 정리한다.

## 코드 위치

- `backend/internal/messaging` - message broker adapter 후보를 담당한다.

## 책임

- 메시지 발행과 수신 구현 세부사항을 내부 인프라 경계에 둔다.
- application에는 messaging provider DTO나 client 예외가 노출되지 않게 한다.
- retry, dead-letter, outbox, idempotency 전략이 필요한 경우 broker 구현과 함께 문서화한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, message broker
- used by: Spring runtime, `core/application` Port or event handler
- 금지되는 방향: broker DTO의 application 노출, broker 예외의 application 전파, domain 모델의 topic/queue 의존

## 핵심 원칙

- 메시징은 트랜잭션 결과를 외부로 전달하거나 비동기 처리를 연결하는 adapter다.
- 재시도와 중복 수신 가능성을 전제로 idempotency 기준을 먼저 정한다.
- broker별 topic, queue, header, payload schema는 internal 경계 안에 둔다.

## 관련 정책

- [transaction-and-consistency](../../../policies/transaction-and-consistency.md) - outbox, 이벤트 발행, 정합성 경계
- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - retry, backoff, 처리량 경계
- [logging](../../../policies/logging.md) - 메시지 처리 실패와 추적 로깅

## 금지 규칙

- application Port 시그니처에 broker DTO나 provider client 타입을 노출하지 않는다.
- 메시지 수신 handler에 domain 불변식 판단을 흩어 놓지 않는다.
- retry, dead-letter, idempotency 기준 없이 상태 변경 메시지를 처리하지 않는다.

## 주요 컴포넌트

- Publisher adapter: `{Event}PublisherAdapter`
- Consumer handler: `{Event}MessageHandler`
- Message DTO: `{Event}Message`
- Broker config: `{Provider}MessagingConfig`

## 전략 문서

- 전용 전략 문서 없음

## 완료 기준

- 구현 추가 시 retry, dead-letter, outbox, idempotency 기준이 이 문서 또는 `strategies` 문서에 설명된다.
- application은 broker 구현이 아니라 Port, event, handler 계약에 의존한다.
- 중복 수신과 일시 장애 시 처리 결과를 설명할 수 있다.
