# Observability Guidelines

## 목적

`backend/internal/observability` 모듈의 책임과 경계를 정리한다.

## 적용 범위

- 관측성 adapter 후보 모듈

## 책임

- metric, tracing, logging backend 연동 세부사항을 내부 인프라 경계에 둔다.
- 업무 모듈에는 관측성 provider SDK 타입이 직접 퍼지지 않게 한다.

## 의존 경계

`build.gradle.kts` 기준 의존 대상은 `core/application`, `core/domain`이다.

## 확인 필요

- 현재 소스 파일이 없어 metric naming, trace propagation, alert 연동 전략은 구현 추가 시 문서화한다.
