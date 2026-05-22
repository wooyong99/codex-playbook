# Messaging Guidelines

## 목적

`backend/internal/messaging` 모듈의 책임과 경계를 정리한다.

## 적용 범위

- 메시지 broker adapter 후보 모듈

## 책임

- 메시지 발행과 수신 구현 세부사항을 내부 인프라 경계에 둔다.
- application에는 메시징 provider DTO나 client 예외가 노출되지 않게 한다.

## 의존 경계

`build.gradle.kts` 기준 의존 대상은 `core/application`, `core/domain`이다.

## 확인 필요

- 현재 소스 파일이 없어 retry, dead-letter, outbox, idempotency 전략은 구현 추가 시 문서화한다.
