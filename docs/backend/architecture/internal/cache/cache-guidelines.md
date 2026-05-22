# Cache Guidelines

이 문서는 `backend/internal/cache` 모듈의 실제 코드 위치, 책임, 의존 경계, 구현 전략 보강 기준을 정리한다.

## 코드 위치

- `backend/internal/cache` - cache 저장소나 cache client adapter 후보를 담당한다.

## 책임

- cache 저장소나 cache client 구현 세부사항을 내부 인프라 경계에 둔다.
- application 계약에는 cache provider 세부 타입이 노출되지 않게 한다.
- TTL, key naming, invalidation 전략이 필요한 경우 provider 구현과 함께 문서화한다.

## 의존 경계

- depends on: `core/application`, `core/domain`, cache provider
- used by: Spring runtime, `core/application` Port
- 금지되는 방향: cache provider SDK 타입의 application 노출, domain 모델 내부 cache key 의존

## 핵심 원칙

- cache는 성능 최적화 수단이며 domain 불변식이나 정합성의 유일한 근거가 되면 안 된다.
- cache key와 TTL은 업무 의미 단위로 설명할 수 있어야 한다.
- invalidation 실패가 사용자 상태를 영구히 오염시키지 않도록 재생성 경로를 둔다.

## 관련 정책

- [concurrency-and-performance](../../../policies/concurrency-and-performance.md) - cache TTL, stampede 방지, 성능 경계
- [transaction-and-consistency](../../../policies/transaction-and-consistency.md) - cache invalidation과 정합성 경계

## 금지 규칙

- application Port 시그니처에 provider cache 타입을 노출하지 않는다.
- domain 객체가 cache key, TTL, serialization 방식을 알게 하지 않는다.
- TTL과 invalidation 기준 없이 업무 데이터를 cache하지 않는다.

## 주요 컴포넌트

- Cache adapter: `{Domain}CacheAdapter`
- Cache key factory: `{Domain}CacheKey`
- Cache properties: `{Provider}CacheProperties`
- Cache config: `{Provider}CacheConfig`

## 전략 문서

- 전용 전략 문서 없음

## 완료 기준

- 구현 추가 시 TTL, key naming, invalidation 기준이 이 문서 또는 `strategies` 문서에 설명된다.
- application은 cache provider가 아니라 Port 또는 service 계약에 의존한다.
- cache 장애 시 원천 데이터 조회나 재생성 경로를 설명할 수 있다.
