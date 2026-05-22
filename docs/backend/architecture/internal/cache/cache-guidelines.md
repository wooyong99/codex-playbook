# Cache Guidelines

## 목적

`backend/internal/cache` 모듈의 책임과 경계를 정리한다.

## 적용 범위

- 캐시 adapter 후보 모듈

## 책임

- cache 저장소나 cache client 구현 세부사항을 내부 인프라 경계에 둔다.
- application 계약에는 cache provider 세부 타입이 노출되지 않게 한다.

## 의존 경계

`build.gradle.kts` 기준 의존 대상은 `core/application`, `core/domain`이다.

## 확인 필요

- 현재 소스 파일이 없어 TTL, key naming, invalidation 전략은 구현 추가 시 문서화한다.
