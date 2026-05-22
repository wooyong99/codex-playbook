# Observability Guidelines

이 문서는 `backend/internal/observability` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략 보강 기준을 정리한다.

## 코드 위치

- `backend/internal/observability` - metric, tracing, logging backend adapter 후보를 담당한다.

## 책임

- metric, tracing, logging backend 연동 세부사항을 내부 인프라 경계에 둔다.
- 업무 모듈에는 observability provider SDK 타입이 직접 퍼지지 않게 한다.
- metric naming, trace propagation, alert 연동 전략이 필요한 경우 provider 구현과 함께 문서화한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, observability provider
- used by: Spring runtime, app/support/internal adapters
- 금지되는 방향: provider SDK 타입의 업무 모듈 노출, 민감 정보 원문 metric/tag 기록

## 핵심 원칙

- 관측성은 장애 분석과 운영 판단을 돕는 기술 경계이며 업무 규칙을 소유하지 않는다.
- trace id, metric name, tag는 요청 흐름과 리소스 단위를 일관되게 설명해야 한다.
- 민감 정보는 metric, trace, log tag에 포함하지 않는다.

## 관련 정책

- [logging](../../../policies/logging.md) - 로깅 형식과 민감 정보 차단
- [security](../../../policies/security.md) - 민감 정보 처리
- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - 성능 지표와 병목 관찰

## 금지 규칙

- 업무 모듈이 observability provider SDK에 직접 의존하게 하지 않는다.
- 개인정보, 인증 토큰, 원문 payload를 metric/tag/span attribute로 기록하지 않는다.
- metric naming과 tag cardinality 기준 없이 고카디널리티 값을 남기지 않는다.

## 주요 컴포넌트

- Metric adapter: `{Domain}MetricAdapter`
- Trace config: `{Provider}TraceConfig`
- Observation filter/interceptor: `{Domain}ObservationInterceptor`
- Alert integration: `{Provider}AlertClient`

## 전략 문서

- 전용 전략 문서 없음

## 완료 기준

- 구현 추가 시 metric naming, trace propagation, alert 연동 기준이 이 문서 또는 `strategies` 문서에 설명된다.
- 업무 모듈은 provider SDK가 아니라 공통 관측 계약이나 framework extension에 의존한다.
- 운영자가 주요 실패 흐름을 trace id와 metric으로 추적할 수 있다.
